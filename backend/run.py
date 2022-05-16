from curses import echo
import uvicorn
from settings import Settings
from dbhelper import DBHelper
from dotenv import load_dotenv
from pathlib import Path

if __name__ == '__main__':

    envf:str = "/app/.env"
    try:
        load_dotenv(dotenv_path=Path(envf))
    except:
        print("Application {} file can`t load".format(envf))
        exit(1)

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