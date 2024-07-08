#Auteur : Remi De Pretto
#Date : 15/06/24
#Ceci est une implementation du jeu de la vie (Game of life) en parrallele.

# Quelques codes d'échappement (tous ne sont pas utilisés)
CLEARSCR="\x1B[2J\x1B[;H"          #  Clear SCReen
CLEAREOS = "\x1B[J"                #  Clear End Of Screen
CLEARELN = "\x1B[2K"               #  Clear Entire LiNe
CLEARCUP = "\x1B[1J"               #  Clear Curseur UP
GOTOYX   = "\x1B[%.2d;%.2dH"       #  ('H' ou 'f') : Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"             #  effacer après la position du curseur
CRLF  = "\r\n"                     #  Retour à la ligne

# VT100 : Actions sur le curseur
CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible

# VT100 : Actions sur les caractères affichables
BOLD = "\x1B[1m"                    #  Gras


# VT100 : Couleurs : "22" pour normal intensity
CL_WHITE="\033[01;37m"                  #  Blanc

#-------------------------------------------------------
import multiprocessing as mp
import os,math, sys, ctypes, signal
from random import randint
from time import sleep


def effacer_ecran() : print(CLEARSCR,end='')
def erase_line_from_beg_to_curs() : print("\033[1K",end='')
def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')
def move_to(lig, col) : print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def en_couleur(Coul) : print(Coul,end='')
def en_rouge() : print(CL_RED,end='') # Un exemple !
def erase_line() : print(CLEARELN,end='')

#Fonctions pour le GOL

def prochain_etat(en_vie, nbr_voisin):
    '''Cette fonction decrit les regles du jeu de la vie'''

    if en_vie:

        if nbr_voisin < 2:
            return False
        
        elif nbr_voisin < 4:
            return True
        
        return False

    if nbr_voisin == 3:
        return True

    return False


def compte_quartier(L, i, j, k_range, l_range):
    '''Cette fonction compte le nombre de True autour de i,j (exclu) dans un meme quartier'''
    
    #Initialisation du compteur
    if L[i][j]:
        n = -1
    else:
        n = 0
    
    for k in range(*k_range):
        for l in range(*l_range):
            if L[i + k][j + l]:
                n += 1
    return n


def compte_bord(ville, quartier, i, j, k_range, l_range):
    '''Cette fonction compte le nombre de True autour de i,j (exclu)'''

    demi_long = len(ville[quartier]) - 1
    
    #Initialisation du compteur
    if ville[quartier][i][j]:
        n = -1
    else:
        n = 0
    
    for k in range(*k_range):
        for l in range(*l_range):
            #Cas general puis 4 cas particuliers
            x = i + k
            y = j + l
            if (0 <= x <= demi_long and 0 <= y <= demi_long and ville[quartier][x][y]) or (
                x < 0 and 0 <= y <= demi_long and ville[quartier - 2][-1][y]) or (
                demi_long < x and 0 <= y <= demi_long and ville[quartier + 2][0][y]) or (
                y < 0 and 0 <= x <= demi_long and ville[quartier - 1][x][-1]) or (
                demi_long < y and 0 <= x <= demi_long and ville[quartier + 1][x][0]):
                n += 1
    return n


def compte_centre_ville(ville, quartier, i, j):
    '''Cette fonction compte le nbr de voisin dans le centre ville'''

    index_fin = len(ville[quartier]) - 1

    #Initialisation du compteur
    if ville[quartier][i][j]:
        n = -1
    else:
        n = 0
    
    for k in range(-1,2):
        for l in range(-1,2):
            x = i + k
            y = j + l
            q = quartier

            if x < 0:
                q -= 2
                x = -1

            elif index_fin < x:
                q += 2
                x = 0

            if y < 0:
                q -= 1
                y = -1
            
            elif index_fin < y:
                q = quartier + 1
                y = 0

            if ville[q][x][y]:                
                n += 1
    return n


