
from dataclasses import dataclass


@dataclass
class settings:
    DBCONN:str = None
    DBNAME:str = None
    SESSIONTIME:int = 600
    JWTKEY:str = None

    @staticmethod
    def load(s):
        for i in s.__annotations__:
            if s.__annotations__[i] is str:
                print(i,type(i))
                s.__setattr__(i,"OK2")
            print(i,s.__dict__[i])


settings.load(settings())