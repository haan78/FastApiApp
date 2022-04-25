from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
import random

from lib.FastLib import FastLib
from project import Project

from api import API
from auth import AUTH

def Router():
    prj = Project("/etc/app.env")
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="/static"), name="static")
    
    def main(request:Request):
        s = prj.Session().read(request=request)
        if s is not None:
            v = FastLib.toJS(s,True)
            return FastLib.template("template.html",{
                "rnd":"rnd"+str(random.randint(1,1000)).rjust(4,"0"),
                "module":"main"          
            },{"BEDATA":v})
        else:
            return RedirectResponse("/auth/login/hata",status_code=302)

    @app.get("/",response_class=HTMLResponse)
    def login(request:Request):
        return main(request=request)

    @app.post("/",response_class=HTMLResponse)
    def login(request:Request):
        return main(request=request)

    @app.get("/err")
    def err():
        raise "HATA"


    app.include_router(API(prj))
    app.include_router(AUTH(prj))

    return app

