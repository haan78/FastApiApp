from project import Project
from fastapi import Request, APIRouter, HTTPException
from lib.FastApiBarisJSONRoute import FastApiBarisJSONRoute

from lib.Mongo import Mongo
from pymongo import MongoClient
from bson.objectid import ObjectId

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

    @apirouter.get("/db1")
    def db1():
        m:Mongo = Mongo("mongodb://root:12345@mongodb","dojo")
        mc:MongoClient = m.link()
        cur = mc.get_database("dojo").get_collection("gelirgider").find({
            "_id":ObjectId("61caf5285451957d2c688849")
        })
        
        v = m.toList(cur)
        print(v)

        return v

    return apirouter
