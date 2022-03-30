from urllib import response
from pydantic import BaseModel
from project import Project
from fastapi import Request,Response, APIRouter,Form
from fastapi.responses import HTMLResponse,RedirectResponse
from lib.FastLib import FastLib
from project import Project

def AUTH(prj:Project)->APIRouter:

    auth = APIRouter(prefix="/auth")
    @auth.get("/login",response_class=HTMLResponse)
    def login():
        return FastLib.template("templates/login.html",{ "status":"" })
    
    @auth.get("/login/{status}",response_class=HTMLResponse)
    def login(status:str):
        return FastLib.template("templates/login.html",{ "status":status })

    @auth.get("/logout",response_class=HTMLResponse)
    def logout(request:Request):        
        return prj.Session().killAndRedirect("/auth/login/bye",request)

    @auth.post("/form",response_class=RedirectResponse)
    async def form(identitiy:str = Form("Ali"),password:str = Form("Veli")):        
        if identitiy == "user" and password == "12345":            
            return prj.Session().writeAndRedirect("/",{
                "identitiy":"user"
            })            
        else:
            return RedirectResponse("/auth/login/wrong",status_code=302)
        

    @auth.get("/jwt/{ token }",response_class=RedirectResponse)
    def jwt(token:str):
        pass

    return auth