import os.path

from fastapi import Request
from fastapi.responses import JSONResponse

import jwt
import re


class FastLib:
    jwtkey = 'dfndsfkldjs--kjrherlkjrhlewrjhwelkrjhewrl'
    jwtalgo = 'HS256'
    identityheadername = 'IDENTITY'

    def __init__(self,jwtkey = None) -> None:
        self.jwtkey = jwtkey

    def identity(self, request: Request):
        header = request.headers.get(self.identityheadername)
        if header is not None:
            return jwt.decode(header, self.jwtkey, algorithms=[self.jwtalgo], options={'require': ["exp"]})
        else:
            raise Exception('No identity has been sent')

    def response(self, data, meta=None):
        if isinstance(data, Exception) or isinstance(data, TypeError):
            return JSONResponse(
                status_code=200,
                content={
                    "success": False,
                    "data": {
                        "text": str(data),
                        "type": type(data).__name__
                    },
                    "meta": None
                }
            )
        else:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "data": data,
                    "meta": meta
                }
            )

    def html(self, file: str, data: dict):
        if os.path.isfile(file):
            f = open(file)
            content = f.read()
            for key in data:
                v = str(data[key])
                pet = "{{\s*" + key + "\s*}}"
                content = re.sub(string=content, repl=v, pattern=pet)

            return content
        else:
            raise Exception("HTML Template not found")
