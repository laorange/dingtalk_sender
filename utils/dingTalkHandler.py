import json
import datetime

import httpx
from tqdm import tqdm

from utils.types import *


def getSettings(settingFileName) -> Settings:
    import json
    _settings = dict()
    try:
        with open(settingFileName, encoding="utf-8") as settings_json:
            print("TIPS：已自动加载缓存。若需重新拉取组织成员信息，请删除或编辑配置文件”settings.json“\n")
            _settings = json.load(settings_json)
    finally:
        return _settings


def outputSettings(settings: Settings, settingFileName):
    with open(settingFileName, "wt", encoding="utf-8") as file:
        json.dump(settings, file, ensure_ascii=False)


class DingTalkHandler:
    def __init__(self, settingFileName: str = "settings.json"):
        settings = getSettings(settingFileName)
        # 权限
        self.agentId: str = _ if (_ := settings.get("AGENT_ID", None)) else input("请输入AgentId: ")
        self.appKey: str = _ if (_ := settings.get("APP_KEY", None)) else input("请输入AppKey: ")
        self.appSecret: str = _ if (_ := settings.get("APP_SECRET", None)) else input("请输入AppSecret: ")
        assert self.agentId and self.appKey and self.appSecret

        self.accessToken: str = self.getAccessToken()

        self.addressBook: AddressBook = {}
        self.status = settings.get("STATUS", "INIT")

        if self.status != "DONE":
            self.fetchAddressBook()
            outputSettings({"AGENT_ID": self.agentId,
                            "APP_KEY": self.appKey,
                            "APP_SECRET": self.appSecret,
                            "STATUS": self.status,
                            "ADDRESS_BOOK": self.addressBook}, settingFileName)

    def getAccessToken(self) -> str:
        url = "https://oapi.dingtalk.com/gettoken"
        params = dict(appkey=self.appKey, appsecret=self.appSecret)
        accessToken = httpx.get(url, params=params).json()["access_token"]
        self.status = "PREPARED"
        return accessToken

    @staticmethod
    def getDingTalkResponse(method: Method, url: str, **kwargs) -> Dict:
        if method == "GET":
            response = httpx.get(url, **kwargs).json()
        elif method == "POST":
            response = httpx.post(url, **kwargs).json()
        else:
            raise Exception("暂不支持别的请求方式")
        if response.get("errcode", -1) != 0:
            raise Exception(response.get("errmsg", str(response)))
        return response

    def getSubDepartmentIdList(self, departmentId: DepartmentId = 1) -> List[DepartmentId]:
        url = "https://oapi.dingtalk.com/topapi/v2/department/listsubid"
        params = dict(access_token=self.accessToken)
        data = dict(dept_id=departmentId)
        response = self.getDingTalkResponse("POST", url=url, params=params, json=data)
        return response["result"]["dept_id_list"]

    def getDescendantDepartmentIdList(self, departmentId: DepartmentId = 1) -> List[DepartmentId]:
        descendantDepartmentIdList = self.getSubDepartmentIdList(departmentId)
        if len(descendantDepartmentIdList) != 0:
            for descendantDepartmentId in tqdm(descendantDepartmentIdList, desc="正在获取部门信息"):
                descendantDepartmentIdList += self.getSubDepartmentIdList(descendantDepartmentId)
        return descendantDepartmentIdList + [1]  # 根部门 id=1

    def getSimpleUserList(self, dept_id: DepartmentId = 1, cursor=0, size=100) -> List[UserInfoDict]:
        url = "https://oapi.dingtalk.com/topapi/user/listsimple"
        params = dict(access_token=self.accessToken)
        data = dict(dept_id=dept_id, cursor=cursor, size=size)
        response = self.getDingTalkResponse("POST", url, params=params, json=data)
        userList: List[UserInfoDict] = response["result"]["list"]

        if response["result"]["has_more"]:
            userList = userList + (self.getSimpleUserList(dept_id=dept_id, cursor=cursor + 1, size=size))

        return userList

    def getUserDetail(self, userId: UserId) -> UserDetail:
        url = "https://oapi.dingtalk.com/topapi/v2/user/get"
        params = dict(access_token=self.accessToken)
        data = dict(userid=userId)
        response = self.getDingTalkResponse("POST", url, params=params, json=data)
        return response["result"]

    def getUserDetailListOfDepartment(self, dept_id: DepartmentId = 1) -> List[UserDetail]:
        simpleUserList = self.getSimpleUserList(dept_id)

        return [self.getUserDetail(simpleUser["userid"]) for simpleUser in simpleUserList]

    def fetchAddressBook(self):
        self.status = "WORKING"
        departmentIdList = self.getDescendantDepartmentIdList()
        self.addressBook = {departmentId: (self.getUserDetailListOfDepartment(departmentId))
                            for departmentId in tqdm(departmentIdList, desc="正在获取部门成员信息")}
        self.status = "DONE"

    def createMyCalendar(self, publisherUserId: UserId, users: List[UserDetail], start: datetime.datetime, end: datetime.datetime,
                         summary: str, description: str = ""):
        """
        根据自定义需求的创建日程，发布后即刻通知 \n
        :param publisherUserId: 发布者的ID
        :param users: 日程参与者的信息
        :param start: 日程开始时间
        :param end: 日程结束时间
        :param summary: 日程标题，最大不超过2048个字符。
        :param description: 日程描述，最大不超过5000个字符。
        :return: None
        """

        url = f"https://api.dingtalk.com/v1.0/calendar/users/{publisherUserId}/calendars/primary/events"
        headers = {"x-acs-dingtalk-access-token": self.accessToken}
        data = {
            "summary": summary,
            "description": description,
            "start": {
                # "date": start.strftime("%Y-%m-%d"),
                "dateTime": start.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
                "timeZone": "Asia/Shanghai",
            },
            "end": {
                # "date": end.strftime("%Y-%m-%d"),
                "dateTime": end.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
                "timeZone": "Asia/Shanghai",
            },
            "isAllDay": False,
            "attendees": [
                {"id": user["unionid"], "isOptional": False} for user in (users if len(users) <= 500 else users[:499])
            ],
            "reminders": [
                {"method": "dingtalk", "minutes": (end - start).seconds // 60 - 2},  # 通知发布2分钟后，应用内提醒
                {"method": "dingtalk", "minutes": 60 if (end - start).seconds // 60 > 60 else (end - start).min // 2},  # 只剩60分钟，短信提醒
            ]
        }

        response = httpx.post(url, headers=headers, json=data).json()
        return response
