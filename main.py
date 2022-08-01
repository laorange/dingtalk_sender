from utils.dingTalkHandler import DingTalkHandler
import datetime

if __name__ == '__main__':
    file = "settings-sillage.db"

    dingTalkHandler = DingTalkHandler(file)

    print("prepared")

    # calendarInfo = dingTalkHandler.createMyCalendar("", receivers,
    #                                  datetime.datetime.now(),
    #                                  datetime.datetime.now() + datetime.timedelta(hours=2),
    #                                  "测试", "消息的内容")
    # print(calendarInfo)
