import os

from utils.dingTalkHandler import DingTalkHandler
from sanic import Sanic
from sanic.response import json as jsonResponse
from sanic_cors import CORS

file = "settings.db"
dingTalkHandler = DingTalkHandler(file)

app = Sanic("dingTalkSender")
CORS(app)

app.static("/", "./front-end/dist/index.html", name="index")
app.static("/favicon.ico", "./front-end/dist/favicon.ico", name="favicon")
app.static("/static", "./front-end/dist", name="dist")


@app.get("/address-book/")
async def addressBook(request):
    return jsonResponse(dingTalkHandler.addressBook)


@app.get("/access-token/")
async def addressBook(request):
    return jsonResponse({"accessToken": dingTalkHandler.getAccessToken()})


@app.websocket("/refresh-address-book/")
async def feed(request, ws):
    while True:
        await ws.recv()
        await dingTalkHandler.refreshAddressBook()
        await ws.send("prepared")


if __name__ == '__main__':
    PORT = 8095
    os.startfile(f"http://localhost:{PORT}")
    app.run(host='localhost', port=PORT)
