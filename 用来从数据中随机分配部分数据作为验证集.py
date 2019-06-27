#coding=utf-8
#用来从数据中随机分配部分数据作为验证集
#输入：原始数据集folder以及其对应的图像label的txt文件


import os
import random
import shutil
import sys

imgPath='./testData'
split_outPath='./valData'
os.system("mkdir valData")

IntxtPath='./flaw_label_test.list'
split_outTxtPath ='./flaw_label_val.list'
split_reminTxtPath ='./flaw_label_remain_test.list'
imgFiles = os.listdir(imgPath)
imgNum = len(imgFiles)


labelIndex={}
f=open(IntxtPath,'r')
while (1):
    line=f.readline()
    if line:
        if line.startswith('image'):
            imgname=line.strip('\n').strip('\r')
            bblist=[]
            num=f.readline().strip('\n')
            for i in range(int(num)):
                bbi=f.readline().strip('\n').strip('\r')
                bbi=bbi.split(' ')
                bblist.append(bbi)
            labelIndex[imgname]=bblist
    else:
        break


#print(len(labelIndex))
#print(labelIndex)
#sys.exit(1)

resultList=random.sample(range(0,imgNum-1),500)
fo = open(split_outTxtPath, "w")
fr = open(split_reminTxtPath, "w")
for i in resultList:
    imgName = os.path.join(imgPath,imgFiles[i])
    shutil.move(imgName,os.path.join(split_outPath,imgFiles[i]))
    txtName=str(imgFiles[i])
    print(txtName)
    fo.write(str(txtName)+'\n')
    labelNum = len(labelIndex[txtName])
    fo.write(str(labelNum)+'\n')
    for j in range(labelNum):
        curLabel = labelIndex[txtName][j]
        curLabelToWrite = " ".join(curLabel)
        print(curLabelToWrite)
        # sys.exit(1)
        fo.write(curLabelToWrite+'\n')



print("_-------------------------val done----------------------------_")

remainList = os.listdir(imgPath)
for r in remainList:
    txtName=str(r)
    print(txtName)
    fr.write(str(txtName)+'\n')
    labelNum = len(labelIndex[txtName])
    fr.write(str(labelNum)+'\n')
    for j in range(labelNum):
        curLabel = labelIndex[txtName][j]
        curLabelToWrite = " ".join(curLabel)
        fr.write(curLabelToWrite+'\n')



    # orifo = open(os.path.join(txtPath,txtName),'r')
    # fo.write(str(imgFiles[i])+'\n')
    # while 1:
    #     line = orifo.readline()
    #     if line:
    #         fo.write(line)
    #     else:
    #         break





