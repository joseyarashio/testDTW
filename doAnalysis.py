import math
import numpy as np
import matplotlib.pyplot as plt
from dtw import *

def getSample(filename):
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET
    
    tree = ET.ElementTree(file=filename)
    root = tree.getroot()
    
    text=[]
    Start=[]
    End=[]
    SampleArray=[]
    pitch=[]
    volume=[]
    
    for elem in tree.findall('cm/word/text'):
        text.append(elem.text)
        
    for elem in tree.findall('cm/word/interval'):
        a=elem.text.split()[0]
        Start.append(a)
        b=elem.text.split()[1]
        End.append(b)
        
    for elem in tree.findall('cm/word/pitch'):
        a=elem.text.split()
        floats = [float(x) for x in elem.text.split()]
        pitch.append(floats)
        
    for elem in tree.findall('cm/word/volume'):
        a=elem.text.split()
        floats = [float(x) for x in elem.text.split()]
        volume.append(floats)
        
    SampleArray.append(text)
    SampleArray.append(Start)
    SampleArray.append(End)
    SampleArray.append(pitch)
    SampleArray.append(volume)
    return SampleArray
    
def compare(S_index,U_index,Sample,User):
    '''find the DTW path'''
    s1=len(Sample[3][S_index])
    x1=sum(Sample[3][S_index])/s1
    print('word_Sample:',Sample[0][S_index])
    print('word_User:',User[0][U_index])
    print('average Pitch:Sample:',x1)
    s2=len(User[3][U_index])
    x2=sum(User[3][U_index])/s2
    print('average Pitch:User:',x2)
    move=x1-x2
    print('moving step=',move)
    AdaptUser = [x + move for x in User[3][U_index]]
    
    if(s1/s2)<2 and (s1/s2)>0.5:
        dodtw = Dtw(Sample[3][S_index],AdaptUser,distance_func=lambda x, y: math.fabs(x - y))
        print('total DTW_distance=',dodtw.calculate())
        print('mapping matrix:',dodtw.get_path()[::-1])
        print('lenth:',len(dodtw.get_path()))
        (total_dst,times)=calculate_Dst(dodtw.get_path(),Sample[3][S_index],AdaptUser)
        print('unit DTW_distance=',total_dst/times)
        p1=[]
        p2=[]
        p3=[]
        for i in range(len(Sample[3][S_index])):
            p1.append(i)
        for i in range(len(AdaptUser)):
            p2.append(i)
        for i in range(len(User[3][U_index])):
            p3.append(i)
            #plot data
        f=figure(User[0][U_index]+str(U_index)+str(S_index))
        subplot(2,1,1)
        plt.plot(p1,Sample[3][S_index], linestyle="dashed", marker="o", color="green",label='Sample')
        plt.plot(p2,AdaptUser, linestyle="dashed", marker="o", color="red",label='User')
        plt.plot(p3,User[3][U_index], linestyle="dashed", marker="o", color="pink",label='User2')
        plt.ylim((40,65))
        plt.title('word: '+User[0][U_index])
        plt.xlabel('unit dst(DTW):'+str(round(total_dst/times,2))+'______total distance(DTW):'+str(round(total_dst,2)))
        subplot(2,1,2)
        plt.plot(p1,Sample[4][S_index], linestyle="dashed", marker="o", color="green",label='Sample')
        plt.plot(p2,User[4][U_index], linestyle="dashed", marker="o", color="red",label='User')
        plt.xlabel('unit dst(DTW):'+str(round(total_dst/times,2))+'______total distance(DTW):'+str(round(total_dst,2)))
        f.show()
    else:
        print('compare failed')

def calculate_Dst(DTW_path,Sample,User):
    '''calculate the distance between Sample and User'''
    total_dst=0
    times=0
    for x in DTW_path:
        total_dst+=abs(Sample[x[0]]-User[x[1]])
        #print(x[0],',',x[1],total_dst)
        times+=1
    print('total distance:',total_dst/2)
    print('point:',times/2)
    return (total_dst,times)
    
def find_matching_list(Sampletext_list,Usertext_list):
    matching=[]
    pivot=-1
    for idy, word_u in enumerate(Usertext_list):
        for idx, word_s in enumerate(Sampletext_list):
            if(word_u==word_s)and(word_u!=None)and(idx>pivot):
                matching.append((idx,idy))
                pivot=idx
                break
    return matching
    
def makeCsv(Sample):
    Csv=open('output.csv','w')
    
    textList=Sample[0]
    timeList=Sample[1]
    
    for i in range(len(textList)):
        if(str(textList[i]) != 'None'):
            Csv.write('['+str(timeList[i])+']'+str(textList[i])+'\n')
    Csv.close()
        
def result(opt):
    '''show the compare result '''
    Sample=getSample('output/output.xml')
    User=getSample('output/output2.xml')
    matching_list=find_matching_list(Sample[0],User[0])
    if(opt==-1):
        for x in matching_list:
            compare(x[0],x[1],Sample,User)
            print('------------------------------------')
    else:
        compare(matching_list[opt][0],matching_list[opt][1],Sample,User)
        print('------------------------------------')