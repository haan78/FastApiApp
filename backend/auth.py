
from fastapi import Request, APIRouter,Form
from fastapi.responses import HTMLResponse,RedirectResponse
from lib.FastBaris import FastBarisHTMLResponse,FastBarisFileContent,FastBarisJWTRead
from FastSession.FastSessionAbstract import FastSessionAbstract
from dbhelper import DBHelper

def AUTH(session:FastSessionAbstract,db:DBHelper)->APIRouter:

    def loginpage():
        return FastBarisHTMLResponse( content=FastBarisFileContent("login.html") )

    auth = APIRouter(prefix="/auth")
    @auth.get("/login",response_class=HTMLResponse)
    def login():
        return loginpage()
    
    @auth.get("/login/{status}",response_class=HTMLResponse)
    def login(status:str):
        return loginpage()

    @auth.get("/logout",response_class=HTMLResponse)
    def logout(request:Request):        
        return session.killAndRedirect("/auth/login/bye",request)

    @auth.post("/form",response_class=RedirectResponse)
    async def form(identitiy:str = Form("Ali"),password:str = Form("Veli")):        
        if identitiy == "user" and password == "12345":            
            return session.writeAndRedirect("/",{
                "identitiy":"user"
            })            
        else:
            return RedirectResponse("/auth/login/wrong",status_code=302)
        

    return auth