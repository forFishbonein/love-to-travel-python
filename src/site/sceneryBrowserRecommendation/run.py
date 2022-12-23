#景区聚类训练
import pandas as pd
inputfile = r'D:\肖红娇\项目\爱旅游网站\原始数据\用户景区数据\scenerydetail.xlsx'
df=pd.read_excel(inputfile)
# df

# conn = get_conn()
# sql = "select * from similarity_note"
# try:
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     list1=list(cursor.fetchall())
# except pymysql.Error as e:
#     print('连接失败')
df_data = pd.DataFrame(columns = ['id','评分','门票','城市adcode'],index = range(0,len(df['中文名称'])))
for i in range(0,len(df['中文名称'])):
    df_data.iloc[i,0] = float(df['景区码'][i])
    if df['评分'][i]=='--':
        df_data.iloc[i,1]=0
    else:
        df_data.iloc[i,1]= float(df['评分'][i])

    if df['门票'][i]=='-':
        df_data.iloc[i,2]=0
    else:
        df_data.iloc[i,2] =float(df['门票'][i])

    df_data.iloc[i,3] = df['城市adcode'][i]
df_data.dropna(inplace=True)
# df_data['城市adcode'][2102]
k = 500   #聚类的类别
iteration = 600  #聚类最大循环次数
data_zs = 1.0*(df_data-df_data.mean())/df_data.std()   #数据标准化

#构建kmeans模型
from sklearn.cluster import KMeans
model = KMeans(n_clusters = k, n_jobs = 5, max_iter = iteration, random_state = 1234) #分类为k，并发数为4
model.fit(data_zs)
#简单打印结果
r1 = pd.Series(model.labels_).value_counts()  #统计各类别数目
r2 = pd.DataFrame(model.cluster_centers_)  #找出聚类中心
r = pd.concat([r2,r1],axis =1)  #得到聚类中心对应的类别下的数目

r.columns = list(df_data.columns) + ['类别数目']    #重命名表头
# print(r)

r = pd.concat([df_data, pd.Series(model.labels_,index =df_data.index)],axis =1)
r.columns = list(df_data.columns) + ['聚类类别']

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

    df=pd.DataFrame(list_res[1:len(list_res)],columns=list_res[0])
    return df,list_res

# str(r['id'][8])== str(8)



import pymysql
list_res = getData()[1]


list_new = list_res[1:7000]



conn = get_conn()
cursor = conn.cursor()
count=0
for k in range(len(list_new)):
    if k!=2102 and k!=2475  and  k!=5697  and k!=7455 and k!=7943 and k!=7944 and k!=8364 and k!=10119 and k!=10443:
        #         print(k)
        for i in range(len(r['id'])):
            # print(i)
            if  i!=2102 and i!=2475  and  i!=5697  and i!=7455 and i!=7943 and i!=7944 and i!=8364 and i!=10119 and i!=10443 and float(list_new[k][0]) == r['id'][i]:
                #                   print()
                sqlInsert="update scenery set cluster=%s where id=%s"
                cluster = r['聚类类别'][i]
                #                     print(cluster)
                item = list_new[k][0]
                #                     print(value)
                try:
                    cursor.execute(sqlInsert,(cluster,item))
                    conn.commit()
                finally:
                    conn.close
#             count+=1
#     print(count)







