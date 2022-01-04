from lib.DotEnv import ReadDotEnvFile
from lib.FastLib import FastLib
from FastSession.FastMongoSession import FastMongoSession
from data import Data

class Project:
    data: Data = None
    session: FastMongoSession = None
    lib: FastLib = None
    port: int

    def __init__(self) -> None:
        settings = ReadDotEnvFile(".env", ["JWTKEY", "DBCONN", "DBNAME","PORT"])
        self.data = Data(settings["DBCONN"],settings["DBNAME"])
        self.lib = FastLib(settings["JWTKEY"])
        self.session = FastMongoSession( self.data.colletion("session") )
        self.port = int( settings["PORT"] )