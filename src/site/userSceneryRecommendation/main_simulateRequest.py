from calculateSimilar import calculateSimilarIterm4User,calculateSimilarUser4Iterm
import sys
def SceneryRec():

    # usrNo = input("请输入用户编号（如'1', '627', '1923'）：")
    res = calculateSimilarIterm4User(usrNo)
    # print('用户编号：' + usrNo + '推荐的前10个物品为：')

    print(res)
    return res

def UserRec(itermNo):
    res = calculateSimilarUser4Iterm(itermNo,num=10)
    # itermNo = input("请输入景区编号（如'21693', '84678', '85026B', '90210B'）：")
    # print('景区编号：' + itermNo + '推荐的前10个用户为：')
    for item in res:
        if item==None:
            res.remove(item)
    print(res)
    return res

if __name__ == "__main__":


    SceneryRec(usrNo)
