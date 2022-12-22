#连接用户数据库
import pymysql
from pymongo import MongoClient
import pandas as pd
import numpy as np
#方式一

def get_conn():
    return pymysql.connect(
        host='47.98.138.0',
        port=3306,
        user='userservice',
        password='2x8R3WmbCzt6tcEd',
        database='userservice',
        charset='utf8'
    )

#连接景区数据库
def get_conn1():
    return pymysql.connect(
        host='47.98.138.0',
        port=3306,
        user='travelservice',
        password='2x8R3WmbCzt6tcEd',
        database='travelservice',
        charset='utf8'
    )

#获取用户数据
def UserData():
    conn = get_conn()
    sql = "select * from  user"
    list_res=[['用户码','用户编号']]
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        tup=cursor.fetchall()

        for item in tup:
            list_res.append([str(item[0]),str(item[0])])
    #         print(tup)
    except pymysql.Error as e:
        print('连接失败')
    # with open('userId.txt', 'w',encoding='UTF-8') as outf:
    #     for i in range(1,len(list_res)):
    #
    #         outf.write(list_res[i][0])
    #         outf.write('\n')
    myUser2Id=pd.DataFrame(list_res[1:6000],columns=list_res[0])
    return myUser2Id

#获取景区数据
def SceneryData():
    conn = get_conn1()
    sql = "select * from scenery"
    list_res=[['景区码','景区编号']]
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        tup=cursor.fetchall()
        print(len(tup))
        for item in tup:
            list_res.append([str(item[0]),str(item[0])])

    except pymysql.Error as e:
        print('连接失败')
    # with open('sceneryId.txt', 'w',encoding='UTF-8') as outf:
    #     for i in range(1,len(list_res)):
    #         outf.write(list_res[i][0])
    #         outf.write('\n')
    itemId=pd.DataFrame(list_res[1:10750],columns=list_res[0])
    return itemId


