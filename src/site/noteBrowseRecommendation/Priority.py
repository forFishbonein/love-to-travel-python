#构建给某个用户推荐内容的优先顺序
# 最终的推荐列表
# 第一优先级：个人推荐列表：target_wenz_list
import UserRecommendation
import DataProcess
def recommenduser():
    target_wenz_list,target_g_view_list,target_g_wenz_list= UserRecommendation.personalRe()

    level_1_list = target_wenz_list
    print("第一优先级推荐：", level_1_list)

    # target_g_view_list=UserRecommendation.personalRe()[1]
    # target_g_wenz_list=UserRecommendation.personalRe()[2]

    # 第二优先级：最近浏览与组推荐列表的交集 并且 排除 level_1_list的记录
    level_2_list = list(set(target_g_view_list) & set(target_g_wenz_list) - set(level_1_list))
    print("第二优先级推荐：", level_2_list)

    # 第三优先级：最近浏览记录排查组推荐的列表 并且 排除 level_1_list、level_2_list的记录
    level_3_list = list(set(target_g_view_list) - set(target_g_wenz_list) - set(level_1_list) - set(level_2_list))
    print("第三优先级推荐：", level_3_list)

    # 第四优先级：组里面各个用户推荐的合集 排除 level_1_list、level_2_list、level_3_list的记录
    level_4_list = list(set(target_g_wenz_list) - set(level_1_list) - set(level_2_list) - set(level_3_list))
    print("第四优先级推荐：", level_4_list)


    wenz_vec_list,target_g_users,target_user= UserRecommendation.userRe()
    print("给目标用户：id=({}),昵称=({})，推荐的文章列表为：".format(target_user[1], target_user[2]))
    print("-" * 50)

    print("第一优先级：")
    print("-" * 50)


    wenz_list= DataProcess.noteData()
    for wid in level_1_list:
        # 文章编号与文章标题
        print("{}, {}".format(wenz_list[wid][0], wenz_list[wid][1]))

    print("第二优先级：")
    print("-" * 50)
    for wid in level_2_list:
        print("{}, {}".format(wenz_list[wid][0], wenz_list[wid][1]))

    print("第三优先级：")
    print("-" * 50)
    for wid in level_3_list:
        print("{}, {}".format(wenz_list[wid][0], wenz_list[wid][1]))

    print("第四优先级：")
    print("-" * 50)
    for wid in level_4_list:
        print("{}, {}".format(wenz_list[wid][0], wenz_list[wid][1]))

if __name__ == "__main__":
    recommenduser()