from typing import Callable, List
from pymongo import MongoClient
from pymongo import cursor
from pymongo.database import Database
from pymongo.collation import Collation
from pymongo.cursor import Cursor
from datetime import datetime
from datetime import date
from bson.objectid import ObjectId
from dateutil import parser

class Mongo():
    _connstr: str = None
    _dbname: str = None
    _conn: MongoClient = None
    _cursorFnc: Callable = None
    TIMESTAMPFORMAT : str = "%Y-%m-%dT%H:%M:%S.000Z"
    DATEFORMAT : str = "%Y-%m-%dT00:00:00.000Z"

    def __init__(self,connstr: str, dbname: str):
        self._connstr = connstr
        self._dbname = dbname

    def link(self, new:bool = False) -> MongoClient:
        if new or self._conn is None:
            self._conn = MongoClient(self._connstr)
        return self._conn

    def db(self,dbname: str = None) -> Database:
        if dbname is None:
            return self.link().get_database(self._dbname)
        else:
            return self.link().get_database(self,dbname)
    
    def ISOToDate(self,iso:str)->date:
        dt:datetime = parser.isoparse(iso)
        return date(dt.year,dt.month,dt.day)

    def ISOtoDateTime(self,iso:str)->datetime:
        return parser.isoparse(iso)

    
    def colletion(self, name: str, dbname: str = None) -> Collation:
        return self.db(dbname).get_collection(name)

    def _renderDocumnet(self, doc ):
        def render( data ):
            d = data
            t = type(d)
            if t is dict:
                for k in d:
                    d[k] = render(d[k])
            elif (t is list) or (t is tuple):
                for i in range(len(d)):
                    d[i] = render(d[i])
            elif t is datetime:
                d = d.strftime(self.TIMESTAMPFORMAT)
            elif t is date:
                d = d.strftime(self.DATEFORMAT)
            elif t is ObjectId:
                d = str(d)
            return d

        return render( doc )

    def assignCurFunc(self) -> Callable:
        def setfnc(fnc):            
            self._cursorFnc = fnc
        return setfnc
    
    def freeCurFnc(self):
        self._cursorFnc = None      

    def toList(self, cur:Cursor, freeCurFnc:bool = True, renderDoc:bool = True ) -> list:
        l = []
        for doc in cur:
            if renderDoc:
                doc = self._renderDocumnet(doc)

            if self._cursorFnc is None:
                l.append( doc )
            else:
                l.append( self._cursorFnc( doc ) )
        
        if freeCurFnc:
            self.freeCurFnc()

        return l
