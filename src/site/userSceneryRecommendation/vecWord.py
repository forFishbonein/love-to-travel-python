import gensim
import pandas as pd

def vecUser_train():
    model = gensim.models.Word2Vec.load("userid.word2vec")
    file=open('userid.txt')
    user_data= file.read().splitlines()

    EmbedingUser=[['0','1','2','3','4','5','6','7','8','9']]
    for item in user_data:
        EmbedingUser.append(model.wv.get_vector(item))
    EmbedingUser=pd.DataFrame(EmbedingUser)
    return EmbedingUser

def vecSCenery_train():
    model = gensim.models.Word2Vec.load("sceneryId.word2vec")
    file=open('sceneryId.txt')
    scenery_data= file.read().splitlines()

    EmbedingScenery=[['0','1','2','3','4','5','6','7','8','9']]
    for item in scenery_data:
        EmbedingScenery.append(model.wv.get_vector(item))
    EmbedingScenery=pd.DataFrame(EmbedingScenery)
    return EmbedingScenery

print(vecUser_train())
print(vecSCenery_train())