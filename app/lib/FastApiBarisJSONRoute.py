from fastapi import Request,Response,HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRoute
from typing import Callable

class FastApiBarisJSONRoute(APIRoute):

    def json_response(self, data):
        if isinstance(data,HTTPException):
            return JSONResponse(
                status_code=200,
                content={
                    "success": False,
                    "data": {
                        "detail":data.detail,
                        "status":data.status_code,
                        "type": type(data).__name__
                    },
                    "meta": self.meta()
                }
            )

        elif isinstance(data, Exception) or isinstance(data, TypeError):
            return JSONResponse(
                status_code=200,
                content={
                    "success": False,
                    "data": {
                        "detail": str(data),
                        "type": type(data).__name__
                    },
                    "meta": self.meta()
                }
            )
        else:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "data": jsonable_encoder(data),
                    "meta": self.meta()
                }
            )

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:            
            try:
                self.auth(Request)
                result = await original_route_handler(request)
                return self.json_response(result.body)
            except Exception as ex:
                return self.json_response(ex)

        return custom_route_handler
    
    def auth(self,request: Request):
        pass

    def meta(self):
        pass