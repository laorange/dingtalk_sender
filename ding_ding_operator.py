import json
from typing import List, TypedDict

import requests


class DingUserInfo(TypedDict):
    name: str
    userid: str


class DingDingOperator:
    def __init__(self, agentId, appKey, appSecret):
        self.appSecret = appSecret
        self.appKey = appKey
        self.agentId = agentId

        self.accessToken = self.getAccessToken()
        self.users: List[DingUserInfo] = self.getUserListSimple()

    def getAccessToken(self) -> str:
        url = "https://oapi.dingtalk.com/gettoken"
        params = dict(appkey=self.appKey, appsecret=self.appSecret)
        accessToken = requests.get(url, params=params).json()["access_token"]
        return accessToken

    def getUserListSimple(self, dept_id=1, cursor=0, size=100) -> List[DingUserInfo]:
        url = "https://oapi.dingtalk.com/topapi/user/listsimple"
        params = dict(access_token=self.accessToken)
        data = dict(dept_id=dept_id, cursor=cursor, size=size)
        response = requests.post(url, params=params, data=data).json()
        if response.get("errcode", -1) != 0:
            raise Exception(response.get("errmsg", str(response)))
        userList: List[DingUserInfo] = response["result"]["list"]

        if response["result"]["has_more"]:
            userList = userList + self.getUserListSimple(dept_id=dept_id, cursor=cursor + 1, size=size)

        return userList

    def filterUsers(self, givenUserNames: List[str]) -> List[DingUserInfo]:
        return [user for user in self.users if (user["name"] in givenUserNames)]

    def sent_text_msg(self, user_id_list: List[str], text: str):
        """
        发送文字信息
        :param text : 发送的消息内容
        :param user_id_list : 发送目标的id
        :return post请求后的结果
        """
        url = "https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2"
        params = dict(access_token=self.accessToken)

        msg = json.dumps({"msgtype": "text", "text": {"content": text}}),
        data = {"agent_id": self.agentId,
                "msg": msg,
                "userid_list": ",".join(user_id_list)}

        response = requests.post(url, params=params, data=data).json()
        if response.get("errcode", -1) != 0:
            raise Exception(f"请求错误：{response.get('errmsg', str(response))}")
        else:
            return response
