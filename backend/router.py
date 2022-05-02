from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles

from project import Project
from lib.FastBaris import FastBarisFileContent,FastBarisHTMLResponse,FastBarisBaseData

from api import API
from auth import AUTH

def CreateRouter():
    prj:Project = Project()
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="/static"), name="static")
    
    def main2(request:Request):
        s = prj.Session().read(request=request)
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

    app.include_router(API(prj))
    app.include_router(AUTH(prj))

    return app


ROUTER = CreateRouter()

