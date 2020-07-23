import os
import sys
from pyhanlp import *

if __name__ == '__main__':
    if len(sys.argv) > 1:
        top_N = int(sys.argv[1])
    else:
        top_N = 1000
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = os.path.join(root_dir,"project/training/merged_text.txt")
    text = open(filename, "r").read()
    print(len(text))
    text_len = int(len(text) * 0.6)
    new_words = HanLP.extractPhrase(text[:text_len],top_N)
    target_file = os.path.join(root_dir,"project/training/phrases.txt")
    with open(target_file,"w") as wf:
        for word in new_words:
            word = word.strip()
            if word == "":continue
            wf.write(word.strip()+"\n")