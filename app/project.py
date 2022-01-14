import uvicorn
from fastapi import FastAPI
from lib.FastLib import FastLib
from FastSession.FastMongoSession import FastMongoSession
from lib.Mongo import Mongo
from dotenv import load_dotenv
from pathlib import Path
import os

class Project:
    data: Mongo = None
    session: FastMongoSession = None
    lib: FastLib = None
    port: int

    settings:dict = {
        "JWTKEY":None,
        "DBCONN":None,
        "DBNAME":None,
        "PORT":None,
        "SESSIONTIME":None
    }

    def __init__(self,envfile = ".env") -> None:
        self._loadEnv(envfile=envfile)
        print(self.settings)
        self.data = Mongo(self.settings["DBCONN"],self.settings["DBNAME"])
        self.lib = FastLib(self.settings["JWTKEY"])
        self.session = FastMongoSession( self.data.colletion("session"),timeout=int(self.settings["SESSIONTIME"]) )
        self.port = int( self.settings["PORT"] )

    def _loadEnv(self, envfile:str):
        dotenv_path = Path(envfile)
        load_dotenv(dotenv_path=dotenv_path)

        for k in self.settings.keys():
            v = os.getenv(k)
            if v is None:
                raise Exception('ENV '+k+" dose not exist")
            else:
                self.settings[k] = v

    @staticmethod
    def run(app: FastAPI, port:int = 8080):
        uvicorn.run(app, host="0.0.0.0", port=port)
