from datetime import datetime
from dateutil import parser
import os
from typing import Any, Type

def ENV(name:str,type:Type = Any,required:bool = True,default:Any=None)->Any:
    v = os.getenv(name)
    #print("ENV ",name," ",v)
    if v is None:
        if required == True:
            raise Exception("ENV variable {} is required".format(name))
        else:
            return default
    elif type is Any:
        return v
    elif type is int:
        return int(v)
    elif type is float:
        return float(v)
    elif type is bool:
        return bool(v)
    elif type is str:
        return str(v)
    elif type is datetime:
        return parser(v)
    else:
        raise Exception("Unsupported ENV type")