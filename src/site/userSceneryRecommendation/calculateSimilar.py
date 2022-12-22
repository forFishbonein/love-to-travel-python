import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import DataProcess
import vecWord

EmbedingUser= vecWord.vecUser_train()
EmbedingIterm= vecWord.vecSCenery_train()
iterm2Id= DataProcess.SceneryData()

myUser2Id= DataProcess.UserData()

# EmbedingUser = pd.read_csv('EmbedingUser.csv').drop(columns=['Unnamed: 0'])
# EmbedingIterm = pd.read_csv('EmbedingScenery.csv').drop(columns=['Unnamed: 0'])
# iterm2Id = pd.read_csv(r'D:\暂存文件\recommenderSystemForFlowerShop-master\recommenderSystemForFlowerShop-master\scenery_test.csv',encoding="GBK",dtype='str')
# myUser2Id = pd.read_csv(r'D:\暂存文件\recommenderSystemForFlowerShop-master\recommenderSystemForFlowerShop-master\User_test.csv',dtype='str')

# print(EmbedingUser)
# print(iterm2Id)
# print(myUser2Id)

def getUseEmbeding(userid):
    return np.array(EmbedingUser.loc[userid])

def getItermEmbeding(itermid):
    return np.array(EmbedingIterm.loc[itermid])

def calculateSimilarIterm4User(userNo,num=10):
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

def calculateSimilarUser4Iterm(itermNo,num=10):
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
