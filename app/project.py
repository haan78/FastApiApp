from lib.DotEnv import ReadDotEnvFile
from lib.FastLib import FastLib
from FastSession.FastMongoSession import FastMongoSession
from lib.Mongo import Mongo

class Project:
    data: Mongo = None
    session: FastMongoSession = None
    lib: FastLib = None
    port: int

    def __init__(self) -> None:
        settings = ReadDotEnvFile(".env", ["JWTKEY", "DBCONN", "DBNAME","PORT","SESSIONTIME"])
        self.data = Mongo(settings["DBCONN"],settings["DBNAME"])
        self.lib = FastLib(settings["JWTKEY"])
        self.session = FastMongoSession( self.data.colletion("session"),timeout=int(settings["SESSIONTIME"]) )
        self.port = int( settings["PORT"] )