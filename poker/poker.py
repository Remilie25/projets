#copyright 2023 DE PRETTO REMI
import ssl
from random import randint
import asyncio
import json
import logging
import websockets
import time
import threading

def dist():
    '''distribue les cartes 2 par joueur puis 5 à la table'''
    global Jinfo
    cd=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51]
    for i in Jinfo['JnP']:
        c1=randint(0,len(cd)-1)
        Jinfo[i][3][0]=cd[c1]
        print(i,cd[c1])
        cd[c1]=99
        cd.remove(99)
    for x in Jinfo['JnP']:
        c2=randint(0,len(cd)-1)
        Jinfo[x][3][1]=cd[c2]
        print(x,cd[c2])
        cd[c2]=99
        cd.remove(99)
    for y in range(5):
        c1=randint(0,len(cd)-1)
        Jinfo['ct'][y]=cd[c1]
        cd[c1]=99
        cd.remove(99)

def maxcept(c7,r):
    '''F° détermine le max de c7 à part les cartes du carré ou des paires'''
    if r['2paires']!=-25:
        c=[]
        for w in c7:
            if w!=r['2paires'] and w!=r['paire']:
                c.append(w)
        r['acolyte']=max(c)
    elif r['paire']!=-25:
        c=[]
        for w in c7:
            if w!=r['paire']:
                c.append(w)
        r['acolyte']=max(c)
        for w2 in c:
            if w2==r['paire'] or w2==r['acolyte']:
                c.remove(w2)
        r['2acolyte']=max(c)
        for w3 in c:
            if w3==r['paire'] or w3==r['acolyte'] or w3==r['2acolyte']:
                c.remove(w3)
        r['3acolyte']=max(c)
    elif r['brelan']!=-25:
        c=[]
        for w in c7:
            if w!=r['brelan']:
                c.append(w)
        r['acolyte']=max(c)
        for w2 in c:
            if w2==r['brelan'] or w2==r['acolyte']:
                c.remove(w2)
        r['2acolyte']=max(c)
    elif r['carré']!=-25:
        c=[]
        for w in c7:
            if w!=r['carré']:
                c.append(w)
        r['acolyte']=max(c)
    return r

def pbc(P):
    '''F° dit si il y a paires/brelan/carré/full/quinte'''
    global Jinfo
    c7=[]
    f={25:''}
    r={'paire':-25, '2paires':-25, 'brelan':-25, 'carré':-25, 'full':-25, 'quinte':-25, 'col':False,'h':[],'acolyte':-25}
    c0=Jinfo[P][3][0]%13
    c1=Jinfo[P][3][1]%13
    for i in Jinfo['ct']:
        c7.append(i%13)
    c7.append(c0)
    c7.append(c1)
    for x in c7:
        if x in f:
            f[x]+=1
        else:
            f[x]=1
    for x,y in f.items():
        if y==2:
            if r['paire']<x:
                r['2paires']=r['paire']
                r['paire']=x
            elif r['2paires']<x:
                r['2paires']=x
            r=maxcept(c7,r)
        elif y==3 and r['brelan']<x:
            r['brelan']=x
            r=maxcept(c7,r)
        elif y==4 and r['carré']<x:
            r['carré']=x
            r=maxcept(c7,r)
    c7.sort()
    for i in range(5):
        r['h'].append(c7[i+2])
    r=col(P,r)
    s=1
    if r['carré']==-25 and r['col']==False:
        if 12 in c7:
            c7.append(-1)
        c7.sort()
        h=[c7[0]]
        for y in range(len(c7)-1):
            if c7[y]+1==c7[y+1]:
                s+=1
                h.append(c7[y+1])
            elif c7[y]!=c7[y+1] and s<5:
                s=1
                h=[c7[y+1]]
        if s>=5:
            r['quinte']=h[-1]
            r['h']=[]
            h.sort()
            while len(h)>5:
                h.remove(h[0])
            for w in h:
                r['h'].append(w)
    elif r['col']==True:
        for y in range(4):
            if r['h'][y]+1==r['h'][y+1]:
                s+=1
            elif r['h'][y]!=r['h'][y+1] and s<5:
                s=1
        if s>=5:
            r['quinte']=r['h'][-1]%13
    if r['brelan']!=-25 and r['paire']!=-25:
        r['full']=r['brelan']
    if r['paire']==-25 and r['2paires']==-25 and r['brelan']==-25 and r['carré']==-25 and r['full']==-25 and r['quinte']==-25 and r['col']==False:
        c7.sort()
        r['h']=[]
        for i2 in range(5):
            r['h'].append(c7[-1-i])
    return r


