from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from FastSession.FastSqLiteSession import FastSqLiteSession
from lib.FastBaris import FastBarisFileContent,FastBarisHTMLResponse,FastBarisBaseData


from settings import Settings
from dbhelper import DBHelper

from api import API
from auth import AUTH

def CreateRouter():
    sett:Settings = Settings() 
    app = FastAPI()
    session:FastSqLiteSession = FastSqLiteSession("/tmp/session.db")

    app.mount("/static", StaticFiles(directory="/app/static"), name="static")
    
    def main2(request:Request):
        s = session.read(request=request)
        if s is not None:
            return FastBarisHTMLResponse(baseData=FastBarisBaseData(data=s),content=FastBarisFileContent("template.html"))
        else:
            return RedirectResponse("/auth/login",status_code=302)

    @app.get("/",response_class=HTMLResponse)
    def main(request:Request):
        return main2(request=request)

    @app.post("/",response_class=HTMLResponse)
    def main(request:Request):
        return main2(request=request)

    app.include_router(AUTH(sett,session))
    app.include_router(API(sett,session))

    return app


ROUTER = CreateRouter()

