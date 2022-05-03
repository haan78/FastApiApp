from typing import Callable
from fastapi import Request, APIRouter, HTTPException
from lib.FastBaris import FastBarisJSONRoute,FastBarisJWTRead
from bson.objectid import ObjectId
from FastSession.FastSessionAbstract import FastSessionAbstract
from dbhelper import DBHelper

def API(session:FastSessionAbstract,db:DBHelper) -> APIRouter:

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
        raise HTTPException(status_code=422, detail="Hadi canim")

    @apirouter.get("/db1")
    def db1():
        cur = db.mongo.db().get_collection("gelirgider").find({
            "_id":ObjectId("61caf5285451957d2c688849")
        })
        
        v = db.mongo.toList(cur)
        #print(v)

        return v

    return apirouter