def quinte(c7):
    s=1
    if 12 in c7:
        c7.append(-1)
    c7.sort()
    print(c7)
    h=[c7[0]]
    for y in range(len(c7)-1):
        if c7[y]+1==c7[y+1]:
            s+=1
            h.append(c7[y+1])
            print('+1','s=',s)
            if s>=5 and c7[y+1]+1!=c7[y+2]:
                return h
        elif c7[y]!=c7[y+1]:
            s=1
            h=[c7[y+1]]
            print('RST')
    return h


def col(P,r):
    '''F° dit s'il y a une couleur'''
    global Jinfo
    c7=[Jinfo[P][3][0],Jinfo[P][3][1]]
    d={'R':[],'G':[],'B':[],'N':[]}     #faire une liste de carte par couleur gardant num                                       OK
    for w in Jinfo['ct']:               #refaire col avec toutes les cartes pas juste joueur plus cartes de même col dans r     OK
        c7.append(w)
    for i in c7:
        if i<=12:
            d['R'].append(i)
        elif i<=25:
            d['G'].append(i)
        elif i<=38:
            d['B'].append(i)
        elif i<=51:
            d['N'].append(i)
    for x,y in d.items():
        if len(y)>=5:
            r['col']=True
            for w in y:
                r['h'].append(w)
            while len(r['h'])>5:
                r['h'].remove(r['h'][0])
            r['h'].sort()
    return r
##
def comp():
    '''F° qui donne un nbr correspondant à la valeur d'une main'''
    global Jinfo
    R={}
    for i in Jinfo['JnF']:
        r=pbc(i)
        print(i,r)
        if r['col']!=False and r['quinte']!=-25:                                #GROS PROBLEME CAR QUINTE ET COL DIFF MAIS QUINTE FLUSH
            cm=0
            if Jinfo[i][3][0] in r['h']:
                if Jinfo[i][3][1] in r['h']:
                    if Jinfo[i][3][1]%13<Jinfo[i][3][0]%13:
                        cm=Jinfo[i][3][0]%13/100+Jinfo[i][3][1]%13/10000
                    else:
                        cm=Jinfo[i][3][0]%13/10000+Jinfo[i][3][1]%13/100
                else:
                    cm=Jinfo[i][3][0]%13/100
            print('r=',r,'cm',cm)
            vm=13.1212-r['quinte']-cm                                           #TypeError: 'int' object is not subscriptable OK
        elif r['carré']!=-25:
            vm=26,12-r['carré']-r['acolyte']/100
        elif r['full']!=-25:
            vm=39.12-r['full']-r['paire']/100
        elif r['col']!=False:
            cm=r['h'][-1]%13+r['h'][-2]%13/100+r['h'][-3]%13/10000+r['h'][-4]%13/1000000+r['h'][-5]%13/100000000
            vm=52.12121212-cm
        elif r['quinte']!=-25:
            vm=65-r['quinte']
        elif r['brelan']!=-25:
            vm=78.1212-r['brelan']-r['acolyte']/100-r['2acolyte']/10000
        elif r['2paires']!=-25:
            vm=91.1212-r['paire']-r['2paires']/100-r['acolyte']/10000
        elif r['paire']!=-25:
            vm=104.121212-r['paire']-r['acolyte']/100-r['2acolyte']/10000-r['3acolyte']/1000000
        else:
            cm=r['h'][-1]+r['h'][-2]/100+r['h'][-3]/10000+r['h'][-4]/1000000+r['h'][-5]/100000000
            vm=117.12121212-cm
        R[i]=vm
    pm=[]
    m=150
    for r,t in R.items():
        if t<m:
            m=t
            pm=[r]
        elif t==m:
            pm.append(r)
    Jinfo['V']=pm
    print(R)
    return


