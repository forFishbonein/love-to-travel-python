import sceneryClustering as sc
import pymysql
import pandas as pd
import numpy as np


def getData():
    conn = sc.get_conn()
    sql = "select * from scenery"
    list_res=[['id','评分','门票','城市adcode','聚类类别']]
    list_show=[]
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        tup=cursor.fetchall()
        # print(len(tup))
        for item in tup:
            list_res.append([str(item[0]),str(item[3]),str(item[4]),str(item[13]),str(item[19])])
            list_show.append([str(item[0]),item[1],item[3],item[4],item[14]])

    except pymysql.Error as e:
        print('连接失败')
    # with open('sceneryId.txt', 'w',encoding='UTF-8') as outf:
    #     for i in range(1,len(list_res)):
    #         outf.write(list_res[i][0])
    #         outf.write('\n')
    df=pd.DataFrame(list_res[1:7000],columns=list_res[0])
    return df,list_show

def Recommmendation(scan_list):
    #景区推荐:猜你喜欢,根据浏览记录推荐

    r,sce_list = getData()
    # scan_list=[3,4,10]
    # item=4
    list_res=[]
    for item in scan_list:
        type_list=[]
        for i in range(0,len(r['评分'])):
            # print(r['评分'])
            # print(type(item))
            # print(type(r['id'][i]))
            if i!=2102 and i!=2475  and  i!=5697  and i!=7455 and i!=7943 and i!=7944 and i!=8364 and i!=10119 and i!=10443 and item == int(r['id'][i]):
                # print(item)
                for k in range(0,len(r['评分'])):
                    if k!=2102 and k!=2475  and  k!=5697  and k!=7455 and k!=7943 and k!=7944 and k!=8364 and k!=10119 and k!=10443 and r['聚类类别'][i]==r['聚类类别'][k] and i!=k:
                        type_list.append(sce_list[k])
                        # print(type_list)
        #             print(r['聚类类别'][i])

        type_list = sorted(type_list, key=lambda row: row[1], reverse=True)[:3]
        for i in range(len(type_list)):
            if type_list[i] not in list_res:
                list_res.append(type_list[i])
    #     print(type_list)

    list_res= list_res[:6]
    # print(list_res)
    return list_res

def getJson(scan_list):
    arr=Recommmendation(scan_list)

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

if __name__ == '__main__':
    # Recommmendation()
    Recommmendation([3,5,10])
    # print(Recommmendation([3,4,10]))
