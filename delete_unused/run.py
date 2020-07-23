import re
reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
def clearBlankLine():
    file1 = open('ans.txt', 'r', encoding='utf-8')
    file2 = open('total_ans.txt', 'w', encoding='utf-8')
    try:
        for line in file1.readlines():
            if line == '\n':
                line = line.strip("\n")
            file2.write(line)
    finally:
        file1.close()
        file2.close()


if __name__ == '__main__':
    f=open("total.txt",encoding='utf-8')
    p=open("ans.txt",'w',encoding='utf-8')
    line=f.readline()
    while line:
        temp=re.sub(reg, '', line)
        p.write(temp)
        p.write('\n')
        line=f.readline()
    f.close()
    clearBlankLine()