def compte_coin(ville, quartier, i, j):
    '''Cette fonction compte les voisins en vie dans les quatre coins des quartiers'''

    # i et j sont soit a 0 soit a index_fin
    if quartier == 0:
        if i > 0:
            if j > 0:
                return compte_centre_ville(ville, quartier, i, j)
            
            else:
                return compte_bord(ville, quartier, i, j, (-1,2), (0,2))
            
        else:
            if j > 0:
                return compte_bord(ville, quartier, i, j, (0,2), (-1,2))

            else:
                return compte_quartier(ville[quartier], i, j, (0,2), (0,2))

    elif quartier == 1:
        if i > 0:
            if j > 0:
                return compte_bord(ville, quartier, i, j, (-1,2), (-1,1))
            
            else:
                return compte_centre_ville(ville, quartier, i, j)
            
        else:
            if j > 0:
                return compte_quartier(ville[quartier], i, j, (0,2), (-1,1))

            else:
                return compte_bord(ville, quartier, i, j, (0,2), (-1,2))

    elif quartier == 2:
        if i > 0:
            if j > 0:
                return compte_bord(ville, quartier, i, j, (-1,1), (-1,2))
            
            else:
                return compte_quartier(ville[quartier], i, j, (-1,1), (0,2))
            
        else:
            if j > 0:
                return compte_centre_ville(ville, quartier, i, j)

            else:
                return compte_bord(ville, quartier, i, j, (-1,2), (0,2))

    else:
        if i > 0:
            if j > 0:
                return compte_quartier(ville[quartier], i, j, (-1,1), (-1,1))
            
            else:
                return compte_bord(ville, quartier, i, j, (-1,1), (-1,2))
            
        else:
            if j > 0:
                return compte_bord(ville, quartier, i, j, (-1,2), (-1,1))

            else:
                return compte_centre_ville(ville, quartier, i, j)
            


def compte_voisin_en_vie(ville, quartier, i, j):
    '''Cette fonction compte le nbr de voisin en vie. Cette fonction est compliquee car 
       beaucoup de conditions. Elle aurait pu etre simplifiee pour une meilleure comprehension
       et le respect des bonnes pratiques. Mais l'optimisation a primee ! Appelez la fonction
       affiche_ville_aide() pour un peu d'aide.'''

    index_fin = len(ville[quartier]) - 1

    #-----Cas general----- id = 0
    if 0 < i < index_fin and 0 < j < index_fin:
        return compte_quartier(ville[quartier], i, j, (-1,2), (-1,2))
        

    #-----Cas particuliers----- id non nul
    #Les tests sur les quartiers sont effectues en dernier car ils sont
    #moins determinant que la position i,j
    

    #**coin d'un quartier**
    #centre ville (les 4 cases du milieu) || id = 1
    #bords de la ville frontalier avec un autre quartier || id = 2 + quartier
    #coin de la ville id = 10
    elif i in (0,index_fin) and j in (0,index_fin):
        return compte_coin(ville, quartier, i, j)
    
    #**bords de la ville**
    elif i == 0 and quartier in (0,1): #id = 6
        return compte_quartier(ville[quartier], i, j, (0,2), (-1,2))

    elif j == 0 and quartier in (0,2): #id = 7
        return compte_quartier(ville[quartier], i, j, (-1,2), (0,2))

    elif i == index_fin and quartier in (2,3): #id = 8
        return compte_quartier(ville[quartier], i, j, (-1,1), (-1,2))

    elif j == index_fin and quartier in (1,3): #id = 9
        return compte_quartier(ville[quartier], i, j, (-1,2), (-1,1))

    
    #**bords internes des quartiers**
    elif (i == index_fin and quartier in (0,1)) or (i == 0 and quartier in (2,3)): #id = 11
        return compte_bord(ville, quartier, i, j, (-1,2), (-1,2))

    elif (j == index_fin and quartier in (0,2)) or (j == 0 and quartier in (1,3)): #id = 12
        return compte_bord(ville, quartier, i, j, (-1,2), (-1,2))
    

