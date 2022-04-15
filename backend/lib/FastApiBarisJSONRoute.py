from cgi import print_directory
from fastapi import Request,Response,HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRoute
from typing import Callable
import sys
import traceback
import json

class FastApiBarisJSONRoute(APIRoute):

    def json_response(self, data):
        code = 0
        jbody = None
        if isinstance(data,HTTPException):
            code = data.status_code
            jbody = json.dumps({
                    "detail":data.detail,
                    "type": type(data).__name__
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
                self.auth(request)
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
    
    def auth(self,request: Request):
        pass
