from lib.ENV import ENV
import logging
import time
import os

def applogger(name:str)->logging.Logger:
    logfolder:str = "/var/log/app"
    if not os.path.exists(logfolder):
        os.makedirs(logfolder)
    fh = logging.FileHandler(filename="{}/{}-{}.log".format(logfolder,name,time.strftime("%y%m%d%H%M%S")),mode="w")
    fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger = logging.getLogger(name=name)
    logger.addHandler(fh)
    return logger

class Settings:
    DBCONN: str
    SESSIONTIME: int
    JWTKEY: str

    def __init__(self) -> None:
        self.DBCONN: str = ENV("DBCONN", str)        
        self.SESSIONTIME: int = ENV("SESSIONTIME", int, False, 500)
        self.JWTKEY: str = ENV("JWTKEY", str)
