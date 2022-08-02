from utils.dingTalkHandler import DingTalkHandler
from sanic import Sanic
from sanic.response import json

file = "settings-sillage.db"
dingTalkHandler = DingTalkHandler(file)

app = Sanic("dingTalkSender")

@app.get("/address-book/")
async def addressBook(request):
    return json(dingTalkHandler.addressBook)


if __name__ == '__main__':
    app.static("/", "./front-end/dist/index.html", name="index")
    app.static("/static", "./front-end/dist", name="dist")
    app.run(host='localhost', port=8095)
