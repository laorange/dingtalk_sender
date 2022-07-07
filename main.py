import json

from ding_ding_operator import DingDingOperator

with open("settings.json", encoding="utf-8") as settings_json:
    settings = json.load(settings_json)

if __name__ == '__main__':
    text = input("请输入想要发送的信息: ")
    users = []
    while 1:
        new_user = input("请输入接收者的姓名: ")
        if new_user:
            users.append(new_user)
            print("(若已完成输入，请直接回车)")
        else:
            break
    operator = DingDingOperator(settings["AGENT_ID"], settings["APP_KEY"], settings["APP_SECRET"])
    filtered_users = operator.filterUsers(users)
    print(f'根据您的输入，成功检索到了这些用户：{[user["name"] for user in filtered_users]}')
    print(f'即将向他们发送"{text}"')
    filtered_user_id_list = [user["userid"] for user in filtered_users]
    print(operator.sent_text_msg(filtered_user_id_list, text))
