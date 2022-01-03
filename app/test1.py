from bson.objectid import ObjectId
from data import Data
from bson.json_util import dumps

database = Data("mongodb://root:12345@mongodb","dojo")

##l = list(database.colletion("uye").find({}))

##print( dumps(l) )
##print( database.toList(database.colletion("uye").find({"_id":ObjectId("61caf5285451957d2c688814")})) )
print( database.toList(database.colletion("uye").find({})) )

