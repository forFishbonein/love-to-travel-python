import pandas as pd
import codecs
import numpy
import gensim
import numpy as np
import re

from sqlalchemy import null

import connection
# from keyword_extract import *
import pymysql

wordvec_size=10
def get_char_pos(string,char):
    chPos=[]
    try:
        chPos=list(((pos) for pos,val in enumerate(string) if(val == char)))
    except:
        pass
    return chPos

#从text文件中读取关键词，利用之前训练好的词向量获取关键词的词向量
def word2vec(file_name,model):
    with codecs.open(file_name, 'r',encoding='UTF-8') as f:
        word_vec_all = numpy.zeros(wordvec_size)
        # print(wordvec_size)
        # print(word_vec_all)
        for data in f:

            space_pos = get_char_pos(data, ' ')
            # print(space_pos)
            first_word=data[0:space_pos[0]]
            if model.prepare_vocab(first_word):

                word_vec_all= word_vec_all+model.wv[first_word]

            for i in range(len(space_pos) - 1):
                word = data[space_pos[i]:space_pos[i + 1]]
                if model.prepare_vocab(word):
                    word_vec_all = word_vec_all+model.wv[word]

        # word_vec_all = numpy.zeros(wordvec_size)
        # for data in f:
        #     space_pos = get_char_pos(data, '\n')
        #     first_word=data[0:space_pos[0]]
        #     # if model.train(first_word):
        #     word_vec_all= word_vec_all+model[first_word]
        #
        #     for i in range(len(space_pos) - 1):
        #         word = data[space_pos[i]:space_pos[i + 1]]
        #         # if model.train(word):
        #         word_vec_all = word_vec_all+model[word]
        # print(word_vec_all)
        return word_vec_all

#通过余弦相似度计算两个向量之间的相似度
def simlarityCalu(vector1,vector2):
    vector1Mod=np.sqrt(vector1.dot(vector1))
    vector2Mod=np.sqrt(vector2.dot(vector2))
    if vector2Mod!=0 and vector1Mod!=0:
        simlarity=(vector1.dot(vector2))/(vector1Mod*vector2Mod)
    else:
        simlarity=0


    return simlarity

def getSmilarity():
    # note1_keywords ='note1.txt'
    # note2_keywords ='note2.txt'
    # note1_vec=word2vec(note1_keywords,model)
    # note2_vec=word2vec(note2_keywords,model)
    # sim=simlarityCalu(note1_vec,note2_vec)
    # return sim
    noteId=connection.getId()

    # for i in range(noteId[10:100]):#7225为游记数量
    simlarity_list=[]
    # i_str=str(i+1)
    # print(noteId[i])
    note1_keywords ="data/note10.txt"
    for j in range(10,30):

        j_str=str(j+1)
        # note2_keywords = "data/note"+j_str+'.txt'
        # note1_vec=word2vec(note1_keywords,model)
        # note2_vec=word2vec(note2_keywords,model)
        # sim=simlarityCalu(note1_vec,note2_vec)
        print(noteId[10])
    #
    #     list1=[noteId[j],sim]
    #     print(list1)
    #     simlarity_list.append(list1)
    # simlarity_list.sort(key=lambda ele:ele[1],reverse=True)
    #     # conn = get_conn()
    #     # cursor= smilarityData()
    #
    # simlarity_list_res=simlarity_list[:10]
        # sqlInsert=null
        # str1=''
        # for i in range(len(simlarity_list_res)):
        #     sqlInsert="insert note_related value(%s,%s)"
        #     str1+=str(simlarity_list_res[i][0],)
        # value = [simlarity_list_res[0][0],str1]
        # value = (str(noteId[0]),str(noteId[1]))
        # print(value)
        #
        # try:
        #     cursor.execute(sqlInsert,value)
        #     conn.commit()
        # finally:
        #     conn.close
    # return simlarity_list_res

def get_conn():
    return pymysql.connect(
        host='47.98.138.0',
        port=3306,
        user='travelservice',
        password='2x8R3WmbCzt6tcEd',
        database='travelservice',
        charset='utf8'
    )

def smilarityData():
    conn = get_conn()
    sql = "select * from note_related"
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        list1=list(cursor.fetchall())
        # print(list1)
    except pymysql.Error as e:
        print('连接失败')
    return cursor



if __name__ == '__main__':


    # model = gensim.models.Word2Vec.load('data/note_data.word2vec')
    # smilarityData()
    getSmilarity ()


