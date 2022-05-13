from curses import echo
import uvicorn
from settings import Settings
from dbhelper import DBHelper

if __name__ == '__main__':
    sett = Settings()
    try:
        DBHelper.initdb(sett)
    except Exception as ex:
        print("Database installing error / "+str(ex))
        exit(1)
    except:
        print("Database installing error")
        exit(1)

    print("Port = {}, Mode = {}, Version = {}  ".format(sett.PORT,sett.APPMODE,sett.VERSION))

    reload:bool = True if sett.APPMODE == "development" else False
    level:str = "warning" if sett.APPMODE == "production" else "info"
    uvicorn.run("router:ROUTER", host="0.0.0.0", log_level=level, lifespan="off", reload=reload, port=sett.PORT )