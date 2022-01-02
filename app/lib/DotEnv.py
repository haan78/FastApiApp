import array
import os
from dotenv import load_dotenv
from pathlib import Path


def ReadDotEnvFile(file, titles: array):
    dotenv_path = Path(file)
    load_dotenv(dotenv_path=dotenv_path)
    result = {}
    for t in titles:
        v = os.getenv(t)
        if v is not None:
            result[t] = v
        else:
            raise Exception('ENV '+t+" dose not exist")

    return result
