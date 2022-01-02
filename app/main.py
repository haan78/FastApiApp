import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel
from pymongo import MongoClient

from lib.DotEnv import ReadDotEnvFile
from lib.FastLib import FastLib
from FastSession.FastMongoSession import FastMongoSession

import random

settings = ReadDotEnvFile(".env", ["JWTKEY", "DBCONN", "DBNAME"])

fsm = FastMongoSession(MongoClient(settings["DBCONN"]).get_database(settings["DBNAME"]).get_collection("session"), timeout=600)

app = FastAPI()

FastLib.jwtkey = settings["JWTKEY"]

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/jsdist", StaticFiles(directory="jsdist"), name="jsdist")


class testObj(BaseModel):
    test: str


@app.get("/", response_class=HTMLResponse)
async def index_html():
    return FastLib().html("index.html", {"module": "main", "rndint": "rnd"+str(random.randint(1, 1000))})


@app.get("/test")
def test(request: Request):
    return {
        "header1": request.headers.get("User-Agent"),
        "header2": request.headers.get("user-agent")
    }


@app.get("/gotoerr")
def gotoerr():
    return RedirectResponse("/err")


@app.get("/err")
def err():
    raise Exception("Deneme")


@app.exception_handler(Exception)
def error(request: Request, exc: Exception):
    return FastLib().response(exc)


@app.post("/identity")
def identity(test: testObj, request: Request):
    id = FastLib().identity(request)
    return {
        "test": test,
        "id": id
    }


@app.post("/identity2")
async def identity2(request: Request):
    id = FastLib().identity(request)
    jd = await request.json()
    return {
        "jData": jd,
        "id": id
    }


@app.get("/write")
def setcoo(response: Response):
    fsm.write(response, {
        "name": "Ali Barış Öztürk"
    })
    return "Yazıldı"


@app.get("/read")
async def read_items(request: Request):
    v = fsm.read(request)
    return {"ads_id": v}


@app.get("/kill")
async def kill(response: Response):
    fsm.kill(response)
    return "silindi"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
