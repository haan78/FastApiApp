from datetime import datetime
from fastapi import FastAPI,Response,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
import random
from lib.FastLib import FastLib
from project import Project

from api import API

def create():
    prj = Project(".env")
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="/static"), name="static")
        
    @app.get("/login",response_class=HTMLResponse)
    def login():
        v = FastLib.toJS({
                "tarih":datetime.now(),
                "isim":"Ali Barış Öztürk"
            },True)
        print(v)
        return FastLib.template("template.html",{
            "rnd":"rnd"+str(random.randint(1,1000)).rjust(4,"0"),
            "module":"login"          
        },{"BEDATA":v})

    @app.get("/logout")
    def logout(request:Request, response: Response):       
        prj.Session().kill(request,response)
        return RedirectResponse("/login")

    app.include_router(API(prj))

    return app

APP=create()