def BBF():
    global Jinfo
    BB=[20,30,40,60,80,100,140]
    B=[10,15,20,30,40,50,70]
    dt=7
    Jinfo['niv']=0
    n2=Jinfo['Md']+dt
    n3=Jinfo['Md']+2*dt
    n4=Jinfo['Md']+3*dt
    n5=Jinfo['Md']+4*dt
    n6=Jinfo['Md']+5*dt
    n7=Jinfo['Md']+6*dt
    t=time.localtime()[4]
    if t<Jinfo['Md']:
        t+=60
    if t>=n7:
        Jinfo['niv']=6
    elif t>=n6:
        Jinfo['niv']=5
    elif t>=n5:
        Jinfo['niv']=4
    elif t>=n4:
        Jinfo['niv']=3
    elif t>=n3:
        Jinfo['niv']=2
    elif t>=n2:
        Jinfo['niv']=1
    Jinfo[Jinfo['JnP'][-1]][0]-=BB[Jinfo['niv']]
    Jinfo[Jinfo['JnP'][-2]][0]-=B[Jinfo['niv']]
    Jinfo[Jinfo['JnP'][-1]][2]+=BB[Jinfo['niv']]
    Jinfo[Jinfo['JnP'][-2]][2]+=B[Jinfo['niv']]
    Jinfo[Jinfo['JnP'][-1]][4]+=BB[Jinfo['niv']]
    Jinfo[Jinfo['JnP'][-2]][4]+=B[Jinfo['niv']]
    Jinfo[Jinfo['JnP'][-1]][5]+=BB[Jinfo['niv']]
    Jinfo[Jinfo['JnP'][-2]][5]+=B[Jinfo['niv']]
    Jinfo['PR']=Jinfo['JnP'][-1]
    Jinfo['Pot']=BB[Jinfo['niv']]+B[Jinfo['niv']]
    if len(Jinfo['JnP'])>2:
        Jinfo[Jinfo['JnP'][-3]][2]='D'
    return BB[Jinfo['niv']]


def creer_Jinfo():
    global Jinfo
    for i in Jinfo['JnP']:
        Jinfo[i]=[1500,False,0,[99,99],0,0]

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print("Starting " + self.name)
      deroulement()
      print("Exiting " + self.name)

def accord_Ac():   #A finir
    global Jinfo
    global c
    print('début')
    JAJ=[]
    for x in Jinfo['JnF']:
        JAJ.append(x)
    print(JAJ)
    a=0
    while a!=len(JAJ) and len(JAJ)>=2:
        print("a=",a,"c=",c,'lenJAJ=',len(JAJ))
        Jinfo['EAJ']=JAJ[c]
        print('EAJ=',Jinfo['EAJ'],'0=',Jinfo[Jinfo['EAJ']][0])
        Jinfo[JAJ[c]][1]=False
        if Jinfo[JAJ[c]][0]<=0:
            JAJ.remove(JAJ[c])
            print(Jinfo['EAJ'],'removed')
        else:
            T=0
            asyncio.run(notify_Jinfo())
            while Jinfo[JAJ[c]][1]==False and T<=30:
                time.sleep(1)
                T+=1
            C=Jinfo['C']==True or JAJ[c]==Jinfo['R']                                #il faut savoir si les accord_Ac marchent ?
            if T>=30 or Jinfo[JAJ[c]][1]=='F':
                Jinfo[JAJ[c]][1]='F'
                Jinfo['JnF'].remove(JAJ[c])
                JAJ.remove(JAJ[c])
                c-=1
            elif Jinfo[Jinfo['EAJ']][1]=='C' and C==True:
                a+=1
            elif Jinfo[Jinfo['EAJ']][1]=='C' and JAJ[c]==Jinfo['PR']:
                a+=1
            elif Jinfo[Jinfo['EAJ']][1]=='R':
                a=1
                Jinfo['R']=JAJ[c]
            elif Jinfo[Jinfo['EAJ']][1]=='P':
                a+=1
        c+=1
        c=c%len(JAJ)
        if len(Jinfo['JnF'])<=1:
            return 'AF'
##
def analyse(P,r):
    '''F° inspiree des plus grd ds #analyse, indique pbc'''
    c=[Jinfo[P][3][0],Jinfo[P][3][1]]
    c+=Jinfo['ct'][0:int(Jinfo['R'])]
    for i in range(len(c)):
        c[i]=c[i]%13                                                            #carte par hauteur
    if 12 in c:                                                                 #si as : quinte possible avec as plus petite carte
        c.append(-1)
    c.sort()
    suite=1
    maxsuite=1
    maxquinte=-25
    f={-1:0,0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}
    for i in range(len(c)-1):
        if c[i]+1==c[i+1]:
            suite+=1
        elif c[i]!=c[i+1]:
            maxquinte=c[i]
            maxsuite=max(maxsuite,suite)
            suite=1
        f[c[i]]+=1
    r['suite']=max(maxsuite,suite)
    for i in range(13):                                                         #parcours de f pour trouver :   (dans l'orde croissant dc ok pour hauteur de paires etc)
        if f[i]==2:                                                             #paire et 2paires
            if r['paire']==-25:
                r['paire']=i
            else:
                r['paire'],r['2paires']=r['paire'],i
        elif f[i]==3:                                                           #brelan
            r['brelan']=i
        elif f[i]==4:                                                           #carré
            r['carré']=i
    if r['brelan']!=-25 and r['paire']!=-25:                                    #full
        r['full']=r['brelan']
    if r['suite']>=5:                                                           #quinte
        r['quinte']=maxquinte
    r['h']=c[len(c)-5:len(c)]                                                   #liste hauteur
    return r

