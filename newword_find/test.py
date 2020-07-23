import os
from pyhanlp import *
from smoothnlp.algorithm.phrase import extract_phrase

def hannlp_test(input_file,output_file=None):
    text = open(input_file,"r").read()
    new_words = HanLP.extractPhrase(text,1000)
    print(new_words)

def smoothnlp_test(input_file,output_file=None):
    text = open(input_file,"r").readlines()
    new_words = extract_phrase(corpus=text,top_k=1000,chunk_size=10000,max_n=5,min_freq=5)
    print(new_words)

if __name__ == '__main__':
    dirname = os.path.dirname
    input_file = os.path.join(dirname(dirname(os.path.abspath(__file__)),"/data/merged_text.txt")
    # hannlp_test(input_file),output_file=None
    smoothnlp_test(input_file)
