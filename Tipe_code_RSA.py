from secrets import randbelow
import math
from random import randint

def est_premier_naif(n):
    """teste si n est premier en O(n)"""
    for i in range(2,n):
        if n%i==0:
            return False
    return True

def est_premier_naif_2(n):
    """teste si n est premier en O(n^(1/2))"""
    for i in range(2,int(math.sqrt(n))):
        if n%i==0:
            return False
    return True

def initialisation_D(iteration=100000):
    D['Dmax']=2
    D[0]=False
    D[1]=False
    D[2]=True
    def init_dico(n):
        m=D['Dmax']
        for i in range(2,m+1):
            if D[i]:
                if n%i==0:
                    D[n]=False
                    return
        for i in range(m+1,int(math.sqrt(n))):
            if n%i==0:
                D[n]=False
                return
        D[n]=True
    for i in range(iteration):
        init_dico(i)
        D['Dmax']+=1

def est_premier_dico(n):
    m=D['Dmax']
    if m>n:
        return D[n]
    else:
        for i in range(2,m+1):
            if D[i]:
                if n%i==0:
                    D[n]=False
                    return False
        for i in range(m+1,int(math.sqrt(n))):
            if n%i==0:
                D[n]=False
                return False
    D[n]=True
    return True

'''def exponentiation_rapide(x,n):
    r,y,m=1,x,n
    while m>0:
        y*=y
        if m%2==1:
            r*=y
        m//=2
    return r'''