def cellule_evolution(quartier_evolue, ville, quartier, i, j):
    '''Cette fonciton modifie l'etat d'une cellule.'''
    
    quartier_evolue[i][j] = prochain_etat(ville[quartier][i][j], compte_voisin_en_vie(ville, quartier, i, j))


def copie_quartier_sur_ville(ville, quartier, quartier_evo):
    '''Copie la prochaine generation du quartier sur la ville'''

    for ligne in range(len(quartier_evo)):
        for colonne in range(len(quartier_evo)):
            ville[quartier][ligne][colonne] = quartier_evo[ligne][colonne]


def quartier_evolution(ville, quartier, afficher_prochain_tick, calculer_prochain_tick, push_ville_evo, keep_running):
    '''Cette fonction met a jour un quartier du jeu de la vie.'''
    
    demi_long = len(ville[quartier])
    
    while keep_running.value:

        #Affichage a recuperer la ville. Calcul de la generation suivante.
        calculer_prochain_tick.acquire() 

        quartier_evolue = [[0] * demi_long for _ in range(demi_long)]

        for i in range(demi_long):
            for j in range(demi_long):
                cellule_evolution(quartier_evolue, ville, quartier, i, j)

        #Quartier fini. Attente des autres pour ne pas les gener.
        for _ in range(3): push_ville_evo[quartier].release()
        for i in range(4):
            if i != quartier:
                push_ville_evo[i].acquire()

        copie_quartier_sur_ville(ville, quartier, quartier_evolue)

        #Quartier mise a jour. Libere affichage
        afficher_prochain_tick.release()

#----------------------------------------
## Aide pour compte_voisin_en_vie

def affiche_ville_aide():
    '''affiche la ville avec les identifiants de la disjonction de cas.'''
    import test_compte_voisin as tcv
    global demi_longueur_cote

    try:
        (demi_longueur_cote)
    except:
        demi_longueur_cote = 10


    dico = {0:'normal', 1:'centre ville', 2:'coin avec un seul quartier juxtapose de q=0',
            3:'coin avec un seul quartier juxtapose de q=1',
            4:'coin avec un seul quartier juxtapose de q=2',
            5:'coin avec un seul quartier juxtapose de q=3',
            6:'bord de la ville haut', 7:'bord de la ville gauche',
            8:'bord de la ville bas', 7:'bord de la ville droit',
            10:'coin de la ville',
            11:'bord interne horizontal', 12:'bord de la ville vertical'}
    for i in dico.keys():
        print(i, '<=>', dico[i])
        
    tcv.affiche_ville(tcv.test(demi_longueur_cote))

#----------------------------------------
## Fonction pour l'affichage

        
def copie_ville(ville):
    '''Cette fonction copie la ville'''
    
    copie = []

    for quartier in ville:
        q_tmp = []
        
        for ligne in quartier:
            q_tmp.append(ligne[:])

        copie.append(q_tmp)

    return copie


