import pandas as pd
from pymongo import MongoClient
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

def labelData():
    # 城市数据
    df = pd.read_excel(r"D:\肖红娇\项目\爱旅游网站\原始数据\游记数据2.xlsx")
    df_city = pd.read_excel(r'D:\肖红娇\项目\爱旅游网站\原始数据\省份城市\cityData.xls')



    df['trip'].fillna("-", inplace=True)
    list_trip = list(set(df['trip']))
    list_res = []
    for item in list_trip:
        string = str(item).split("\xa0")
        for k in string:
            if k == '-':
                continue
            list_res.append(k)
    label_list = list(set(list_res))
    area_list = list(df_city['城市名称'])
    return label_list, area_list
# 游记数据

df_text = pd.read_excel(r'D:\肖红娇\项目\爱旅游网站\原始数据\全花销游记2.xlsx')

def getID():
    client = MongoClient('mongodb://travelservice:W6xDFpnZb86hH7mj@47.98.138.0:27017/travelservice?')
    ##指定要操作的数据库，test
    db = client.travelservice
    ##限定数据库表，plan
    mycol = db["_id"]
    list_id = mycol.distinct( "_id")
    list_nid = list_id[99:]
    return list_nid


def noteData():
    list_nid = getID()
    wenz_list = []
    label_list,area_list  = labelData()

    for i in range(len(df_text['title'])):
        area_idx=0
        label_idx=0
        for j in range(len(label_list)):
            string = df_text['trip'][i].split("\xa0")
            #         print(string[0])
            #         break

            if string[0] == label_list[j]:
                label_idx = j

        for k in range(len(area_list)):
            if df_text['city'][i] == area_list[k]:
                area_idx = k
        title = "游记_{}_{}_{}".format(i, area_list[area_idx], label_list[label_idx])

        wenz_list.append([list_nid[i], title, [area_idx, label_idx]])
    return wenz_list


# 用户数据

def userData():

    area_idx=0
    label_idx=0
    list_user = list(set(df_text['用户名称']))
    label_list = labelData()[0]
    area_list = labelData()[1]
    user_list = []
    for i in range(len(df_text['用户名称'])):
        for m in range(len(list_user)):
            if df_text['用户名称'][i] == list_user[m]:
                for j in range(len(label_list)):
                    string = df_text['trip'][i].split("\xa0")

                    if len(string) <= 1:
                        if string[0] == label_list[j]:
                            label_idx = j

                    else:
                        if string[1] == label_list[j]:
                            label_idx = j
                for k in range(len(area_list)):
                    if df_text['city'][i] == area_list[k]:
                        area_idx = k

                title = "用户_{}_{}_{}".format(i, area_list[area_idx], label_list[label_idx])

                user_list.append([i, title, [area_idx, label_idx]])
    return user_list