def col2(P,r):
    '''F° dit s'il y a une couleur'''
    global Jinfo
    c7=[Jinfo[P][3][0],Jinfo[P][3][1]]
    d={'R':[],'G':[],'B':[],'N':[]}
    for w in Jinfo['ct'][:int(Jinfo['R'])]:
        c7.append(w)
    for i in c7:
        if i<=12:
            d['R'].append(i)
        elif i<=25:
            d['G'].append(i)
        elif i<=38:
            d['B'].append(i)
        elif i<=51:
            d['N'].append(i)
    return d

##

def bot_eval():
    ''''F° évalue + ou - s'il faut pay ou fold de 1 à 10'''
    r={'paire':-25, '2paires':-25, 'brelan':-25, 'carré':-25, 'full':-25, 'quinte':-25, 'col':False,'h':[],'acolyte':-25,'suite':1}
    col=col2()
    maxcol=0
    rng=randint(1,100)
    for x in col.keys():
        if len(col[x])>len(maxcol):
            maxcol=col[x]
    r['col']=[-25,-25]
    if len(maxcol)-int(Jinfo['R'])>=0:
        if Jinfo[Jinfo['EAJ']][3][0] in maxcol:
            r['col'].append(Jinfo[Jinfo['EAJ']][3][0])
        if Jinfo[Jinfo['EAJ']][3][1] in maxcol:
            r['col'].append(Jinfo[Jinfo['EAJ']][3][1])
    r=analyse(Jinfo['EAJ'],r)

    if r['col']!=False and r['quinte']!=-25:                                #copie de comp mais ajuster pour eval la main
        cm=0
        if Jinfo[i][3][0] in r['h']:
            if Jinfo[i][3][1] in r['h']:
                if Jinfo[i][3][1]%13<Jinfo[i][3][0]%13:
                    cm=Jinfo[i][3][0]%13/100+Jinfo[i][3][1]%13/10000
                else:
                    cm=Jinfo[i][3][0]%13/10000+Jinfo[i][3][1]%13/100
            else:
                cm=Jinfo[i][3][0]%13/100
        print('r=',r,'cm',cm)
        vm=13.1212-r['quinte']-cm
    elif r['carré']!=-25:
        vm=26,12-r['carré']-r['acolyte']/100
    elif r['full']!=-25:
        vm=39.12-r['full']-r['paire']/100
    elif r['col']!=False:
        cm=r['h'][-1]%13+r['h'][-2]%13/100+r['h'][-3]%13/10000+r['h'][-4]%13/1000000+r['h'][-5]%13/100000000
        vm=52.12121212-cm
    elif r['quinte']!=-25:
        vm=65-r['quinte']
    elif r['brelan']!=-25:
        vm=78.1212-r['brelan']-r['acolyte']/100-r['2acolyte']/10000
    elif r['2paires']!=-25:
        vm=91.1212-r['paire']-r['2paires']/100-r['acolyte']/10000
    elif r['paire']!=-25:
        vm=104.121212-r['paire']-r['acolyte']/100-r['2acolyte']/10000-r['3acolyte']/1000000
    else:
        cm=r['h'][-1]+r['h'][-2]/100+r['h'][-3]/10000+r['h'][-4]/1000000+r['h'][-5]/100000000
        vm=117.12121212-cm


