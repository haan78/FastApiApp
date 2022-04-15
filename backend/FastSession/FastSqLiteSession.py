from FastSession.FastSessionAbstract import FastSessionAbstract
import sqlite3
import json
from datetime import datetime,timedelta
from os.path import exists

class FastSqLiteSession(FastSessionAbstract):
    _conn:sqlite3.Connection = None
    TABLENAME:str = "FASTAPISESSION"

    def __init__(self,file:str,timeout: int = 900):
        super(FastSqLiteSession, self).__init__(timeout)
        self._conn = self.__dbGetConnection(file)
    
    def __del__(self):
        if self._conn is not None:
            self._conn.close()

    def __dbGetConnection(self,file:str)->sqlite3.Connection:
        createTable:bool = not exists(file)
        with sqlite3.connect(file,check_same_thread=False) as _conn:
            if createTable:
                cur = _conn.cursor()
                cur.execute('CREATE TABLE IF NOT EXISTS '+self.TABLENAME+' (id TEXT PRIMARY KEY, start_time TEXT, end_time TEXT, duration INTEGER, body TEXT  )')
                cur.execute('CREATE INDEX IF NOT EXISTS '+self.TABLENAME+'_ind_1 ON '+self.TABLENAME+' (end_time)')
                cur.close()
            return _conn

    def writeHandler(self, id: str, data) ->None:
        n = datetime.now()
        st = str(n)
        et = str(datetime.now() + timedelta(seconds=self._timeout) )
        jdata = json.dumps(data)
        cur = self._conn.cursor()
        cur.execute('INSERT INTO '+self.TABLENAME+' (id, start_time, end_time, duration, body) VALUES(?, ?, ?, ?, ?)',(id,st,et,self._timeout,jdata))
        cur.close()

    def readHandler(self, id:str):
        cur = self._conn.cursor()
        n = datetime.now()
        nowtime = str(n)
        cur.execute('DELETE FROM '+self.TABLENAME+' WHERE end_time < ?',(nowtime,))
        cur.execute('SELECT body,start_time,end_time FROM '+self.TABLENAME+' WHERE id = ? AND end_time >= ?',(id,nowtime))
        row = cur.fetchone()
        #print((row,type(row)))
        result = None
        if row is not None:
            et = str(n + timedelta(seconds=self._timeout) )
            cur.execute('UPDATE '+self.TABLENAME+' SET end_time = ? WHERE id = ?',(et,id))
            result = json.loads(row[0])
        cur.close()
        return result

    def killHandler(self, id:str):
        cur = self._conn.cursor()
        cur.execute('DELETE FROM '+self.TABLENAME+' WHERE id = ?',(id,))
        cur.close()
