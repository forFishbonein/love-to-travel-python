#景区聚类训练
import pandas as pd
# inputfile = r'D:\肖红娇\项目\爱旅游网站\原始数据\用户景区数据\scenerydetail.xlsx'
# df=pd.read_excel(inputfile)
import pymysql

def get_conn():
    return pymysql.connect(
        host='47.98.138.0',
        port=3306,
        user='travelservice',
        password='2x8R3WmbCzt6tcEd',
        database='travelservice',
        charset='utf8'
    )

def connectionSql():
    conn = get_conn()
    sql = "select * from scenery" #
    list_pre=[]
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        # print(cursor.fetchall())
        data=list(cursor.fetchall())
        for i in range(len(data)):
            list_pre.append(list(data[i]))

        return list_pre
    except pymysql.Error as e:
        print('连接失败')

def modelTrain():
    data_list=connectionSql()
    # print(data_list)

    df_data = pd.DataFrame(columns = ['id','评分','门票','城市adcode'],index = range(0,len(data_list)))
    for i in range(0,len(data_list)):
        df_data.iloc[i,0] = data_list[i][0]
        if data_list[i][3]=='--':
            df_data.iloc[i,1]=0
        else:
            df_data.iloc[i,1]= float(data_list[i][3])

        if data_list[i][4]=='-':
            df_data.iloc[i,2]=0
        else:
            df_data.iloc[i,2] =float(data_list[i][4])

        df_data.iloc[i,3] = data_list[i][12]

    df_data.dropna(inplace=True)
    # print(df_data)
    k = 10   #聚类的类别
    iteration = 400  #聚类最大循环次数
    print(1.0*(df_data-df_data.mean()))
    data_zs = 1.0*(df_data-df_data.mean())/df_data.std()   #数据标准化

    #构建kmeans模型
    from sklearn.cluster import KMeans
    model = KMeans(n_clusters = k, n_jobs = 4, max_iter = iteration, random_state = 1234) #分类为k，并发数为4
    model.fit(data_zs)

    #简单打印结果
    r1 = pd.Series(model.labels_).value_counts()  #统计各类别数目
    r2 = pd.DataFrame(model.cluster_centers_)  #找出聚类中心
    r = pd.concat([r2,r1],axis =1)  #得到聚类中心对应的类别下的数目

    r.columns = list(df_data.columns) + ['类别数目']    #重命名表头
    print(r)

    r = pd.concat([df_data, pd.Series(model.labels_,index =df_data.index)],axis =1)
    r.columns = list(df_data.columns) + ['聚类类别']
    return r


def sceneryRecommendation():
    #景区推荐:猜你喜欢,根据浏览记录推荐
    res=modelTrain()
    scan_list=[3,4,10]#浏览数据,测试
    # item=4
    list_res=[]
    for item in scan_list:
        type_list=[]
        for i in range(0,len(res['评分'])):
            if i!=2102 and i!=2475  and  i!=5697  and i!=7455 and i!=7943 and i!=7944 and i!=8364 and i!=10119 and i!=10443 and item == res['id'][i]:
                for k in range(0,len(res['评分'])):
                    if k!=2102 and k!=2475  and  k!=5697  and k!=7455 and k!=7943 and k!=7944 and k!=8364 and k!=10119 and k!=10443 and res['聚类类别'][i]==res['聚类类别'][k] and i!=k:
                        type_list.append([res['id'][k],res['评分'][k]])
                    #                     print(type_list)
        #             print(r['聚类类别'][i])

        type_list = sorted(type_list, key=lambda row: row[1], reverse=True)[:3]
        for item in type_list:
            list_res.append(item)
    #     print(type_list)

    list_res= sorted(list_res, key=lambda row: row[1], reverse=True)[:5]
    print(list_res)
    return list_res

def insertData():
    conn = get_conn()
    list_res=sceneryRecommendation()
    sql = "select * from scenery_related"
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        # list1=list(cursor.fetchall())
    except pymysql.Error as e:
        print('连接失败')

    # for i in list_res:
    #     sqlInsert="insert hot_city value(%s,%s)"
    #     value = i
    #     try:
    #         cursor.execute(sqlInsert,value)
    #         conn.commit()
    #     finally:
    #         print('连接失败')


print(modelTrain())