def affichage(ville, afficher_prochain_tick, calculer_prochain_tick, keep_running, temps_min_entre_affichage):
    '''Cette fonction gere l'affichage'''

    demi_long = len(ville[0])
    longueur = 2 * demi_long
    generation = -1

    while keep_running.value:

        generation += 1

        #Recuperation des informations
        for _ in range(4): afficher_prochain_tick.acquire()
        
        ville_a_afficher = copie_ville(ville)
        
        for _ in range(4): calculer_prochain_tick.release()

        #affichage
        
        for ligne in range(longueur):
            
            move_to(ligne + 1, longueur)         # pour effacer toute ma ligne
            erase_line_from_beg_to_curs()
            move_to(ligne + 1, 1)

            q = 2 * (ligne // demi_long)
            l = ligne % demi_long

            for colonne in range(longueur):

                if colonne == demi_long:
                    q += 1
                
                if ville_a_afficher[q][l][colonne % demi_long]:
                    print("X", end = '')
                else:
                    print(end = ' ')

        move_to(longueur + 2, 10 + math.log2(generation + 1))
        erase_line_from_beg_to_curs()
        move_to(longueur + 2, 1)
        print('Generation %d'%(generation))
        
        sleep(temps_min_entre_affichage)

    


# ---------------------------------------------------

def detourner_signal(signum, stack_frame) :
    keep_running.Value = False
    os._exit(0)

# ---------------------------------------------------

#Programme principal

if __name__ == "__main__":

    import platform
    if platform.system() == "Darwin" :
        mp.set_start_method('fork') # Nécessaire sous macos, OK pour Linux (voir le fichier des sujets)

    Nbr_quartier = 4 #Pas modifiable. Si modification le code ne le supportera pas.
    demi_longueur_cote = 30 #Longueur de la moitie d'un cote. Modifiable !
                            #Attention au limite du terminal.
    keep_running = mp.Value(ctypes.c_bool, True)
    temps_min_entre_affichage = 0.1 #en secondes

    #Cree une matrice carree de taille 2 * demi_longueur_quartier. Une case vaut True => cellule vivante
    ville = [[ mp.Array('i',[randint(0,8)//7 for _ in range(demi_longueur_cote)])
               for l in range(demi_longueur_cote)] for q in range(Nbr_quartier)]

    #Ville test avec glider a decommenter pour tester
    '''
    ville = [[ mp.Array('i',[0 for _ in range(demi_longueur_cote)])
               for l in range(demi_longueur_cote)] for q in range(Nbr_quartier)]

    #Glider 1
    ville[0][4][5] = True
    ville[0][5][5] = True
    ville[0][5][3] = True
    ville[0][6][5] = True
    ville[0][6][4] = True

    #Glider 2
    ville[0][-2][5] = True
    ville[0][-1][5] = True
    ville[0][-1][3] = True
    ville[2][0][5] = True
    ville[2][0][4] = True

    #Glider 3
    ville[1][4][0] = True
    ville[1][5][0] = True
    ville[0][5][-2] = True
    ville[1][6][0] = True
    ville[0][6][-1] = True

    #Forme
    ville[3][4][5] = True
    ville[3][5][5] = True
    ville[3][5][4] = True
    ville[3][6][5] = True
    ville[3][6][6] = True

    #Centre ville
    ville[0][-1][-1] = True
    ville[1][-1][0] = True
    ville[2][0][-1] = True
    ville[3][0][0] = True
    '''
    

    afficher_prochain_tick = mp.Semaphore(4) # Ces semaphores servent a sync l'affichage sur chaque tick
    calculer_prochain_tick = mp.Semaphore(0)  # pour ne pas rendre les quartiers async. On veut commencer
                                             # par afficher la seed d'ou 4 pour l'affichage.
    push_ville_evo = [mp.Semaphore(0) for _ in range(4)] #Pour synchroniser l'actualisation de la ville
                                                         #ie tous les quatiers en meme temps.
    
    effacer_ecran()
    curseur_invisible()
    
    # Détournement d'interruption
    signal.signal(signal.SIGINT, detourner_signal)

    mes_process = []
    
    for i in range(Nbr_quartier):  # Lancer   Nb_process  processus
        mes_process.append(mp.Process(target=quartier_evolution, args= (ville, i, afficher_prochain_tick, calculer_prochain_tick, push_ville_evo, keep_running)))
        mes_process[i].start()

    mes_process.append(mp.Process(target = affichage, args= (ville, afficher_prochain_tick, calculer_prochain_tick, keep_running, temps_min_entre_affichage)))
    mes_process[-1].start()
    
    move_to(2 * demi_longueur_cote + 4, 1)
    print("Le jeu de la vie est lance, CTRL-C arrêtera le jeu...")

    for i in range(len(mes_process)): mes_process[i].join()

    #Le jeu s'arrete avec le detournement de signal !
