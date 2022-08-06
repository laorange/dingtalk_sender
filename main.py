import os
import sys
import traceback

from utils.dingTalkHandler import DingTalkHandler
from sanic import Sanic
from sanic.response import json as jsonResponse
from sanic_cors import CORS

app = Sanic("dingTalkSender")
CORS(app)


@app.get("/address-book/")
async def addressBook(request):
    return jsonResponse(dingTalkHandler.addressBook)


@app.get("/access-token/")
async def addressBook(request):
    return jsonResponse({"accessToken": dingTalkHandler.getAccessToken()})


@app.post("/send-bulletin/")
async def sendBulletin(request):
    try:
        return jsonResponse(await dingTalkHandler.sendBulletin(data=request.json))
    except Exception as e:
        return jsonResponse({"errorMsg": f"{e}"}, status=400)


@app.websocket("/refresh-address-book/")
async def feed(request, ws):
    while True:
        await ws.recv()
        await dingTalkHandler.refreshAddressBook()
        await ws.send("prepared")


if __name__ == '__main__':
    try:
        dingTalkHandler = DingTalkHandler("settings.db")

        # region 适配pyinstaller打包后的静态文件位置
        if getattr(sys, 'frozen', None):
            basedir = sys._MEIPASS
        else:
            basedir = os.path.dirname(__file__)

        app.static("/", os.path.join(basedir, "front-end/dist/index.html"), name="index")
        app.static("/favicon.ico", os.path.join(basedir, "front-end/dist/favicon.ico"), name="favicon")
        app.static("/static", os.path.join(basedir, "front-end/dist"), name="dist")  # endregion

        PORT = 8095
        try:
            os.startfile(f"http://localhost:{PORT}")
        finally:
            app.run(host='localhost', port=PORT)
    except:
        traceback.print_exc()
    finally:
        input("程序结束，如需关闭，请敲击回车: ")
