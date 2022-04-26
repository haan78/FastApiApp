from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
import random

from lib.FastLib import FastLib
from project import Project

from api import API
from auth import AUTH

def CreateRouter():
    prj = Project("/etc/app.env")
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="/static"), name="static")
    
    def main2(request:Request):
        s = prj.Session().read(request=request)
        if s is not None:
            v = FastLib.toJS(s,True)
            return FastLib.template("template.html",{},{"BEDATA":v})
        else:
            return RedirectResponse("/auth/login",status_code=302)

    @app.get("/",response_class=HTMLResponse)
    def login(request:Request):
        return main2(request=request)

    @app.post("/",response_class=HTMLResponse)
    def login(request:Request):
        return main2(request=request)

    app.include_router(API(prj))
    app.include_router(AUTH(prj))

    return app

ROUTER=CreateRouter()
