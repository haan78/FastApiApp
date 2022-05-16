from pymongo import MongoClient
from pymongo import cursor
from pymongo.database import Database
from pymongo.collation import Collation
from pymongo.cursor import Cursor

client : MongoClient = MongoClient('mongodb://root:12345@mongodb/dojo?authSource=admin')
db : Database = client.get_database()
print( str(db) )
print(db.list_collection_names())