def expo_rapide(x,n):
    if n==0:
        return 1
    else:
        if n%2==0:
            return expo_rapide(x*x,n//2)
        else:
            return x*expo_rapide(x*x,n//2)

def pgcd(a,b):
    '''calcul le pgcd de a et b deux entiers naturels'''
    def aux(a,b):
        if b==1:
            return 1
        elif b==0:
            return a
        else:
            return aux(b,a%b)
    if b==0:
        return a
    elif b==1:
        return 1
    else:
        if a<b:
            return aux(b,a)
        else:
            return aux (a,b)

def test(n):
    for i in range(n):
        print(i,D[i])

def genere_premier(mini,rang):
    n=randbelow(rang)+mini
    while not(est_premier_dico(n)):
        n=randbelow(rang)+mini
    return n

def genere_ed(phin):
    e=random(phin-2)+2
    while pgcd(e,phin)!=1:
        e=random(phin-2)+2
        d=random(phin-2)+2
    while ((e*d)%phin)!=1:
        d=random(phin-2)+2
    return e,d

def RSA_generation_cles(est_premier,random,emin=1):
    """genere les cles"""
    mini=expo_rapide(2,emin)
    rang=expo_rapide(2,25)
    def genere_premier():
        n=random(rang)+mini
        c=1
        while not(est_premier(n)):
            n=random(rang)+mini
            c+=1
        return n
    def genere_ed(phin):
        e=random(phin-2)+2
        while pgcd(e,phin)!=1:
            e=random(phin-2)+2
        d=random(phin-2)+2
        while ((e*d)%phin)!=1:
            d=random(phin-2)+2
        return e,d
    p,q=genere_premier(),genere_premier()
    n,phin=p*q,(p-1)*(q-1)
    e,d=genere_ed(phin)
    return (e,n),(d,n)

##
def expo_mod(x,n,p):
    """calcul x^n [p]"""
    if n==0:
        return 1
    else:
        if n%2==0:
            return (expo_mod((x*x)%p,n//2,p))%p
        else:
            return (expo_mod((x*x)%p,n//2,p)*x)%p

def est_premier_pgp(N):
    """determine si N premier si N passe le test de fermat pour 2,3,5,7"""
    L=[expo_mod(i,N-1,N) for i in range(3,8,2)]
    L.append(expo_mod(2,N-1,N))
    if L==[1,1,1,1]:
        return True
    return False

def temoin(N,a,m,s):
    n=expo_mod(a,m,N)
    if n==1:
        return False
    else:
        for d in range(s):
            n=expo_mod(n,m,N)
            if n==N-1:
                return False
            n=(n*n)%N
    return True

def miller_rabin(N):
    m=N
    s=0
    while m%2==0:
        m//=2
        s+=1
    for _ in range(30):
        a=randint(1,N-1)
        if temoin(N,a,m,s):
            return False
    return True

def middle_square(n,seed):
    """PRNG, seed sur n chiffre, n pair"""
    d=expo_rapide(10,n//2)
    r=(seed**2)//d
    d**=2
    return r-(r//d)*d

def t_midsquare():
    print('n=2 : ',middle_square(2,10)==10,middle_square(2,50)==50,middle_square(2,60)==60,middle_square(2,24)==57,middle_square(2,57)==24)
    print('n=4 : ',middle_square(4,100)==100,middle_square(4,2500)==2500,middle_square(4,7600)==7600,middle_square(4,3792)==3792)

## Fortuna : preface
import hashlib
import time

def hash(n):
    h=hashlib.sha3_256()
    h.update(n)
    return h.hexdigest()

def hash_hex(n):
    h=hashlib.sha3_256()
    h.update(n)
    return h.digest()

def encryption_sym(cle,m): #obselete voir blowfish
    '''version provisoire, version actuelle Blowfish'''
    r=""
    for x in str(m):
        #print(cle)
        r+=chr((ord(x)+int(cle,16))%8364) # 8364 dernier chr en base 10.
    return r

def n_to_string(c): #obselete
    y=c//16
    r=str(c%16)
    while y>0:
        r=chr(y%16)+r
        y//16
    return r

def celling(a,b):
    '''renvoie l'entier superieur le plus petit de a/b'''
    c=a//b
    if a%b!=0:
        c+=1
    return c

## Fortuna : la cle est sur 32 octects et n sur 16 octects

#Structure de Fortuna :
#Fortuna dictionnaire global
#'pool1', ... , 'pool31' : <class 'bytes'>
#'Gen' : dictionnaire -> {'cle': int sur 32 octects, 'n': int sur 16 octects}
#'n_reseed' : int
#'reseed_time' : int
#'b_reseed' : bool

def F_init_gen():
    '''initialise le generateur, etat Generateur[n]=0 signifie que le generateur n'a pas recu de graine ; n est un compteur'''
    Generateur={'cle':0,'n':0}
    return Generateur

def F_reseed(seed):
    '''change la graine du generateur avec seed : <class 'bytes'>'''
    Gen=Fortuna['Gen']
    Gen['cle'],Gen['n']=int.from_bytes(hash_hex(Gen['cle'].to_bytes(32,'little')+seed),'little'),(Gen['n']+1)%expo_rapide(2,128)
    Fortuna['b_reseed']=True

def F_gen_blocks(k):
    '''genere k blocks : int, 1 blocs=128 bits, "private"'''
    Gen=Fortuna['Gen']
    assert Gen['n']!=0,"le generateur n'a pas recu de graine"
    if Fortuna['b_reseed']:
        B_precalculs(Gen['cle'])
        Fortuna['reseed']=False
    blocks=0
    c=expo_rapide(2,128)
    decalage=1
    for _ in range(k):
        blocks+=Blowfish_chiffrement_128_bits(Gen['n'])*decalage
        decalage*=c
        Gen['n']+=1
    return blocks

def F_gen_octects(Gen,n):
    '''genere n octects "aleatoirement" '''
    assert 0<=n<=expo_rapide(2,20)
    n2=celling(n,16)
    r=F_gen_blocks(n2)
    Gen['cle']=F_gen_blocks(2)
    return r

def F_init():
    global Fortuna
    Fortuna={}
    for i in range(32):
        Fortuna['pool'+str(i)]=b''
    Fortuna['Gen']=F_init_gen()
    Fortuna['n_reseed']=0
    Fortuna['reseed_time']=0
    Fortuna['b_reseed']=False


def F_hasard(n):
    '''Page 153'''
    MinPoolLen=63
    if len(Fortuna['pool0'])>MinPoolLen and (time.perf_counter_ns()-Fortuna['reseed_time'])>100000:
        Fortuna['n_reseed']+=1
        s=b''
        for i in range(32):
            if Fortuna['n_reseed']%expo_rapide(2,i)==0:
                s+=hash_hex(Fortuna['pool'+str(i)])
                Fortuna['pool'+str(i)]=b''
        Fortuna['reseed_time']=time.perf_counter_ns()
        F_reseed(s)
        print(time.perf_counter_ns()-Fortuna['reseed_time'])
        extract_vmstat(MinPoolLen) #sur un autre thread
    if Fortuna['Gen']['n']==0:
        print("GenErreur : le generateur n'a pas de graine !")
    else:
        return F_gen_octects(Fortuna['Gen'],n)

def F_add_event(s,i,e):
    '''ajoute un evenement e pour augmenter l'entropie recuperee, s : source_id, i : pool_id'''
    assert 0<len(e)<33 and -1<s<256 and -1<i<33, "Probleme l'entree n'est pas correcte"
    Fortuna['pool'+str(i)]+=s.to_bytes(1,'little')+len(e).to_bytes(1,'little')+e


#arret "fixer" les type pour Fortuna + Pb iteration de F_hasard + source ? avant ecrits

#Pb: encrypt sym + bits pertinents pour sources + pool en octects or extr_vm en bits + C:16-bytes
#      v16/05                            v 15/05                         v 15/05

#Pb: C en string par str ou chr + bytes en ascii ou utf8
#    v to_bytes equiv a chr 17/05       v utf8 16/06

#Pb: mieux concat data ou ajout direct pour extract_vm -> pour le moment si >=4 ok
#

#Pb: len(e) en bytes ou en bits ?
#

##entropie

def testos(l):
    f=open("/proc/meminfo")
    print(f.readlines()[l])
    f.close()

def testos2(n,l,t=1):
    for _ in range(n):
        testos(l)
        time.sleep(t)

def init_occ(t=1):
    f=open("/proc/vmstat","r")
    L,V=(f.readline()[:-1]).split(" ")
    for i in f.readlines():
        a,b=i.split(" ")
        L+=";"+a
        V+=";"+b[:-1]
    f.close()
    occ=open("occurences"+str(t)+".txt","x")
    occ.write(L+'\n'+V+'\n')
    occ.close()

def itere_hopper(n,t=1):
    occ=open("occurences"+str(t)+".txt",'a')
    for i in range(n):
        f=open("/proc/vmstat","r")
        V=(f.readline().split(" "))[1][:-1]
        for i in f.readlines():
            V+=";"+i.split(" ")[1][:-1]
        f.close()
        occ.write(V+'\n')
        time.sleep(t)
    occ.close()

def analyse(t=1):
    '''ecrit les lignes ayant au moins n nombres diff'''
    occ=open("occurences"+str(t)+".txt",'r')
    name=occ.readline().split(";")
    D={}
    for i in range(len(name)):
        D[i]=[]
    for i in occ.readlines():
        L=i.split(";")
        for j in range(len(L)):
            if not L[j] in D[j]:
                D[j].append(L[j])
    occ.close()
    R=open("result_analyse"+str(t)+".txt",'a')
    for i in range(len(name)):
         R.write(name[i]+":"+str(len(D[i]))+'\n')
    R.close()

def analyse_fine(i,n,t=1):
    f=open("/proc/vmstat","r")
    a=f.readlines()[i][:-1].split(" ")
    print(a[0],a[1],sep="\n")
    f.close()
    time.sleep(t)
    for j in range(n-1):
        f=open("/proc/vmstat","r")
        print(f.readlines()[i].split(" ")[1][:-1])
        f.close()
        time.sleep(t)

#pt faire des itere_hopper plus freq ? Attention car l'ecriture peut perturber

#truc a test
#/proc/diskstats
#ping www.google.com parite
#/proc/vmstat

#gros candidat : activite de fond = Spotify x val diff sur 51 test f=2Hz,
#notat: varie bcp=vb; vm; vp; ptlc=pas a tt les coups; sc=strict; 100%=diff chaque fois croiss; x%
#les candidats >=40 avec analyse_fine(i,100,0.1):
#1 nr_zone_inactive_anon 49 vb ptlc vp NOT(sc)
#15 numa_local 51 100% f=10Hz sc vm
#17 nr_inactive anon 49 vb ptlc sc vp
#34 nr_anon_page 47 varie trop lentement et sc
#64 pgalloc_normal 51 100% sc vm
#74 pgfree 51 100% sc vm
#75 pgactivate 51 100% vp
#78 pgfault 51 100% vp
#82 pgreuse 40 10% vp


def puissance_2(n):
    '''renvoie sur combien de bits on peut ecrire n (min), pour 0 renvoie 0'''
    x=1
    c=0
    while x-1<n:
        x*=2
        c+=1
    return c

premiers_32=[1+i for i in range(0,32,2)]

def prod_mod(x,n,p):
    """calcul x*n [p]"""
    if n==0:
        return 0
    else:
        if n%2==0:
            return (prod_mod((x+x)%p,n//2,p))%p
        else:
            return (prod_mod((x+x)%p,n//2,p)+x)%p

def pool_id(s,c):
    '''donne le pool_id de maniere cyclique et dependant de s la source'''
    p=premiers_32[s%16]
    return prod_mod(p,c,32)

def extract_vmstat(k):
    '''extrait des bits de vmstat parmis les stats les + instables tant que objectif buffer pas atteint'''
    #global bool_buffer   -> condition tant que len(pool0)<MinPoolLen
    L=[1,15,17,34,64,74,75,78,82]   #liste des lignes "interessantes" dans vmstat
    D={i:0 for i in L}              #dico des dernieres valeurs
    C={i:0 for i in L}              #dico des compteur d'ajout
    Temp={i:[0,0] for i in L}       #dico des bits en attente
    bool_buffer=True
    while bool_buffer:
        vms=open("/proc/vmstat","r")
        for i in range(len(L)):
            if i==0: d=L[i]
            else: d=L[i]-L[i-1]-1
            for _ in range(d):
                vms.readline()
            temp=int(vms.readline().split(" ")[1][:-1])   #prend la valeur de L[i] et la stocke
            delta=puissance_2(abs(D[L[i]]-temp))
            if D[L[i]]!=temp and delta>2:
                D[L[i]]=temp
                r=temp%(expo_rapide(2,delta-2))
                if delta-2+Temp[L[i]][0]>4:
                    r=r*expo_rapide(2,Temp[L[i]][0])+Temp[L[i]][1]
                    F_add_event(i,pool_id(i,C[L[i]]),r.to_bytes(celling(Temp[L[i]][0]+delta-2,8),'little'))
                    Temp[L[i]]=[0,0]
                else:
                    Temp[L[i]][1]=r*expo_rapide(2,Temp[L[i]][0])+Temp[L[i]][1]
                    Temp[L[i]][0]+=delta-2
                C[L[i]]+=1
        if len(Fortuna['pool0'])>k:
            bool_buffer=False



#(t:int).to_bytes(1,'little')
#int.from_bytes( (t:<class 'bytes'>) ,'little')

##Blowfish

def init_P_and_S_old():
    '''initialise P et S avec les decimals de pi, pas fini car pas content'''
    pi=open("PiHex.txt","r")
    P=[]
    S=[]
    for _ in range(4):
        l=pi.readline()
        b=bytes(0)
        for i in range(4):
            for j in range(8):
                b+=bytes(chr(int(l[8*i+j])),'utf8')
            P.append(b)
        raccord=pi.readline()
        b=bytes(0)
        for i in range(2):
            for j in range(8):
                b+=bytes(chr(int(l[8*i+j])),'utf8')
            P.append(b)
    pi.close()
    return P

def init_P_and_S():
    '''initialise P et S avec les decimals de pi, constants'''
    pi=open("PiHex.txt","r")
    global P,S
    P=[]
    S=[[] for _ in range(4)]
    for _ in range(2):
        l=pi.readline()
        b=''
        for i in range(8):
            P.append(int(l[8*i:8*i+9],16))
    raccord=pi.readline()
    for i in range(2):
        P.append(int(raccord[8*i:8*i+9],16))
    for s in range(4):
        for i in range(2,8):
            S[s].append(int(raccord[8*i:8*i+9],16))
        for _ in range(31):
            l=pi.readline()
            for i in range(8):
                S[s].append(int(l[8*i:8*i+9],16))
        raccord=pi.readline()
        for i in range(2):
            S[s].append(int(raccord[8*i:8*i+9],16))
    pi.close()
    return

def premier_n_bits(x,n): #ne sert pas -> faire direct par x//2**n
    '''renvoie les n premiers bits de x avec le poids faible devant'''
    xf=0
    y=1
    z=x
    for i in range(n):
        xf+=y*(z%2)
        z//=2
        y*=2
    return xf

def feistel(x):
    '''x int sur 32 bits'''
    global Sc
    c=0x100000000 #=2**32 constante
    x_0=x%256          #decompose x sur 4*8 bits
    x_1=(x//256)%256
    x_2=(x//256**2)%256
    x_3=(x//256**3)%256
    return ((((Sc[0][x_0]+Sc[1][x_1])%c)^Sc[2][x_2])+Sc[3][x_3])%c

def B_chiffrement_blocs(x):
    '''x int sur 64 bits'''
    global Pc
    c=0x100000000 #=2**32 constante
    x_faible=x//c
    x_fort=x//c
    for i in range(16):
        x_faible^=Pc[i]
        x_fort^=feistel(x_faible)
        x_faible,x_fort=x_fort,x_faible
    x_faible,x_fort=x_fort,x_faible
    x_fort^=Pc[16]
    x_faible^=Pc[17]
    return x_fort*c+x_faible


def B_precalculs(cle):
    '''precalcul afin que l'encryption soit possible, cle : int sur 256 bits'''
    c=0x100000000 #=2**32 constante
    plaintext=0
    global Pc,Sc
    Pc=P[:]
    Sc=[l[:] for l in S]
    t_cle=[(cle//expo_rapide(c,i))%c for i in range(8)]
    for i in range(18):
        Pc[i]^=t_cle[i%8]
    for s in range(4):
        for i in range(256):
            Sc[s][i]^=t_cle[i%8]
    for i in range(9):
        plaintext=B_chiffrement_blocs(plaintext)
        Pc[2*i],Pc[2*i+1]=plaintext%c,plaintext//c
    for s in range(4):
        for i in range(128):
            plaintext=B_chiffrement_blocs(plaintext)
            Sc[s][2*i],Sc[s][2*i+1]=plaintext%c,plaintext//c


def Blowfish_chiffrement(message):
    '''chiffre le message : int par la cle actuelle stockee dans Pc,Sc globaux'''
    c=0x10000000000000000 #=2**64 constante
    y=message
    z=1
    s=0
    while y>0:
        s+=B_chiffrement_blocs(y%c)*z
        y//=c
        z*=c
    return s

def Blowfish_chiffrement_128_bits(block):
    c=0x10000000000000000 #=2**64 constante
    b_0=block%c
    b_1=block//c
    return B_chiffrement_blocs(b_0)+B_chiffrement_blocs(b_1)*c

def test_sur_32(L):
    c=0x100000000 #=2**32 constante
    for x in L:
        if c<x:
            return False
    return True

def F_clone(Fortuna):
    F={i:Fortuna[i] for i in Fortuna.keys()}
    F['Gen']=Fortuna['Gen'].copy()
    return F

Fortuna_0={'pool0': b'\x00\x02H\x88\x01\x03lB\x07\x02\x02H\x88\x03\x02\x13f\x04\x03\x84\x9b\x07\x05\x03P\xeb\x1b\x06\x02s\x04\x07\x03EU\x07\x08\x02\t\xb0\x05\x01\t\x04\x01\x03\x07\x01t\x08\x01\x15\x07\x01\xa8\x05\x01\x0f\x00\x01\xed\x02\x01\xed', 'pool1': b'\x05\x01\r\x07\x01\x00\x01\x01\x0e\x04\x01\x17\x04\x01:\x01\x01\x0e', 'pool2': b'\x00\x01\x89\x04\x01\x00\x04\x01Z\x01\x01\x07\x07\x01\x1f\x08\x01\x03\x07\x01+\x04\x01V\x02\x01\x87\x03\x01e', 'pool3': b'\x01\x01)\x01\x01\x00\x04\x01\x0e\x01\x01\x11\x07\x01\x01\x08\x01:\x01\x02a\x00', 'pool4': b'\x00\x01\x89\x08\x01\x07\x07\x01\x1a\x04\x01>\x02\x01!\x07\x01\n', 'pool5': b'\x05\x01\x1f\x01\x01\x00\x07\x01\x0c\x01\x01\x18\x04\x01\x05\x08\x01\x02\x01\x019\x04\x01\x11', 'pool6': b'\x00\x01\x89\x05\x01\x1f\x02\x02\xca\x01\x01\x01\x03\x03\x01!\x04\x01\x0e\x07\x01\x13', 'pool7': b'\x04\x01\x00\x01\x01\x02\x08\x01\x13\x03\x01\x18\x08\x01\x17\x04\x01\x07', 'pool8': b"\x01\x01\x10\x05\x01\x98\x00\x01\x89\x02\x01\x89\x07\x01\x16\x07\x01'", 'pool9': b'\x04\x01"\x01\x01,\x04\x01\x00\x01\x01\x04\x01\x01\x01\x05\x018\x08\x01A\x08\x01\x1b\x04\x02\xe9\x01\x01\x01\x17', 'pool10': b'\x04\x01\x02\x02\x01\x89\x05\x01?\x00\x01\x89\x08\x01\x1c\x01\x01\x0c\x01\x01\x1c\x05\x01\x1d\x04\x01\x1f\x07\x01\x1c\x03\x01\xed\x01\x01\x1c', 'pool11': b'\x07\x01\x1b\x08\x01\x0b\x01\x01\xb2', 'pool12': b'\x07\x01\x08\x00\x01\x99\x07\x02x\x00\x08\x01\x12\x01\x01>\x04\x01\x06\x07\x01\n\x02\x01\xa9', 'pool13': b'\x04\x01\x00\x01\x01\x00\x04\x01s\x04\x01\x0c\x08\x01\xe5\x07\x01\x0f\x04\x01J', 'pool14': b'\x05\x01\x1f\x01\x01z\x01\x01\x0b\x07\x01\x1d\x00\x02\xca\x01\x01\x01\x07\x08\x016\x02\x01C\x07\x010\x01\x01\x02', 'pool15': b'\x01\x01\x00\x01\x012\x04\x01\x00\x05\x01\x1f\x01\x01\x0c\x08\x02E\x01\x04\x01\x18\x08\x01\x1e\x01\x01B\x07\x01\x1e', 'pool16': b'\x07\x01I\x00\x01\xed\x02\x01\xed\x08\x01\xf9\x07\x015\x03\x01\x87', 'pool17': b'\x04\x01\x18\x08\x01\x18\x01\x01\t\x04\x01\x1a\x08\x01\x10\x07\x01\x0b', 'pool18': b'\x02\x01\x89\x07\x01\x1c\x00\x01\x0f\x04\x01\x03\x01\x01\x00\x07\x02\xa3\x01', 'pool19': b'\x05\x02\x19\x00\x01\x01h\x04\x01\x02\x01\x010\x08\x01\x11\x04\x01\x10\x07\x01\x18', 'pool20': b'\x04\x01\x00\x01\x01\n\x02\x01\x89\x05\x01<\x01\x01\x00\x08\x01\x01\x07\x01\x00\x00\x01!\x07\x01|\x04\x01(\x03\x01C', 'pool21': b'\x08\x01\x11\x04\x01\x02\x01\x01\x14\x08\x01\x03\x03\x01\xa9\x07\x01\x02\x01\x01\x12', 'pool22': b'\x07\x01\t\x05\x01\x14\x01\x01\x00\x01\x01\n\x07\x01\xb1\x04\x01\x08\x00\x01C\x07\x019\x02\x01\xcb', 'pool23': b'\x05\x01\x00\x04\x01\xaa\x07\x01\x1c\x01\x01\x15\x08\x01\r\x01\x01\r\x07\x01\x0c\x04\x01\x1d\x01\x014\x04\x010', 'pool24': b'\x04\x01\x00\x05\x01\x1f\x07\x01z\x03\x01\x0f\x07\x01\x1c\x00\x01e\x02\x01e\x04\x01\x17', 'pool25': b'\x04\x01`\x08\x01\x11\x07\x01\x0f\x01\x01\x0c', 'pool26': b'\x04\x01\x00\x04\x01\x16\x07\x01\x1c\x02\x01\x0f\x07\x01\x94\x00\x01\x87', 'pool27': b'\x04\x01\x1c\x01\x01\x18\x04\x01\x04\x04\x01\t\x07\x01\x07\x01\x01\x12\x04\x01/', 'pool28': b'\x05\x01\x03\x01\x01\x00\x04\x01\x02\x04\x01\x00\x04\x01\n\x02\x01\x99\x07\x01\x16\x03\x01\x1c\x07\x01\x1a\x08\x01\x17\x00\x01\xa9', 'pool29': b'\x01\x01(\x04\x01\x1f\x05\x01?\x04\x018\x01\x01\x0c\x01\x01/', 'pool30': b'\x01\x01\x00\x05\x013\x02\x01\x89\x04\x01\x0c\x07\x01\x08\x01\x01\x16\x04\x01\x1c\x07\x01\xf1\x00\x01\xcb\x03\x01\xa9', 'pool31': b'\x08\x01\x1b\x04\x01\x14\x01\x018\x07\x01\x0f\x04\x01\n\x01\x015', 'Gen': {'cle': 0, 'n': 0}, 'n_reseed': 0, 'reseed_time': 0, 'b_ressed': False}

def lenteur(k):
    t_0=time.perf_counter_ns()
    F_hasard(k)
    t_1=time.perf_counter_ns()
    return t_0,t_1,t_1-t_0,(t_1-t_0)//1000000

def cesar(m):
    r=""
    c=ord('a')
    for x in m:
        r+=chr((ord(x)+3-c)%26+c)
    return r


def a_dicho(a,n):
    g,d=0,100
    y=n
    c=expo_rapide(a,d)
    while y%c==0:
        y//=c
        g=d
        d*=d
        c=expo_rapide(c,d-1)
    while d-g>1:
        m=(d+g)//2
        c=expo_rapide(a,(d-g)//2)
        if y%c==0:
            g=m
            y//=c
        else:
            d=m
    return g

# def AKS(n):
#     i=2
#     while i<sqrt(n):
#         if n==expo_rapide(i,a_dicho(i,n)):
#             return False

