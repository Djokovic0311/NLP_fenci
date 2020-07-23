import jieba

#分词
def stripdata(Test):
    # jieba 默认启用了HMM（隐马尔科夫模型）进行中文分词
    seg_list = jieba.cut(Test)  # 分词

    #获取字典，去除停用词
    line = "/".join(seg_list)
    word = stripword(line)
    #print(line)
    #列出关键字
    #print("\n关键字：\n"+word)

#停用词分析
def stripword(seg):
    #打开写入关键词的文件
    keyword = open('key_word.txt', 'w+', encoding='utf-8')
    print("去停用词：\n")
    wordlist = []

    #获取停用词表
    stop = open('stopword.txt', 'r+', encoding='utf-8')
    stopword = stop.read().split("\n")

    #遍历分词表
    for key in seg.split('/'):
        #print(key)
        #去除停用词，去除单字，去除重复词
        if not(key.strip() in stopword) and (len(key.strip()) > 1) and not(key.strip() in wordlist) :
            wordlist.append(key)
            #print(key)
            keyword.write(key+"\n")

    #停用词去除END
    stop.close()
    keyword.close()
    return '/'.join(wordlist)

def creat():
    Rawdata = open('test.txt','r+',encoding='utf-8')
    text = Rawdata.read()
    #调用分词
    stripdata(text)

    #END
    Rawdata.close()

creat()