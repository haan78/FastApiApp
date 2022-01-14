from pymongo.cursor import Cursor
from project import Project

project = Project()

cur = project.data.colletion("uye").find({ "active":True },limit = 1)
@project.data.assignCurFunc()
def method1(doc):
    return doc

print( project.data.toList(cur) )
