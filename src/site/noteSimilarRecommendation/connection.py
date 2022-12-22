import pandas as pd
import numpy as np
import thulac
import csv
from pymongo import MongoClient

def getId():
    client = MongoClient('mongodb://travelservice:W6xDFpnZb86hH7mj@47.98.138.0:27017/travelservice?')
    ##指定要操作的数据库，test
    db = client.travelservice
    ##限定数据库表，plan
    mycol = db["note"]
    # mycol
    note = mycol.distinct( "_id")
    # print(note)
    noteId=[]
    for item in note:
        noteId.append(str(item))
    # print(noteId)
    return noteId
# print(getId())