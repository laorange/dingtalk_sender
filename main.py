from dingTalkOperator import DingTalkOperator

"""
钉钉应用类型：企业内部开发
需要在钉钉后台开启如下权限：
+ 通讯录管理：
    + 通讯录部门信息读权限
    + 成员信息读权限
    + 通讯录部门成员读权限
"""


def get_filtered_users():
    _users = []
    while 1:
        new_user = input("请输入接收者的姓名: ")
        if new_user:
            _users.append(new_user)
            print("(若已完成输入，请直接回车)", end="")
        else:
            break
    return _users


if __name__ == '__main__':
    operator = DingTalkOperator()

    text = input("请输入想要发送的信息: ")
    users = get_filtered_users()

    filtered_users = operator.filterUsers(users)

    if filtered_users:
        print(f'根据您的输入，成功检索到了这些用户：{",".join([user[0] for user in filtered_users])}')
        print(f'即将向他们发送"{text}"')
        filtered_user_id_list = [user[1] for user in filtered_users]
        send_feedback = operator.sendCorporationTextMsg(filtered_user_id_list, text)
        print(send_feedback)
    else:
        print("没有找到符合条件的用户，请查证后重试")
    input("请敲击回车来结束程序：")
