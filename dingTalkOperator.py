import json
from typing import List, TypedDict, Dict, Tuple
from tqdm import tqdm

import requests

SETTING_JSON_FILE = "settings.json"


class SimpleUserInfoDict(TypedDict):
    name: str
    userid: str


class DepartmentDict(TypedDict):
    ext: str  # --------------------------- "ext": "{\"faceCount\":\"int\"}",
    auto_add_user: bool  # ---------------- "auto_add_user": true,
    parent_id: int  # --------------------- "parent_id": 1,
    name: str  # -------------------------- "name": "xx部门",
    dept_id: int  # ----------------------- "dept_id": int,
    create_dept_group: bool  # ------------ "create_dept_group": true


class DingTalkOperator:
    def __init__(self):
        settings = self.getSettings()

        agentId = settings.get("AGENT_ID", None)
        appKey = settings.get("APP_KEY", None)
        appSecret = settings.get("APP_SECRET", None)

        self.agentId: str = agentId if agentId else input("请输入AgentId: ")
        self.appKey: str = appKey if appKey else input("请输入AppKey: ")
        self.appSecret: str = appSecret if appSecret else input("请输入AppSecret: ")

        departmentIdList = settings.get("PRESET_DEPARTMENTS", None)
        userDict = settings.get("PRESET_MEMBERS", None)

        self.accessToken = self.getAccessToken()

        self.departmentIdList = departmentIdList if departmentIdList else self.getDescendantDepartmentIdList()
        self.userDict = userDict if userDict else self.getFullUser()
        self.settings = {
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
    def getSettings():
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
    def getDingTalkResponse(method, url, params, data=None):
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

    def getSimpleUserList(self, dept_id=1, cursor=0, size=100) -> List[SimpleUserInfoDict]:
        url = "https://oapi.dingtalk.com/topapi/user/listsimple"
        params = dict(access_token=self.accessToken)
        data = dict(dept_id=dept_id, cursor=cursor, size=size)
        response = self.getDingTalkResponse("POST", url, params, data)
        userList: List[SimpleUserInfoDict] = response["result"]["list"]

        if response["result"]["has_more"]:
            userList = userList + self.getSimpleUserList(dept_id=dept_id, cursor=cursor + 1, size=size)

        return userList

    def getSubDepartmentIdList(self, departmentId: int = 1) -> List[int]:
        url = "https://oapi.dingtalk.com/topapi/v2/department/listsubid"
        params = dict(access_token=self.accessToken)
        data = dict(dept_id=departmentId)
        response = self.getDingTalkResponse("POST", url, params, data)
        return response["result"]["dept_id_list"]

    def getDescendantDepartmentIdList(self, departmentId: int = 1) -> List[int]:
        descendantDepartmentIdList = self.getSubDepartmentIdList(departmentId)
        if len(descendantDepartmentIdList) != 0:
            for descendantDepartmentId in tqdm(descendantDepartmentIdList, desc="正在获取部门信息"):
                descendantDepartmentIdList += self.getSubDepartmentIdList(descendantDepartmentId)
        return descendantDepartmentIdList + [1]  # 根部门 id=1

    def getDepartmentName(self, departmentId: int = 1) -> str:
        url = "https://oapi.dingtalk.com/topapi/v2/department/get"
        params = dict(access_token=self.accessToken)
        data = dict(dept_id=departmentId)
        response = self.getDingTalkResponse("POST", url, params, data)
        return response["result"]["name"]

    def getDepartmentIdListOfUser(self, userId: str) -> List[int]:
        url = "https://oapi.dingtalk.com/topapi/v2/user/get"
        params = dict(access_token=self.accessToken)
        data = dict(userid=userId)
        response = self.getDingTalkResponse("POST", url, params, data)
        return response["result"]["dept_id_list"]

    def getDepartmentNameListOfUser(self, userId: str) -> List[str]:
        departmentIdList = self.getDepartmentIdListOfUser(userId)
        return [self.getDepartmentName(departmentId) for departmentId in departmentIdList]

    def getFullUser(self):
        userDict: Dict[str, str] = {}
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

    def filterUsers(self, givenUserNames: List[str]) -> list[Tuple[str, str]]:
        return [(userName, self.userDict[userName]) for userName in givenUserNames if userName in self.userDict]

    def sendCorporationTextMsg(self, user_id_list: List[str], text: str):
        """
        发送工作信息\n
        :param user_id_list: 发送的消息内容
        :param text: 发送目标的id
        :return: post请求后的结果
        """
        if not user_id_list:
            return print("发送名单为空！")
        url = "https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2"
        params = dict(access_token=self.accessToken)
        data = {"agent_id": self.agentId,
                "msg": {"msgtype": "text", "text": {"content": text}},
                "userid_list": ",".join(user_id_list)}

        response = self.getDingTalkResponse("POST", url, params, self.transformDictToFormData(data))
        print("发送完成!")
        return response
