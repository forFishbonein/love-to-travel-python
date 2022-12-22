#连接用户数据库
import pymysql
# from pymongo import MongoClient
import numpy as np
import gensim
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
# import DataProcess
# import vecWord
# from calculateSimilar import calculateSimilarIterm4User,calculateSimilarUser4Iterm
import sys
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
    list_show=[]
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        tup=cursor.fetchall()
        # print(len(tup))
        for item in tup:
            list_res.append([str(item[0]),str(item[0])])
            list_show.append([str(item[0]),item[1],item[3],item[4],item[14]])

    except pymysql.Error as e:
        print('连接失败')
    # with open('sceneryId.txt', 'w',encoding='UTF-8') as outf:
    #     for i in range(1,len(list_res)):
    #         outf.write(list_res[i][0])
    #         outf.write('\n')
    itemId=pd.DataFrame(list_res[1:10750],columns=list_res[0])
    return itemId,list_show




def vecUser_train():
    model = gensim.models.Word2Vec.load(r"D:\git\love-to-travel\love-to-travel-cloud\travelservice\src\main\resources\static\tensorflowRecommendation\data\userid.word2vec")
    file=open(r'D:\git\love-to-travel\love-to-travel-cloud\travelservice\src\main\resources\static\tensorflowRecommendation\data\userid.txt')
    user_data= file.read().splitlines()

    EmbedingUser=[['0','1','2','3','4','5','6','7','8','9']]
    for item in user_data:
        EmbedingUser.append(model.wv.get_vector(item))
    EmbedingUser=pd.DataFrame(EmbedingUser)
    return EmbedingUser

def vecSCenery_train():
    model = gensim.models.Word2Vec.load(r"D:\git\love-to-travel\love-to-travel-cloud\travelservice\src\main\resources\static\tensorflowRecommendation\data\sceneryId.word2vec")
    file=open(r'D:\git\love-to-travel\love-to-travel-cloud\travelservice\src\main\resources\static\tensorflowRecommendation\data\sceneryId.txt')
    scenery_data= file.read().splitlines()

    EmbedingScenery=[['0','1','2','3','4','5','6','7','8','9']]
    for item in scenery_data:
        EmbedingScenery.append(model.wv.get_vector(item))
    EmbedingScenery=pd.DataFrame(EmbedingScenery)
    return EmbedingScenery

# print(vecUser_train())
# print(vecSCenery_train())



EmbedingUser=vecUser_train()
EmbedingIterm=vecSCenery_train()
iterm2Id=SceneryData()[0]

myUser2Id=UserData()



def getUseEmbeding(userid):
    return np.array(EmbedingUser.loc[userid])

def getItermEmbeding(itermid):
    return np.array(EmbedingIterm.loc[itermid])

def calculateSimilarIterm4User(userNo,num=15):
    '''
    :param userNo:
    :param num:
    :return: recomment iterms list for a special user
    '''
    userid = getUserId(userNo)
    userEmbeding = getUseEmbeding(userid)
    itermEmbeding= np.array(EmbedingIterm)
    # print(itermEmbeding)
    similarList= [cosine_similarity(X=[userEmbeding],Y=[it]) for it in itermEmbeding]
    # transfer to 1 Dimention
    similarList = np.array(similarList).squeeze()
    # print(similarList)
    sortListIndex = np.argsort(similarList)  # list从小到大排序，输出原始list的index
    # print(sortListIndex)
    sortListIndexNum = sortListIndex[-num:]  # 取前num个iterm
    sortListIndexNum = sortListIndexNum[ : : -1]  #表示list反转，每次前进-1，从头到尾
    itermNoList = []
    for i in sortListIndexNum:
        itermNoList.append(getItermNo(i))

    return itermNoList

def calculateSimilarUser4Iterm(itermNo,num=15):
    '''
    :param itermNo:
    :param num:
    :return: recomment users list for a special iterm
    '''
    itermid = getItermId(itermNo)
    itermEmbeding = getItermEmbeding(itermid)
    userEmbeding = np.array(EmbedingUser)
    # print(userEmbeding)
    similarList = [cosine_similarity(X=[itermEmbeding],Y=[ut]) for ut in userEmbeding]
    # transfer to 1 Dimention
    similarList = np.array(similarList).squeeze()
    # print(similarList)
    sortListIndex = np.argsort(similarList)  # list从小到大排序，输出原始list的index
    # print(sortListIndex)
    sortListIndexNum = sortListIndex[-num:]  # 取前num个iterm
    sortListIndexNum = sortListIndexNum[ : : -1] #表示list反转，每次前进-1，从头到尾
    userNoList = []
    for i in sortListIndexNum:
        userNoList.append(getUserNo(i))

    return userNoList

