from pydantic import BaseModel
from project import Project
from fastapi import Request, APIRouter, HTTPException
from lib.FastApiBarisJSONRoute import FastApiBarisJSONRoute

def API(prj:Project) -> APIRouter:
    class ApiRouterControler(FastApiBarisJSONRoute):
        def auth(self, request: Request):
            super().auth(request)
            # raise Exception("You Shall not pass")


    apirouter = APIRouter(prefix="/api", route_class=ApiRouterControler)

    @apirouter.get("/")
    def test2():
        return { "a":5 }

    @apirouter.get("/hata")
    def hata():
        raise Exception("Hattttttt")

    @apirouter.get("/hata2")
    def hata2():
        raise HTTPException(status_code=422, detail="Hadi canım")

    return apirouter
