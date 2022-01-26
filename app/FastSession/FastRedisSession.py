from fastapi import Request, Response
from FastSession.FastSessionAbstract import FastSessionAbstract
import redis
import uuid
import json


class FastRedisSession(FastSessionAbstract):
    _conn: redis.Redis = None

    def __init__(self, connection: redis.Redis, timeout: int = 900):
        super(FastRedisSession, self).__init__(timeout)
        self._conn = connection

    def __del__(self):
        self._conn.close()

    def write(self, response: Response, data) -> str:
        _id = "fastapi_"+str(uuid.uuid4())
        jdata = json.dumps(data)
        self._conn.set(_id, jdata, ex=self._timeout)
        ##response.set_cookie(key=self._sessionName, value=_id, max_age=self._timeout)
        response.set_cookie(key=self._sessionName, value=_id, max_age=3600*24) ##Tum gun
        self._lastSessionId = _id
        return _id

    def read(self, request: Request):
        _id = request.cookies.get(self._sessionName)
        print(_id)
        if _id is not None:
            res = self._conn.get(name=_id)
            v = self._conn.expire(name=_id, time=self._timeout)
            ##print((self._timeout,_id,v))
            
            if res is not None:
                data = json.loads(res)
                return data
            else:
                return None
        else:
            return None

    def kill(self, request:Request, response: Response):
        super(FastRedisSession, self).kill(request,response)
        if self._lastSessionId is not None:
            self._conn.delete(self._lastSessionId)
            self._lastSessionId = None
