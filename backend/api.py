from typing import Callable
from project import Project
from fastapi import Request, APIRouter, HTTPException
from lib.FastBaris import FastBarisJSONRoute,FastBarisJWTRead
from lib.Mongo import Mongo
from pymongo import MongoClient
from bson.objectid import ObjectId

def API(prj:Project) -> APIRouter:

    @FastBarisJSONRoute.auth()
    def auth(request:Request,abort:Callable):
        ##abort("Auth Error2")
        pass
        
        

    apirouter = APIRouter(prefix="/api", route_class=FastBarisJSONRoute)

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
