import traceback

from utils.dingTalkOperator import DingTalkOperator

__version__ = "1.0.0"

"""
> 钉钉应用类型：**企业内部开发**
需要在钉钉后台开启如下权限：
+ 通讯录管理：
    + 通讯录部门信息读权限
    + 成员信息读权限
    + 通讯录部门成员读权限
+ 公告
    + 钉钉公告管理权限
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


def main_dev():
    operator = DingTalkOperator()
    operator.sendBulletin(["userId"], "培训通知", "请按时学习。\n点击此处→确认收到")


def main_product():
    try:
        operator = DingTalkOperator()

        text = input("请输入想要发送的信息: ")
        users = get_filtered_users()

        filtered_users = operator.filterUserTuples(users)

        if filtered_users:
            print(f'根据您的输入，成功检索到了这些用户：{",".join([user[0] for user in filtered_users])}')
            print(f'即将向他们发送"{text}"')
            filtered_user_id_list = [user[1] for user in filtered_users]
            send_feedback = operator.sendBulletin(filtered_user_id_list, "培训通知", f"{text}")
            print(f"\n发送结果：{send_feedback}\n")
        else:
            print("没有找到符合条件的用户，请查证后重试")
    except:
        print(traceback.format_exc())
    finally:
        input("请敲击回车来结束程序：")


if __name__ == '__main__':
    print(f"{'-'*10} 当前版本：v{__version__} {'-'*10}\n")
    main_product()
