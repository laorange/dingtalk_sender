from utils.dingTalkHandler import DingTalkHandler
from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS

file = "settings.db"
dingTalkHandler = DingTalkHandler(file)

app = Sanic("dingTalkSender")
CORS(app)

app.static("/", "./front-end/dist/index.html", name="index")
app.static("/static", "./front-end/dist", name="dist")


@app.get("/address-book/")
async def addressBook(request):
    return json(dingTalkHandler.addressBook)


@app.get("/access-token/")
async def addressBook(request):
    return json({"accessToken": dingTalkHandler.accessToken})


if __name__ == '__main__':
    app.run(host='localhost', port=8095)
