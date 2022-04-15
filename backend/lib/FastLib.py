import os.path
from fastapi import Request
from fastapi.responses import HTMLResponse
import jwt
import re
import datetime
from collections.abc import Iterable
import base64


class FastLib:

    @staticmethod
    def get_jwt_identity(request: Request, jwtkey: str,
                         jwtalgo: str = 'HS256', header: str = 'IDENTITY'):
        header = request.headers.get(header)
        if header is not None:
            return jwt.decode(header, jwtkey, algorithms=[
                              jwtalgo], options={'require': ["exp"]})
        else:
            raise None

    @staticmethod
    def toJS(data,useBase64:bool=False) -> str:
        def _toJS(data) -> str:
            s = ""
            if type(data) is str:
                s += "\"{}\"".format(data)
            elif type(data) is dict:
                s += "{"
                i = 0
                for key, value in data.items():
                    v = FastLib.toJS(value)
                    s += "," if i > 0 else ""
                    s += "\"{}\":{}".format(key, v)
                    i += 1
                s += "}"
            elif isinstance(data, Iterable):
                s += "["
                i = 0
                for value in data:
                    s += "," if i > 0 else ""
                    s += FastLib.toJS(value)
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
        if useBase64:
            bytes = strval.encode("UTF-8")
            b64Bytes = base64.b64encode(bytes)
            return b64Bytes.decode('ascii')
        else:
            return strval


    @staticmethod
    def template(file: str, data: dict,cookies:dict = {},max_cookie_age:int=600):

        if os.path.isfile(file):
            f = open(file)
            html = f.read()
            for key in data:                
                v = str(data[key])                    
                pet = "{{\\s*" + key + "\\s*}}"
                html = re.sub(string=html, repl=v, pattern=pet)
            response = HTMLResponse(status_code=200, content=html)
            for k,v in cookies.items():
                response.set_cookie(key=k,value=v,max_age=max_cookie_age)
            return response
        else:
            raise Exception("HTML Template not found")
