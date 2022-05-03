from curses import echo
import sys
import uvicorn
from settings import Settings
from dbhelper import DBHelper
from dotenv import load_dotenv
from pathlib import Path

if __name__ == '__main__':
    reload = False
    port = 8001
    mode = "production"
    envf = "/etc/app.env"

    if len(sys.argv) > 1:        
        mode = str(sys.argv[1]).strip()   
            
    if len(sys.argv) > 2:
        port=int(sys.argv[2])
    
    if len(sys.argv) > 3:
        envf = str(sys.argv[3]).strip()

    try:
        load_dotenv(dotenv_path=Path(envf))
    except:
        print("Application {} file can`t load".format(envf))
        exit(1)

    try:
        DBHelper.initdb(Settings())
    except Exception as ex:
        print("Database installing error / "+str(ex))
        exit(1)
    except:
        print("Database installing error")
        exit(1)

    print("Port = {}, Mode = {}".format(port,mode))

    reload = True if mode == "development" else False
    level:str = "warning" if mode == "production" else "info"
    uvicorn.run("router:ROUTER", host="0.0.0.0", log_level=level, lifespan="off", reload=reload, port=port )