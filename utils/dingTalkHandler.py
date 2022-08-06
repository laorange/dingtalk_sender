import json
import datetime

import httpx
from tqdm import tqdm
import asyncio

from utils.types import *


def getSettings(settingFileName) -> Settings:
    import json
    _settings = dict()
    try:
        with open(settingFileName, encoding="utf-8") as settings_json:
            print(f"\nTIPS：已自动加载缓存。若需重新输入密钥等敏感信息，请删除配置文件”{settingFileName}“\n")
            _settings = json.load(settings_json)
    finally:
        return _settings


def outputSettings(settings: Settings, settingFileName):
    with open(settingFileName, "wt", encoding="utf-8") as file:
        json.dump(settings, file, ensure_ascii=False)


class DingTalkHandler:
    def __init__(self, settingFileName: str = "settings.json"):
        self.settingFileName = settingFileName
        settings = getSettings(settingFileName)
        # 权限
        self.agentId: str = _ if (_ := settings.get("AGENT_ID", None)) else input("请输入AgentId: ")
        self.appKey: str = _ if (_ := settings.get("APP_KEY", None)) else input("请输入AppKey: ")
        self.appSecret: str = _ if (_ := settings.get("APP_SECRET", None)) else input("请输入AppSecret: ")
        assert self.agentId and self.appKey and self.appSecret

        self.accessToken: str = self.getAccessToken()

        self.status = settings.get("STATUS", "INIT")

        if self.status == "DONE":
            self.addressBook: AddressBook = settings.get("ADDRESS_BOOK", {})
        else:
            asyncio.run(self.refreshAddressBook())

    async def refreshAddressBook(self):
        self.addressBook = await self.getAddressBook()
        outputSettings({"AGENT_ID": self.agentId,
                        "APP_KEY": self.appKey,
                        "APP_SECRET": self.appSecret,
                        "STATUS": self.status,
                        "ADDRESS_BOOK": self.addressBook}, self.settingFileName)

    def getAccessToken(self) -> str:
        url = "https://oapi.dingtalk.com/gettoken"
        params = dict(appkey=self.appKey, appsecret=self.appSecret)
        try:
            accessToken = httpx.get(url, params=params).json()["access_token"]
        except Exception as e:
            print(f"ERROR：验证密钥失败，请检查应用凭证是否正确，或检查网络连接。({e})")
            raise e
        self.status = "PREPARED"
        self.accessToken = accessToken
        return accessToken

    @staticmethod
    async def getDingTalkResponse(method: Method, url: str, **kwargs) -> Dict:
        if method == "GET":
            async with httpx.AsyncClient() as client:
                response = (await client.get(url, **kwargs)).json()
        elif method == "POST":
            async with httpx.AsyncClient() as client:
                response = (await client.post(url, **kwargs)).json()
        else:
            raise Exception("暂不支持别的请求方式")
        if response.get("errcode", -1) != 0:
            raise Exception(response.get("errmsg", str(response)))
        return response

    async def getSubDepartmentIdList(self, departmentId: DepartmentId = 1) -> List[DepartmentId]:
        url = "https://oapi.dingtalk.com/topapi/v2/department/listsubid"
        params = dict(access_token=self.accessToken)
        data = dict(dept_id=departmentId)
        response = await self.getDingTalkResponse("POST", url=url, params=params, json=data)
        return response["result"]["dept_id_list"]

    async def getDescendantDepartmentIdList(self, departmentId: DepartmentId = 1) -> List[DepartmentId]:
        descendantDepartmentIdList = await self.getSubDepartmentIdList(departmentId)
        if len(descendantDepartmentIdList) != 0:
            for descendantDepartmentId in tqdm(descendantDepartmentIdList, desc="正在获取部门信息"):
                descendantDepartmentIdList += await self.getSubDepartmentIdList(descendantDepartmentId)
        return descendantDepartmentIdList + [1]  # 根部门 id=1

    async def getSimpleUserList(self, dept_id: DepartmentId = 1, cursor=0, size=100) -> List[UserInfoDict]:
        url = "https://oapi.dingtalk.com/topapi/user/listsimple"
        params = dict(access_token=self.accessToken)
        data = dict(dept_id=dept_id, cursor=cursor, size=size)
        response = await self.getDingTalkResponse("POST", url, params=params, json=data)
        userList: List[UserInfoDict] = response["result"]["list"]

        if response["result"]["has_more"]:
            userList = userList + (await self.getSimpleUserList(dept_id=dept_id, cursor=cursor + 1, size=size))

        return userList

    async def getUserDetail(self, userId: UserId) -> UserDetail:
        url = "https://oapi.dingtalk.com/topapi/v2/user/get"
        params = dict(access_token=self.accessToken)
        data = dict(userid=userId)
        response = await self.getDingTalkResponse("POST", url, params=params, json=data)
        return response["result"]

    async def getUserDetailListOfDepartment(self, dept_id: DepartmentId = 1) -> List[UserDetail]:
        simpleUserList = await self.getSimpleUserList(dept_id)

        # return [await self.getUserDetail(simpleUser["userid"]) for simpleUser in simpleUserList]

        # # 不可行：会请求到钉钉限流
        # userDetailListOfDepartment: List[UserDetail] = []
        # for f in asyncio.as_completed([self.getUserDetail(simpleUser["userid"]) for simpleUser in simpleUserList]):
        #     userDetailListOfDepartment.append(await f)
        # return userDetailListOfDepartment

        return [(await self.getUserDetail(simpleUser["userid"])) for simpleUser in simpleUserList]

    async def getDepartmentName(self, departmentId: DepartmentId = 1) -> DepartmentName:
        url = "https://oapi.dingtalk.com/topapi/v2/department/get"
        params = dict(access_token=self.accessToken)
        data = dict(dept_id=departmentId)
        response = await self.getDingTalkResponse("POST", url, params=params, json=data)
        return response["result"]["name"]

    async def getDeptAddressBook(self, dept_id: DepartmentId = 1) -> DeptAddressBook:
        return {"dept_id": dept_id, "dept_name": await self.getDepartmentName(dept_id), "users": await self.getUserDetailListOfDepartment(dept_id)}

    async def getAddressBook(self) -> AddressBook:
        self.status = "WORKING"
        departmentIdList = await self.getDescendantDepartmentIdList()
        addressBook = [(await self.getDeptAddressBook(departmentId)) for departmentId in tqdm(departmentIdList, desc="正在获取部门成员信息")]
        self.status = "DONE"
        return addressBook

    def createMyCalendar(self, publisherUserUnionId: UnionId, users: List[UserDetail], start: datetime.datetime, end: datetime.datetime,
                         summary: str, description: str = ""):
        """
        根据自定义需求的创建日程，发布后即刻通知 \n
        :param publisherUserUnionId: 发布者的ID
        :param users: 日程参与者的信息
        :param start: 日程开始时间
        :param end: 日程结束时间
        :param summary: 日程标题，最大不超过2048个字符。
        :param description: 日程描述，最大不超过5000个字符。
        :return: None
        """

        url = f"https://api.dingtalk.com/v1.0/calendar/users/{publisherUserUnionId}/calendars/primary/events"
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
                # {"method": "dingtalk", "minutes": (end - start).seconds // 60},  # 通知发布后，应用内提醒
                # {"method": "dingtalk", "minutes": 60 if (end - start).seconds // 60 > 60 else (end - start).seconds // 60 // 2},  # 只剩60分钟，短信提醒
            ]
        }

        response = httpx.post(url, headers=headers, json=data).json()
        return response

    async def sendBulletin(self, data) -> Dict:
        url = "https://oapi.dingtalk.com/topapi/blackboard/create"
        params = dict(access_token=self.accessToken)

        # private_level = 20 if whether_private else 0
        # data = {"create_request": {
        #     "operation_userid": self.publisher[1],
        #     "private_level": private_level,
        #     "ding": whether_ding,
        #     "blackboard_receiver": {
        #         "userid_list": user_id_list
        #     },
        #     "title": title,
        #     "content": content,
        #     "push_top": whether_push_top,
        #     "author": self.publisher[0]
        # }}

        return await self.getDingTalkResponse("POST", url, params=params, json=data)
