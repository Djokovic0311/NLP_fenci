g=open("ans.txt","w")
f=open("test.txt","r")
line=f.readline()
i=1
while line:
    if i%2 == 1 :
        g.write(line)
        #g.write("\n")
        i+=1
        line=f.readline()
    else:
        line=f.readline()
        i+=1
g.close()
f.close()