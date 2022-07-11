import json
from typing import Tuple

from utils.types import *

import requests
from tqdm import tqdm

SETTING_JSON_FILE = "settings.json"


class DingTalkOperator:
    def __init__(self):
        settings: Settings = self.getSettings()

        agentId: str = settings.get("AGENT_ID", None)
        appKey: str = settings.get("APP_KEY", None)
        appSecret: str = settings.get("APP_SECRET", None)

        self.agentId: str = agentId if agentId else input("请输入AgentId: ")
        self.appKey: str = appKey if appKey else input("请输入AppKey: ")
        self.appSecret: str = appSecret if appSecret else input("请输入AppSecret: ")

        departmentIdList = settings.get("PRESET_DEPARTMENTS", None)
        userDict = settings.get("PRESET_MEMBERS", None)

        self.accessToken: str = self.getAccessToken()

        self.departmentIdList: List[DepartmentId] = departmentIdList if departmentIdList else self.getDescendantDepartmentIdList()
        self.userDict: UserNameIdDict = userDict if userDict else self.getFullUser()
        self.settings: Settings = {
            "AGENT_ID": self.agentId,
            "APP_KEY": self.appKey,
            "APP_SECRET": self.appSecret,
            "PRESET_DEPARTMENTS": self.departmentIdList,
            "PRESET_MEMBERS": self.userDict
        }

        self.outputSettings()

    @staticmethod
    def transformDictToFormData(formDict: Dict):
        """将字典中的字典转换为JSON，否则多层字典会导致提交错误。参考资料：https://blog.csdn.net/monkey7777/article/details/75109962"""
        return {k: json.dumps(v, ensure_ascii=False) if isinstance(v, dict) else v for k, v in formDict.items()}

    @staticmethod
    def getSettings() -> Settings:
        try:
            with open(SETTING_JSON_FILE, encoding="utf-8") as settings_json:
                _settings = json.load(settings_json)
        except FileNotFoundError:
            _settings = dict()
        return _settings

    def outputSettings(self):
        with open(SETTING_JSON_FILE, "wt", encoding="utf-8") as file:
            json.dump(self.settings, file, ensure_ascii=False)

    @staticmethod
    def getDingTalkResponse(method: Method, url: str, params, data=None) -> Dict:
        if method == "GET":
            response = requests.get(url, params=params).json()
        elif method == "POST":
            response = requests.post(url, params=params, data=data).json()
        else:
            raise Exception("暂不支持别的请求方式")
        if response.get("errcode", -1) != 0:
            raise Exception(response.get("errmsg", str(response)))
        return response

    def getAccessToken(self) -> str:
        url = "https://oapi.dingtalk.com/gettoken"
        params = dict(appkey=self.appKey, appsecret=self.appSecret)
        accessToken = requests.get(url, params=params).json()["access_token"]
        return accessToken

    def getSimpleUserList(self, dept_id: DepartmentId = 1, cursor=0, size=100) -> List[UserInfoDict]:
        url = "https://oapi.dingtalk.com/topapi/user/listsimple"
        params = dict(access_token=self.accessToken)
        data = dict(dept_id=dept_id, cursor=cursor, size=size)
        response = self.getDingTalkResponse("POST", url, params, data)
        userList: List[UserInfoDict] = response["result"]["list"]

        if response["result"]["has_more"]:
            userList = userList + self.getSimpleUserList(dept_id=dept_id, cursor=cursor + 1, size=size)

        return userList

    def getSubDepartmentIdList(self, departmentId: DepartmentId = 1) -> List[DepartmentId]:
        url = "https://oapi.dingtalk.com/topapi/v2/department/listsubid"
        params = dict(access_token=self.accessToken)
        data = dict(dept_id=departmentId)
        response = self.getDingTalkResponse("POST", url, params, data)
        return response["result"]["dept_id_list"]

    def getDescendantDepartmentIdList(self, departmentId: DepartmentId = 1) -> List[DepartmentId]:
        descendantDepartmentIdList = self.getSubDepartmentIdList(departmentId)
        if len(descendantDepartmentIdList) != 0:
            for descendantDepartmentId in tqdm(descendantDepartmentIdList, desc="正在获取部门信息"):
                descendantDepartmentIdList += self.getSubDepartmentIdList(descendantDepartmentId)
        return descendantDepartmentIdList + [1]  # 根部门 id=1

    def getDepartmentName(self, departmentId: DepartmentId = 1) -> DepartmentName:
        url = "https://oapi.dingtalk.com/topapi/v2/department/get"
        params = dict(access_token=self.accessToken)
        data = dict(dept_id=departmentId)
        response = self.getDingTalkResponse("POST", url, params, data)
        return response["result"]["name"]

    def getUserDetail(self, userId: UserId) -> Dict:
        url = "https://oapi.dingtalk.com/topapi/v2/user/get"
        params = dict(access_token=self.accessToken)
        data = dict(userid=userId)
        response = self.getDingTalkResponse("POST", url, params, data)
        return response["result"]

    def getUserDepartmentIdList(self, userId: UserId) -> List[DepartmentId]:
        return [departmentId for departmentId in self.getUserDetail(userId)["dept_id_list"]]

    def getUserUnionId(self, userId: UnionId) -> UnionId:
        return self.getUserDetail(userId)["unionid"]

    def getDepartmentNameListOfUser(self, userId: UserId) -> List[DepartmentName]:
        departmentIdList = self.getUserDepartmentIdList(userId)
        return [self.getDepartmentName(departmentId) for departmentId in departmentIdList]

    def getFullUser(self) -> UserNameIdDict:
        userDict: Dict[UserName, UserId] = {}
        for departmentId in tqdm(self.departmentIdList, desc="正在获取部门成员信息"):
            userInfoList = self.getSimpleUserList(dept_id=departmentId)
            for userInfo in userInfoList:
                if previousUserId := userDict.get(userInfo["name"], None):
                    if previousUserId != userInfo["userid"]:
                        print(f"\n\n警告: 发现相同名称的成员!")
                        print(f"{userInfo['name']}({previousUserId}), 部门：{self.getDepartmentNameListOfUser(previousUserId)}")
                        print(f"{userInfo['name']}({userInfo['userid']})，部门：{self.getDepartmentNameListOfUser(userInfo['userid'])}\n")
                        continue
                userDict[userInfo["name"]] = userInfo["userid"]
        return userDict

    def filterUsers(self, givenUserNames: List[UserName]) -> list[Tuple[UserName, UserId]]:
        return [(userName, self.userDict[userName]) for userName in givenUserNames if userName in self.userDict]

    def sendCorporationMsg(self, user_id_list: List[UserId], msg: Dict) -> Dict:
        """
        发送工作消息\n
        :param user_id_list: 发送目标的id
        :param msg: 发送的消息内容
        :return: post请求后的结果
        """
        url = "https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2"
        params = dict(access_token=self.accessToken)
        data = {"agent_id": self.agentId,
                "msg": msg,
                "userid_list": ",".join(user_id_list)}

        response = self.getDingTalkResponse("POST", url, params, self.transformDictToFormData(data))
        print("发送完成!")
        return response

    def sendCorporationTextMsg(self, user_id_list: List[UserId], text: str) -> Dict:
        """发送文字类型的工作消息"""
        return self.sendCorporationMsg(user_id_list, msg={"msgtype": "text", "text": {"content": text}})

    def getAdministratorInfoList(self) -> List[AdministratorInfo]:
        url = "https://oapi.dingtalk.com/topapi/user/listadmin"
        params = dict(access_token=self.accessToken)
        response = self.getDingTalkResponse("POST", url, params)
        return response["result"]

    def getMainAdministratorId(self) -> UserId:
        return [admin['userid'] for admin in self.getAdministratorInfoList() if admin['sys_level'] == 1][0]
