from lib.Mongo import Mongo
from settings import Settings
from FastSession.FastMongoSession import FastMongoSession

class DBHelper:
    mongo:Mongo = None
    settings:Settings = None

    @staticmethod
    def initdb(sett:Settings)->None:
        print("INITDB")

    def __init__(self,sett:Settings) -> None:
        self.settings = sett
        self.mongo = Mongo(self.settings.DBCONN)
        print(self.mongo)

    def createSession(self)->FastMongoSession:
        col = self.mongo.db().get_collection("session")
        return FastMongoSession(collection=col,timeout=self.settings.SESSIONTIME)