def bot():
    if Jinfo['EAJ'][0:3]=="bot":
        c1,c2=Jinfo[Jinfo['EAJ']][3][0]%13,Jinfo[Jinfo['EAJ']][3][1]%13         #cartes sans col
        if Jinfo['R']=='C':                                                     #pre-flop
            if c1>3 or c2>3:
                rng=randint(1,10)
                if c1==c2:                                                      #si paire
                    if c1+rng>7:
                        Jinfo[Jinfo['EAJ']][1]='P'
                    else:
                        Jinfo[Jinfo['EAJ']][1]='F'
                else:                                                           #sinon           #si joueur que raise : faiblesse ?
                    if 4*(Jinfo['Hmise']-Jinfo[Jinfo['EAJ']][4])<Jinfo[Jinfo['EAJ']][0]:    #si Hmise << Tune
                        if (c2+c1)/2+rng>7:
                            Jinfo[Jinfo['EAJ']][1]='P'
                        else:
                            Jinfo[Jinfo['EAJ']][1]='F'
                    else:                                                                   #sinon
                        if (c2+c1)/2+rng/2>10:
                            Jinfo[Jinfo['EAJ']][1]='P'
                        else:
                            Jinfo[Jinfo['EAJ']][1]='F'
            else:
                Jinfo[Jinfo['EAJ']]='F'
        elif Jinfo['R']=='3':                                                   #flop
            rng=randint(1,10)
            if bot_eval()+rng==0:
                r='rien'
    return

def m0():
    '''F° remet les mises et mises de tour à 0'''
    global Jinfo
    for i in Jinfo['JnP']:
        Jinfo[i][2]=0
        Jinfo[i][4]=0

def argentG():
    '''F° s'occupe de redistribuer l'argent au vainqueur et ceux qui ont miser plus'''
    global Jinfo
    mag=0
    JSA=0
    for i in Jinfo['JnP']:
        #print('i=',i,'5=',Jinfo[i][5],'V5=',Jinfo[Jinfo['V'][0]][5],'test=',Jinfo[Jinfo['V'][0]][5]>=Jinfo[i][5])
        if Jinfo[Jinfo['V'][0]][5]==Jinfo[i][5]:
            mag+=1
        elif Jinfo[Jinfo['V'][0]][5]>Jinfo[i][5]:
            mag+=1
            JSA+=Jinfo[i][5]
    #print('mag=',mag)
    if mag==len(Jinfo['JnP']):
        gain=Jinfo['Pot']
    else:
        gain=Jinfo[Jinfo['V'][0]][5]
        for x in Jinfo['JnP']:
            if x not in Jinfo['V']:
                Jinfo[x][0]+=Jinfo[x][5]-gain
    #print('gain=',gain)
    #print("V=",Jinfo['V'])
    if len(Jinfo['V'])==1:
        Jinfo[Jinfo['V'][0]][0]+=gain
    else:                                       #en cas d'égalité pas fini
        g=gain/len(Jinfo['V'])
        if type(g)==float:
            g=int(g)+1
        for i in Jinfo['V']:
            Jinfo[i][0]+=g
    for p in Jinfo['JnP']:
        Jinfo[p][5]=0
        Jinfo[p][4]=0
        Jinfo[p][2]=0
    Jinfo['Pot']=0
    Jinfo['V']=[]

def elim():
    global Jinfo
    Re=[]
    #print("elim :")
    for i in Jinfo['JnP']:
       # print('i=',i,'tune=',Jinfo[i][0])
        if Jinfo[i][0]<=0:
            Jinfo[i][1]='F'
            Re.append(i)
   # print('Re=',Re)
    for x in Re:
        Jinfo['JnP'].remove(x)
    #print()

def J1():
    global Jinfo
    Jinfo['JnP'].append(Jinfo['JnP'][0])
    Jinfo['JnP'].remove(Jinfo['JnP'][0])

def Gmise(P,a):
    global Jinfo
    if a=='R':
        print(P,a,Jinfo[P][2])
        Jinfo[P][0]+=Jinfo[P][4]-Jinfo[P][2]
        Jinfo['Pot']+=Jinfo[P][2]-Jinfo[P][4]
        Jinfo['Hmise']=Jinfo[P][2]
        Jinfo[P][5]+=Jinfo[P][2]-Jinfo[P][4]
        Jinfo[P][4]=Jinfo[P][2]
    if a=='P':
        print(P,a)
        if Jinfo['Hmise']<=Jinfo[P][0]:
            Jinfo[P][0]=Jinfo[P][0]-Jinfo['Hmise']+Jinfo[P][4]
            Jinfo['Pot']+=Jinfo['Hmise']-Jinfo[P][4]
            Jinfo[P][5]+=Jinfo['Hmise']-Jinfo[P][4]
            Jinfo[P][4]=Jinfo['Hmise']
        else:
            Jinfo[P][4]+=Jinfo[P][0]
            Jinfo[P][5]+=Jinfo[P][0]
            Jinfo['Pot']+=Jinfo[P][0]
            Jinfo[P][0]=0

