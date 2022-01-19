from fastapi import Request, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel
import random
from project import Project

def router(project:Project):
    app = project.getApp()
    class testObj(BaseModel):
        test: str

    @app.get("/", response_class=HTMLResponse)
    async def index_html():
        return project.lib.html("template.html", {"module": "main", "rndint": "rnd"+str(random.randint(1, 1000))})
    
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
    def error(exc: Exception):
        return project.lib.response(exc)

    @app.post("/identity")
    def identity(test: testObj, request: Request):
        id = project.lib.identity(request)
        return {
            "test": test,
            "id": id
        }

    @app.post("/identity2")
    async def identity2(request: Request):
        id = project.lib.identity(request)
        jd = await request.json()
        return {
            "jData": jd,
            "id": id
        }

    @app.get("/write")
    def setcoo(response: Response):    
        project.session.write(response, {
            "name": "Ali Barış Öztürk"
        })
        return "Yazıldı"

    @app.get("/read")
    async def read_items(request: Request):
        v = project.session.read(request)
        return {"ads_id": v}

    @app.get("/kill")
    async def kill(response: Response):
        project.session.kill(response)
        return "silindi"

    @app.get("/uyeler")
    def uyeler():
        return project.session.response(project.data.toList( project.data.colletion("uye").find({"active":True}) ))

    @app.get("/items/{item_id}")
    def read_root(item_id: str, request: Request):
        return {"client_host": request.client.host, "item_id": item_id}