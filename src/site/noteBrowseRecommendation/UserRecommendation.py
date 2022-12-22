import UserGroup
import DataProcess
import random
#选择第3组为例
from sklearn.metrics.pairwise import cosine_similarity

def userRe():
    group_user_list= UserGroup.groupData()
    g_idx = 3
    # print("选定的分组信息为：", g_idx)

    # 提取该分组的所有用户
    target_g_users = []
    for row in group_user_list:
        if row[-1] == g_idx:
            target_g_users.append(row)
    # print("分组的所有用户为：")
    # for row in target_g_users:
    #     print(row)
    # 随机从选定的分组中选择一个用户作为我们列子的目标用户

    u_idx = random.randint(0, len(target_g_users) - 1)
    target_user = target_g_users[u_idx]
    # print("选取的目标用户为：", target_user)

    # 提前每一篇文章的特征
    # ['文章ID', '文章标题', '文章特征(栏目,地域,标签)'] [1, '文章_1学习_上海_C/C++', [3, 1, 3]]
    wenz_list= DataProcess.noteData()
    wenz_vec_list = []
    for row in wenz_list:
        wenz_vec_list.append(row[-1])
        # 文章特征情况 #
    # print("文章特征：", wenz_vec_list)
    return wenz_vec_list,target_g_users,target_user

#对文章的特征以独热编码展开
def noteHotCode():
    wenz_list_vec = []
    wenz_vec_list,target_g_users,target_user=userRe()
    user_vec_list,label_onehot_tpl,area_onehot_tpl= UserGroup.hotCode()
    for row in wenz_vec_list:
        # 对栏目进行独热编码（平展开来）
        #     topic_vec = topic_onehot_tpl.copy()
        #     topic_vec[row[0]] = 1
        # 对地域进行独热编码（平展开来）

        area_vec = area_onehot_tpl.copy()
        area_vec[row[0]] = 1
        # 对标签进行独热编码（平展开来）

        label_vec = label_onehot_tpl.copy()
        label_vec[row[0]] = 1


    for i, row in enumerate(wenz_vec_list):
        # 对栏目进行独热编码（平展开来）
        #     topic_vec = topic_onehot_tpl.copy()
        #     topic_vec[row[0]] = 1

        # 对地域进行独热编码（平展开来）
        area_vec = area_onehot_tpl.copy()
        area_vec[row[0]] = 1

        # 对标签进行独热编码（平展开来）
        label_vec = label_onehot_tpl.copy()
        label_vec[row[1]] = 1

        wenz_vec_list[i] =  area_vec + label_vec
    #print("文章特征独热编码展开后：", wenz_vec_list)
    # 对目标分组的用户，生成每一个用户的推荐列表（基于余弦相似度实现）
    # target_g_users=userRe()[1]
    user_rec_list1 = []
    for row in target_g_users:
        # ['用户ID', '用户名称', '用户特征(栏目,地域,标签)', '用户特征（独热编码）', '分组编号']
        # [0, '用户_1_科技_广西_AI', [0, 3, 0], [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0], 1]
        user_vec = row[-2]
        #print([user_vec])

        # 基于用户的独热编码特征与文章的独热编码特征进行相似度计算
        sim_list = cosine_similarity([user_vec], wenz_vec_list)
        #print(sim_list)

        # 用户与文章的相似度与文章编号关联起来
        sim_list1 = []
        for i, sim_v in enumerate(sim_list[0]):
            sim_list1.append((i, sim_v))
            # 用户与每一篇文章相似内容做排序
        sorted_sim_list = sorted(sim_list1, key=lambda row: row[1], reverse=True)

        # 为了方便，这里只提取最相关的前10篇文章
        user_rec_list1.append(sorted_sim_list[:10])

    # print("组用户的推荐列表信息：")
    for i, wlis in enumerate(user_rec_list1):
        # print("-" * 50)
        # print("用户信息：", target_g_users[i])
        # print("-" * 50)
        for w in wlis:
            print("文章编号：{}，相似度: {}".format(w[0], w[1]))

    return target_g_users,user_rec_list1


def personalRe():
    # 提取出个人推荐的文章列表(只提前文章编号)
    target_g_users,user_rec_list1=noteHotCode()
    # user_rec_list1=noteHotCode()[1]
    wenz_vec_list,target_g_users,target_user=userRe()
    target_wenz_list = []
    for i, wlis in enumerate(user_rec_list1):
        # 第一个元素是用户编号，用户ID
        if (target_user[0] != target_g_users[i][0]):
            continue
        for w in wlis:
            target_wenz_list.append(w[0])
    print("用户个人的推荐列表信息: ", target_wenz_list)

    # 组成员的文章推荐列表信息（只提前文章编号）
    target_g_wenz_list = []
    for i, wlis in enumerate(user_rec_list1):
        for w in wlis:
            target_g_wenz_list.append(w[0])
    print("组成员个人推荐的文章列表的合集：", target_g_wenz_list)
    #U3

    # 模拟组用户浏览了一些文章
    target_g_view_list = []
    # 浏览的内容是根据相似度推荐里面的
    for _ in range(10):
        idx = random.randint(0, len(target_g_wenz_list))
        target_g_view_list.append(target_g_wenz_list[idx])
    # 浏览一些最新的时政信息或者火爆全网的消息或者小概率推送一些和用户没有那么相关的内容（如，广告，哈哈哈）
    wenz_vec_list=userRe()[0]
    for _ in range(10):
        idx = random.randint(0, len(wenz_vec_list))
        if idx not in target_g_view_list:
            target_g_view_list.append(idx)
    print("组成员最近浏览的文章列表合集:", target_g_view_list)
    return target_wenz_list,target_g_view_list,target_g_wenz_list
    #U2
def atest():
    print("dddd")

if __name__ == "__main__":
    personalRe()