def reset_Ac():
    global Jinfo
    for i in Jinfo['JnP']:
        Jinfo[i][1]=False

def manche():
    global Jinfo
    Jinfo['JnF']=[]
    for i in Jinfo['JnP']:
        Jinfo['JnF'].append(i)
    Jinfo['R']='C'
    Jinfo['C']=False
    m0()
    BB=BBF()
    Jinfo['Hmise']=BB
    print(Jinfo['Hmise'])
    asyncio.run(notify_Jinfo())

    a=accord_Ac()
    time.sleep(1)
    if a=='AF':
        Jinfo['V']=Jinfo['JnF'][0]
    Jinfo['R']='3'
    Jinfo['C']=True
    Jinfo['PR']=''
    Jinfo['Hmise']=0
    m0()
    asyncio.run(notify_Jinfo())

    a=accord_Ac()
    time.sleep(1)
    if a=='AF':
        Jinfo['V']=Jinfo['JnF'][0]
    Jinfo['R']='4'
    Jinfo['C']=True
    Jinfo['PR']=''
    Jinfo['Hmise']=0
    m0()
    asyncio.run(notify_Jinfo())

    a=accord_Ac()
    time.sleep(1)
    if a=='AF':
        Jinfo['V']=Jinfo['JnF'][0]
    Jinfo['R']='5'
    Jinfo['C']=True
    Jinfo['PR']=''
    Jinfo['Hmise']=0
    m0()
    asyncio.run(notify_Jinfo())

    a=accord_Ac()
    if a=='AF':
        Jinfo['V']=Jinfo['JnF'][0]
    Jinfo['R']='J'
    Jinfo['EAJ']="Crien"
    print(Jinfo['EAJ'])
    print()
    comp()
    asyncio.run(notify_Jinfo())


def deroulement():
    global Jinfo
    Jinfo['Md']=time.localtime()[4]
    creer_Jinfo()
    while len(Jinfo['JnP'])>1:
        dist()
        reset_Ac()
        manche()
        argentG()
        elim()
        J1()
        time.sleep(5)
        Jinfo['R']='RST'
        asyncio.run(notify_Jinfo())
    Jinfo['V']=Jinfo['JnP']
    asyncio.run(notify_Jinfo())



def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


async def notify_Jinfo():
    global Jinfo
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = json.dumps(Jinfo)
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])
        await notify_Jinfo()


async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


async def Ac(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            if data["action"]=="F":
                print(Jinfo['EAJ'],'F')
                Jinfo[Jinfo['EAJ']][1]='F'
                await notify_Jinfo()
            elif data["action"]=="C":
                print(Jinfo['EAJ'],'C')
                Jinfo[Jinfo['EAJ']][1]='C'
                await notify_Jinfo()
            elif data["action"]=="P":
                Gmise(Jinfo['EAJ'],'P')
                Jinfo[Jinfo['EAJ']][1]='P'
                await notify_Jinfo()
            elif data["action"]=="R":
                Jinfo[Jinfo['EAJ']][2]=int(data['amount'])
                Gmise(Jinfo['EAJ'],'R')
                Jinfo[Jinfo['EAJ']][1]='R'
                Jinfo['C']=False
                await notify_Jinfo()
            elif data["pseudo"]!=False:
                Jinfo["JnP"].append(data["pseudo"])
#                Jinfo["NNP"].append(data["NP"])
                Jinfo['P']=True
                await notify_Jinfo()
                Jinfo['P']=False
            elif data["admin"]=="start":
                thread1.start()
                await notify_Jinfo()
            else:
                logging.error("unsupported event: {}", data)
    finally:
        await unregister(websocket)

c=0
Jinfo={"type":"J",'Vadmin':False,'JnP':[],'NNP':[],'ct':[99,99,99,99,99],'EAJ':'','V':'',"Crien":[0,''],'niv':-1}
thread1 = myThread(1, "Thread-1", 1)

#all fold n'est pas fait donc compare les cartes alors que pas besoin //// quinte problème //// all in reste qu'une personne  /// Ac_accord /// spec mod //// qd il y a 1 mort
#argent en - après all in


logging.basicConfig()

STATE = {"value": 0}

USERS = set()

start_server = websockets.serve(Ac, "localhost", 23614)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
