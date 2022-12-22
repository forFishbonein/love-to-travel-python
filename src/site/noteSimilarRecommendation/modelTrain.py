from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import logging

import pandas as pd
import numpy as np
import gensim

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def tarin_function():
    #     scenery_data=open('D:\肖红娇\项目\爱旅游网站\原始数据\用户景区数据\sceid.txt')
    #r 只读
    import pandas as pd
    #     df = pd.read_excel('D:\肖红娇\项目\爱旅游网站\原始数据\全花销游记2.xlsx')

    note_data=open('data/train.txt',encoding='UTF-8')

    #     print(scenery_data)
    model = Word2Vec(LineSentence(note_data),sg=0, vector_size = 10, window=5, min_count=1, workers=9)
    #     model = Word2Vec(LineSentence(scenery_data),vector_size = 10, window = 2 , min_count = 3, epochs=7, negative=10,sg=1)

    model.save('data/note_data.word2vec')
#     model.wv.most_similar('孔明', topn = 20)
if __name__ == '__main__':
    tarin_function()


# model = gensim.models.Word2Vec.load(r"D:\肖红娇\项目\爱旅游网站\原始数据\游记数据\note_data.word2vec")
# model.save(r'D:\肖红娇\项目\爱旅游网站\原始数据\游记数据\note_data.word2vec')
# file=open(r'D:\肖红娇\项目\爱旅游网站\后台管理\NoteSimiliar\src\train.txt')
# note_data= file.read().splitlines()
# print(user_data)

# EmbedingNote=[]
# for item in note_data:
#     EmbedingNote.append(model.wv.get_vector(item))
# dfnote=pd.DataFrame(EmbedingNote)
# dfnote