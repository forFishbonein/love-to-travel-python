#第一步：基于K-means对用户进行分组
import DataProcess
from sklearn.cluster import KMeans
from collections import Counter
#数据预处理，独热编码——特征离散化

def hotCode():
    DataProcess.labelData()
    user_list= DataProcess.userData()
    label_list,area_list= DataProcess.labelData()
    # print(user_list)

    user_list_vec = []
    for row in user_list:
        user_list_vec.append(row[2])

    #地域独热编码模板
    area_onehot_tpl = []
    for _ in area_list:
        area_onehot_tpl.append(0)
    # print("地域独热编码模板：", area_onehot_tpl)

    #标签独热编码模板
    label_onehot_tpl = []
    for _ in label_list:
        label_onehot_tpl.append(0)
    # print("标签独热编码模板：", label_onehot_tpl)

    user_vec_list = []
    for row in user_list_vec:

        # 对地域进行独热编码（平展开来）
        area_vec = area_onehot_tpl.copy()
        area_vec[row[0]] = 1
        # 对标签进行独热编码（平展开来）
        label_vec = label_onehot_tpl.copy()
        label_vec[row[1]] = 1
        user_vec_list.append(
             area_vec + label_vec
        )
    return user_vec_list,label_onehot_tpl,area_onehot_tpl

#用户分组
def groupData():
    k = 10
    user_vec_list,label_onehot_tpl,area_onehot_tpl=hotCode()
    #构造k-means模型
    model = KMeans(n_clusters = k)
    # print(user_vec_list)
    #
    #进行分组（训练）
    model.fit(user_vec_list)

    #提取分组信息
    n_labels = model.labels_

    #提取中心点信息
    n_centers = model.cluster_centers_

    #打印分组信息
    # print("分组信息:",n_labels)
    # print("-" * 50)
    # print("每个组的中心点: ", n_centers)

    # 把分组后的信息与原来的用户信息进行整合
    # print(["用户ID", "用户名称", "用户特征(栏目,地域,标签)", "用户特征（独热编码）", "分组编号"])
    # print("-" * 50)
    # 原本的用户特征：[0, '用户_1_科技_广西_AI', [0, 3, 0]] #
    #print(user_list)
    # 分组信息和用户信息整合
    user_list= DataProcess.userData()
    group_user_list = []
    for i, row in enumerate(user_list):
        # 用户记录，追加：独热编码后的特征与组信息
        group_user_list.append(row + [user_vec_list[i]] + [n_labels[i]])
    return group_user_list
    # 打印
    # for row in group_user_list:
    #     print(row)
    # for row in user_vec_list[:5]:
    #     print(row)

    Counter(n_labels)

# print(hotCode())