#景区聚类训练
import pandas as pd
import pymysql
# inputfile = r'D:\肖红娇\项目\爱旅游网站\原始数据\用户景区数据\scenerydetail.xlsx'
# df=pd.read_excel(inputfile)

def get_conn():
    return pymysql.connect(
        host='47.98.138.0',
        port=3306,
        user='travelservice',
        password='2x8R3WmbCzt6tcEd',
        database='travelservice',
        charset='utf8'
    )

def getData():
    conn = get_conn()
    sql = "select * from scenery"
    list_res=[['id','评分','门票','城市adcode']]
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        tup=cursor.fetchall()
        print(len(tup))
        for item in tup:
            list_res.append([str(item[0]),str(item[3]),str(item[4]),str(item[13])])

    except pymysql.Error as e:
        print('连接失败')
    # with open('sceneryId.txt', 'w',encoding='UTF-8') as outf:
    #     for i in range(1,len(list_res)):
    #         outf.write(list_res[i][0])
    #         outf.write('\n')
    df=pd.DataFrame(list_res[1:len(list_res)],columns=list_res[0])
    return df,list_res

def cluster():

    df,list_res = getData()
    df_data = pd.DataFrame(columns = ['id','评分','门票','城市adcode'],index = range(0,len(df['id'])))
    for i in range(1,len(df)):
        df_data.iloc[i,0] = float(df['id'][i])
        if list_res[i][1]=='--' or list_res[i][1] == None:
            df_data.iloc[i,1]=0
        else:
            df_data.iloc[i,1]= float(list_res[i][1])

        if list_res[i][2]=='-':
            df_data.iloc[i,2]=0
        else:
            df_data.iloc[i,2] =float(list_res[i][2])

        df_data.iloc[i,3] = list_res[i][3]
    print(df_data)
    df_data.dropna(inplace=True)
    return df_data

def modelTrain():
    df_data = cluster()
    # k = 500   #聚类的类别
    iteration = 600  #聚类最大循环次数
    # print(df_data)
    data_zs = 1.0*(df_data-df_data.mean())/df_data.std()   #数据标准化
    print(data_zs)
    #构建kmeans模型
    from sklearn.cluster import KMeans
    model = KMeans(n_clusters = 500, n_jobs = 5, max_iter = iteration, random_state = 1234) #分类为k，并发数为4
    model.fit(data_zs)

    #简单打印结果
    r1 = pd.Series(model.labels_).value_counts()  #统计各类别数目
    r2 = pd.DataFrame(model.cluster_centers_)  #找出聚类中心
    r = pd.concat([r2,r1],axis =1)  #得到聚类中心对应的类别下的数目

    r.columns = list(df_data.columns) + ['类别数目']    #重命名表头

    r = pd.concat([df_data, pd.Series(model.labels_,index =df_data.index)],axis =1)
    r.columns = list(df_data.columns) + ['聚类类别']
    return r

def writeSql():
    r = modelTrain()
    list_res = getData()[1]
    list_new = list_res[1:len(list_res)]
    conn = get_conn()
    cursor = conn.cursor()
    count=0
    for item in list_new:
        #     print(item)
        for sce in r['id']:

            if  float(item[0]) == sce:
                #
                sqlInsert="update scenery set cluster=%s where id=%s"
                cluster = r['聚类类别'][count]
                item = item[0]
                #                 print(value)
                try:
                    cursor.execute(sqlInsert,(cluster,item))
                    conn.commit()
                finally:
                    conn.close
        count+=1


