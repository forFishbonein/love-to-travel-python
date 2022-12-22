from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def train_function_userId():

    note_data=open('userId.txt')

    #     print(scenery_data)
    model = Word2Vec(LineSentence(note_data),sg=0, vector_size = 10, window=5, min_count=1, workers=9)

    model.save('userId.word2vec')
#     model.wv.most_similar('孔明', topn = 20)

def train_function_sceneryId():

    note_data=open('sceneryId.txt')

    #     print(scenery_data)
    model = Word2Vec(LineSentence(note_data),sg=0, vector_size = 10, window=5, min_count=1, workers=9)

    model.save('sceneryId.word2vec')
#     model.wv.most_similar('孔明', topn = 20)

if __name__ == '__main__':
    train_function_userId()
    train_function_sceneryId()

