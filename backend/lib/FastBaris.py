from functools import wraps
import os
import typing
from fastapi import BackgroundTasks
from fastapi.responses import HTMLResponse
import jwt

import datetime
from collections.abc import Iterable
import base64
import re

from fastapi import Request,Response,HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRoute
from typing import Callable
import sys
import traceback
import json

class FastBarisBaseData:

    max_age:int
    base64text:str
    cookie_name:str

    def __init__(self,data :dict,cookie_name:str = "DATA64",max_age:int = 600) -> None:
        self.max_age = max_age
        self.cookie_name = cookie_name
        self.base64text = self.base64json(data)        
        
    def base64json(self, data) -> str:
        def _toJS(data) -> str:
            s = ""
            if type(data) is str:
                s += "\"{}\"".format(data)
            elif type(data) is dict:
                s += "{"
                i = 0
                for key, value in data.items():
                    v = _toJS(value)
                    s += "," if i > 0 else ""
                    s += "\"{}\":{}".format(key, v)
                    i += 1
                s += "}"
            elif isinstance(data, Iterable):
                s += "["
                i = 0
                for value in data:
                    s += "," if i > 0 else ""
                    s += _toJS(value)
                    i += 1
                s += "]"
            elif type(data) is datetime.datetime:
                s += "\""+data.isoformat()+"\""
            elif type(data) is datetime.date:
                s += "\""+data.strftime("%Y-%m-%d")+"\""
            elif type(data) is bool:
                s += "true" if data else "false"
            else:
                s += str(data)
            return s
        strval = _toJS(data)

        bytes = strval.encode("UTF-8")
        b64Bytes = base64.b64encode(bytes)
        return b64Bytes.decode('ascii')


class FastBarisHTMLResponse(HTMLResponse):
    def __init__(self, content: typing.Any = None, status_code: int = 200, headers: dict = None, media_type: str = None, background: BackgroundTasks = None, baseData : FastBarisBaseData =None) -> None:
        super().__init__(content, status_code, headers, media_type, background)
        if baseData is not None:            
            self.set_cookie(key=baseData.cookie_name,value=baseData.base64text,max_age=baseData.max_age)

def FastBarisFileContent(file:str,replace:dict = {}):
    if os.path.isfile(file):
        f = open(file)
        html = f.read()
        for key in replace:                
            v = str(replace[key])                    
            pet = "{{\\s*" + key + "\\s*}}"
            html = re.sub(string=html, repl=v, pattern=pet)
        return html
    else:
        raise Exception("Template file not found")


def FastBarisJWTRead(request: Request, jwtkey: str,jwtalgo: str = 'HS256', header: str = 'IDENTITY'):
    headerData = request.headers.get(header)
    if headerData is not None:
        return jwt.decode(headerData, jwtkey, algorithms=[jwtalgo], options={'require': ["exp"]})
    else:
        raise None

class FastBarisJSONRoute(APIRoute):

    class AuthExection(Exception):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)

    __auth_method__:Callable[[Request,Callable],None] = None

    @staticmethod
    def __auth_abort__(message:str)->None:
        raise FastBarisJSONRoute.AuthExection(message)

    def json_response(self, data):
        code = 0
        jbody = None
        if isinstance(data,HTTPException):
            code = data.status_code
            jbody = json.dumps({
                    "detail":data.detail,
                    "type": type(data).__name__
            })
        elif isinstance(data,FastBarisJSONRoute.AuthExection):
            code = 401
            jbody = json.dumps({
                    "detail":str(data)                    
            })
        elif isinstance(data, Exception) or isinstance(data, TypeError):
            code = 500
            jbody = json.dumps({
                    "detail":str(data),
                    "type": type(data).__name__
            })
        else:
            code = 200
            jbody = jsonable_encoder(data)
        
        return Response(content=jbody,media_type="application/json", status_code=code)

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:            
            try:
                if self.__auth_method__ is not None:
                    self.__class__.__auth_method__(request,self.__class__.__auth_abort__)
                
                result = await original_route_handler(request)
                return self.json_response(result.body)
                ##return result.body
            except Exception as ex:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traces = traceback.extract_tb(exc_traceback)
                el = traceback.format_list(traces)
                print(str(ex))
                for e in el:
                    print("----------------")
                    print(e)
                
                return self.json_response(ex)

        return custom_route_handler

    @classmethod
    def auth(cls)->Callable:        
        def wrapper(authMethod:Callable[[Request,Callable],None] )->None:
            cls.__auth_method__ = authMethod
        return wrapper

    
            
