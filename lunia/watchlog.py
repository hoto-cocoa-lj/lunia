import shutil,lunia.constant as lc,re

logfile='all.log'
path1='watchlog/'
pattern='INFO: 	(.{2,3})鉴定((\d)个)?(\d)级'
patternE=' (\d+):(\d+):(\d+),'

#把'可能有bug出现'的log删除
def deleteBugLog(p=logfile):
    p1, p2 = p ,path1 + p
    with open(p1, 'r',encoding='utf-8') as f:
        with open(p2, 'w',encoding='utf-8') as g:
            content=f.readlines()
            content.reverse()
            c=[]
            flg,j=True,0
            for i in range(len(content)):
                line=content[i]
                if '可能有bug出现' in line:
                    flg=False
                    j=i
                if not flg and j+5==i:
                    flg=True
                if flg:
                    # g.write(line)
                    c.append(line)
            c.reverse()
            g.writelines(c)

#把跟鉴定结果无关的log删除
def deleteUselessRow(p=path1+logfile):
    with open(p, 'r',encoding='utf-8') as f:
        with open(p+'.new', 'w',encoding='utf-8') as g:
            for line in f.readlines():
                if '颜色均值' in line:
                    g.write(line)
    shutil.move(p+'.new', p)

#由于弹成就等原因，会出现同一时间鉴定一堆属性的现象，返回相关的行数
def getErrorRows(p=path1+logfile):
    lst=[]
    with open(p, 'r',encoding='utf-8') as f:
        l1=len(f.readlines())
        f.seek(0)
        text=f.read()
        matchs=re.findall(patternE, text)
        for match in matchs:
            _,m,s=match
            m=int(m) if m[0]!='0' else int(m[1])
            s=int(s) if s[0]!='0' else int(s[1])
            lst.append(m*60+s)
    assert len(lst)==l1
    i,j,e=0,1,0
    elst=[]
    while 1:
        if i>=len(lst) or j>=len(lst):
            break
        if abs(lst[i]-lst[j])<=2:
            e,j=e+1,j+1
        else:
            if e>=3:
                for k in range(i,j):
                    # elst.append(lst[k])
                    elst.append(k)
            i,j,e=j,j+1,0
    return elst

#删除getErrorRows返回的行数
def deleteErrorRow(p=path1+logfile):
    elst=getErrorRows(p)
    with open(p, 'r',encoding='utf-8') as f:
        with open(p+'.new', 'w',encoding='utf-8') as g:
            lines=f.readlines()
            for i in range(len(lines)):
                if i not in elst:
                    g.write(lines[i])
    shutil.move(p+'.new', p)

#获取鉴定结果
def getZJDDic(p=path1+logfile):
    dic = {}
    for i in lc.ATTRS:
        dic[i]=[0]*9
    with open(p, 'r',encoding='utf-8') as f:
        l1=len(f.readlines())
        f.seek(0)
        text=f.read()
        matchs=re.findall(pattern, text)
        assert  len(matchs)==l1
        for match in matchs:
            a,c,d=match[0],match[2],int(match[3])
            c=int(c) if len(c)>0 else 1
            dic[a][d-1]+=c
            dic[a][8]+=c
    print(dic)
    return dic

def generateData(p,d={}):
    deleteBugLog(p)
    deleteUselessRow(path1+p)
    deleteErrorRow(path1+p)
    dic=getZJDDic(path1+p)
    sum_=0
    for i in dic:
        sum_+=dic[i][-1]
        for j in range(len(dic[i])):
            d[i][j]+=dic[i][j]
    print(sum_)
    return d

if __name__=='__main__':
    # p =  logfile
    d,dper = {},{}
    for i in lc.ATTRS:
        d[i]=[0]*9
        dper[i] = [0]*8
    for p in ['all.log','all.log.2021-06-17','all.log.2021-06-21']:
        d=generateData(p,d)

    for i in d:
        for j in range(len(d[i])-1):
            dper[i][j] = round(d[i][j]/d[i][-1],2)
    print(d,'-'*88,dper)