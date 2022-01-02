import time
import jwt
import requests


# Data to be written
data = {
    "user": {
        "name": "Ali Barış Öztürk",
        "age": 21,
        "Place": "Patna",
        "Blood group": "O+"
    },
    "list":[1,2,3,{ "a":1,"b":2 }],
    "exp": time.time() + 60
}

result = jwt.encode(data, "dfklfglerekrjksdj102lslkwe94ldkklsd--*23ks", algorithm="HS256")

headers = {
    'IDENTITY': result
}
r = requests.post('http://localhost:8000/identity2', headers=headers, json={ "test": "Evet" })
print(r.json())
