import os
import jieba
from model import TrieNode
from utils import get_stopwords, load_dictionary, generate_ngram, save_model, load_model
from config import basedir


def load_data(filename, stopwords):
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            word_list = [x for x in jieba.cut(line.strip(), cut_all=False) if x not in stopwords]
            data.append(word_list)
    return data


def load_data_2_root(data):
    print('------> insert nodes')
    print("total data list:", len(data))
    for i, word_list in enumerate(data):
        if i != 0 and i % 1000 == 0:
            print(i)
        ngrams = generate_ngram(word_list, 3)
        for d in ngrams:
            root.add(d)
    print('------> insert successfully')


if __name__ == '__main__':
    root_name = basedir + "/data/root.pkl"
    stopwords = get_stopwords()
    if os.path.exists(root_name):
        root = load_model(root_name)
    else:
        dict_name = basedir + '/data/dict.txt'
        word_freq = load_dictionary(dict_name)
        root = TrieNode('*', word_freq)
        save_model(root, root_name)

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = os.path.join(root_dir, "./newword_find/data/merged_text3.txt")
    data = load_data(filename, stopwords)
    load_data_2_root(data)
    topN = 2000
    result, add_word = root.find_word(topN)
    target_file = os.path.join(root_dir, "./newword_find/data/phrases_ref4.txt")
    with open(target_file, "w",encoding='utf-8') as wf:
        for word, score in add_word.items():
            word = word.strip()
            if word == "": continue
            wf.write(word.strip() + "\n")
