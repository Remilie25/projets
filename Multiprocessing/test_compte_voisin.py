#Auteur : Remi De Pretto
#Date : 15/06/24
#Ce programme ne sert qu'a afficher l'aide de compte_voisin_en_vie du prorame game_of_life.py

from random import randint


dico = {0:'normal', 1:'centre ville', 2:'coin avec un seul quartier juxtapose de q=0',
        3:'coin avec un seul quartier juxtapose de q=1',
        4:'coin avec un seul quartier juxtapose de q=2',
        5:'coin avec un seul quartier juxtapose de q=3',
        6:'bord de la ville haut', 7:'bord de la ville gauche',
        8:'bord de la ville bas', 7:'bord de la ville droit',
        10:'coin de la ville',
        11:'bord interne horizontal', 12:'bord de la ville vertical'}

def compte_voisin_en_vie(ville, quartier, i, j):
    '''Cette fonction compte le nbr de voisin en vie.'''

    demi_long = len(ville[quartier]) - 1

    #-----Cas general-----
    if 0 < i < demi_long and 0 < j < demi_long:
        ville[quartier][i][j] = 0
        return
        
    #-----Cas particuliers-----
    #bords de la ville frontalier avec un autre quartier
    elif i in (0,demi_long) and j in (0,demi_long):
        if quartier == 0:
            if (i,j) == (0,0):
                ville[quartier][i][j] = 10
                return
            elif (i,j) == (0,demi_long):
                ville[quartier][i][j] = 2
                return
            elif (i,j) == (demi_long,0):
                ville[quartier][i][j] = 2
                return
            elif (i,j) == (demi_long, demi_long):
                ville[quartier][i][j] = 1
                return
            
        elif quartier == 1:
            if (i,j) == (0,0):
                ville[quartier][i][j] = 3
                return
            elif (i,j) == (demi_long,demi_long):
                ville[quartier][i][j] = 3
                return
            elif (i,j) == (demi_long, 0):
                ville[quartier][i][j] = 1
                return
            elif (i,j) == (0,demi_long):
                ville[quartier][i][j] = 10
                return

        elif quartier == 2:
            if (i,j) == (0,0):
                ville[quartier][i][j] = 4
                return
            elif (i,j) == (demi_long,demi_long):
                ville[quartier][i][j] = 4
                return
            elif (i,j) == (0, demi_long):
                ville[quartier][i][j] = 1
                return
            elif (i,j) == (demi_long,0):
                ville[quartier][i][j] = 10
                return

        elif quartier == 3:
            if (i,j) == (0,demi_long):
                ville[quartier][i][j] = 5
                return
            elif (i,j) == (demi_long,0):
                ville[quartier][i][j] = 5
                return
            elif (i,j) == (0, 0):
                ville[quartier][i][j] = 1
                return
            elif (i,j) == (demi_long,demi_long):
                ville[quartier][i][j] = 10
                return
    
    #bords de la ville
    elif i==0 and (quartier in (0,1)):
        ville[quartier][i][j] = 6
        return

    elif j == 0 and quartier in (0,2):
        ville[quartier][i][j] = 7
        return

    elif i == demi_long and quartier in (2,3):
        ville[quartier][i][j] = 8
        return

    elif j == demi_long and quartier in (1,3):
        ville[quartier][i][j] = 9
        return

    #bords interne des quartiers
    elif (i == demi_long and quartier in (0,1)) or (i == 0 and quartier in (2,3)):
        ville[quartier][i][j] = 11
        return

    elif (j == demi_long and quartier in (0,2)) or (j == 0 and quartier in (1,3)):
        ville[quartier][i][j] = 12
        return
    

    ville[quartier][i][j] = -1
    return



def test(demi_long = 10):
    Nbr_quartier = 4
    ville = [[[-1 for _ in range(demi_long)]
              for l in range(demi_long)] for q in range(Nbr_quartier)]
    
    for quartier in range(4):
        for i in range(-1, demi_long):
            for j in range(-1, demi_long):
                try:
                    compte_voisin_en_vie(ville, quartier, i, j)
                except:
                    continue

    print("test fini")
    return ville


def affiche_quartier(v, q):
    for i in range(len(v[q])):
        for j in range(len(v[q])):
            if 0 <= v[q][i][j] < 10:
                separation = ' '
            else:
                separation = ''
            print(separation, v[q][i][j], end=' ')
        print()

        
def affiche_ville(v):
    demi_long = len(v[0])
    
    for i in range(2 * demi_long):
        q = 2 * (i // demi_long)
        x = i % demi_long
        
        for j in range(2 * demi_long):
            y = j % demi_long

            if j == demi_long:
                q +=1
                
            if 0 <= v[q][x][y] < 10:
                separation = ' '
            else:
                separation = ''
            print(separation, v[q][x][y], end=' ')
        print()