def getUserNo(userid):
    for i in range(len(myUser2Id)):
        if int(myUser2Id['用户码'][i])==userid:
            return myUser2Id['用户码'][i]
    return None

def getUserId(userNo):
    for i in range(len(myUser2Id)):
        if myUser2Id['用户码'][i]==userNo:
            return int(myUser2Id['用户码'][i])
    return None

def getItermNo(itermid):
    for i in range(len(iterm2Id)):
        if int(iterm2Id['景区码'][i])==itermid:
            return iterm2Id['景区码'][i]
    return None

def getItermId(itermNo):
    for i in range(len(iterm2Id)):
        if iterm2Id['景区码'][i]==itermNo:
            return int(iterm2Id['景区码'][i])
    return None


# if __name__ == "__main__":
#     # print(getUseEmbeding(0))
#     # print(getItermEmbeding(0))
#     # print(getUserNo(0))
#
#     itermNoList = calculateSimilarIterm4User('12',num=10)
#     print(itermNoList)
#     userNoList = calculateSimilarUser4Iterm('456',num=10)
#     print(userNoList)
#     print(" test is done ")


def SceneryRec(usrNo):

    res_show=[]
    res = calculateSimilarIterm4User(usrNo,num=15)
    list_show=SceneryData()[1]

    res = list(set(res))
    for item in res:
        if item==None:
            res.remove(item)
    # print(res)

    # for i in range(len(res)):
    #     item=str(res[i])
    #
    #     res_show.append(item)
    res_ = res[:6]
    # res_str = ",".join(res_)
    # print(res_str)

    # str=
    for i in range(len(res_)):
        for j in range(len(list_show)):
            if res_[i]==list_show[j][0]:
                res_show.append(list_show[j])
    # print(res_show)

    return res_show

def UserRec(itermNo):
    res_show=[]
    res = calculateSimilarUser4Iterm(itermNo,num=15)
    res = list(set(res))
    for item in res:
        if item==None:
            res.remove(item)
    # print(res)

    for i in range(len(res)):
        item=str(res[i])

        res_show.append(item)
    res_ = res_show[:9]
    res_str = ",".join(res_)

    return res_str



def getJson(usrNo):
    arr=SceneryRec(usrNo)

    arrSce=np.array(arr)
    # print(arrSce)
    x1list=arrSce[:,0]
    x2list=arrSce[:,1]
    x3list=arrSce[:,2]
    x4list=arrSce[:,3]
    x5list=arrSce[:,4]
    res=[]
    for i in range(len(x1list)):
        data={'id':x1list[i],'name':x2list[i],'score':x3list[i],'ticket':x4list[i],'url':x5list[i]}
        res.append(data)
    # msg="内存溢出"
    resDict={"code":0,"msg":"","data":res}
    # print(resDict)
    return resDict

        # UserRec(itermNo)

# def HotCityData():
#     conn = get_conn()
#     sql = "select * from city"
#     try:
#         cursor = conn.cursor()
#         cursor.execute(sql)
#         list1=list(cursor.fetchall())
#     except pymysql.Error as e:
#         print('连接失败')

def writein(n,strW):

    conn = get_conn1()
    sql = "select * from user_scenery"
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        list1=list(cursor.fetchall())
    except pymysql.Error as e:
        print('连接失败')
    #     list_resf=[]
    #     print(list1)
    #     list1=list(query_data(sql))
    sqlInsert="insert user_scenery(user_id,scenery_id) value(%s,%s)"
    value = (n,strW)
    print(value)
    try:
        cursor.execute(sqlInsert,value)
        conn.commit()
    finally:
        conn.close

def writeSce(n,strW):

    conn = get_conn1()
    sql = "select * from scenery_user"
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        list1=list(cursor.fetchall())
    except pymysql.Error as e:
        print('连接失败')
    #     list_resf=[]
    #     print(list1)
    #     list1=list(query_data(sql))
    sqlInsert="insert scenery_user(scenery_id,user_id) value(%s,%s)"
    value = (n,strW)
    print(value)
    try:
        cursor.execute(sqlInsert,value)
        conn.commit()
    finally:
        conn.close



# if __name__ == "__main__":
    # sceneryData= SceneryData()[0]
    # # print(userData)
    # # print(SceneryRec(usrNo='2'))
    # for item in (sceneryData['景区码'][1275:10750]):
    #     userRelation=UserRec(item)
    #     # print(item)
    #     # print(userRelation)
    #     print(item)
    #     writeSce(item,userRelation)

    # getJson(usrNo='1')