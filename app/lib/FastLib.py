import os.path
from fastapi import Request
from fastapi.responses import HTMLResponse
import jwt
import re


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
    def template(file: str, data: dict):
        if os.path.isfile(file):
            f = open(file)
            html = f.read()
            for key in data:
                v = str(data[key])
                pet = "{{\\s*" + key + "\\s*}}"
                html = re.sub(string=html, repl=v, pattern=pet)

            return HTMLResponse(status_code=200, content=html)
        else:            
            raise Exception("HTML Template not found")
