# Auteur : Remi De Pretto (Auteur du quelette de base : un encadrant de CPE Lyon, a priori : Alexander Saidi )
# Date : 06/06/24
# Ce programme simule une course hippique


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
NORMAL = "\x1B[0m"                  #  Normal
BOLD = "\x1B[1m"                    #  Gras
UNDERLINE = "\x1B[4m"               #  Souligné


# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK="\033[22;30m"                  #  Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m"                    #  Rouge
CL_GREEN="\033[22;32m"                  #  Vert
CL_BROWN = "\033[22;33m"                #  Brun
CL_BLUE="\033[22;34m"                   #  Bleu
CL_MAGENTA="\033[22;35m"                #  Magenta
CL_CYAN="\033[22;36m"                   #  Cyan
CL_GRAY="\033[22;37m"                   #  Gris

# "01" pour quoi ? (bold ?)
CL_DARKGRAY="\033[01;30m"               #  Gris foncé
CL_LIGHTRED="\033[01;31m"               #  Rouge clair
CL_LIGHTGREEN="\033[01;32m"             #  Vert clair
CL_YELLOW="\033[01;33m"                 #  Jaune
CL_LIGHTBLU= "\033[01;34m"              #  Bleu clair
CL_LIGHTMAGENTA="\033[01;35m"           #  Magenta clair
CL_LIGHTCYAN="\033[01;36m"              #  Cyan clair
CL_WHITE="\033[01;37m"                  #  Blanc

#-------------------------------------------------------
import multiprocessing as mp
import os, time,math, random, sys, ctypes, signal

# Une liste de couleurs à affecter aléatoirement aux chevaux
lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY,
             CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN,  CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]

def effacer_ecran() : print(CLEARSCR,end='')
def erase_line_from_beg_to_curs() : print("\033[1K",end='')
def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')
def move_to(lig, col) : print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def en_couleur(Coul) : print(Coul,end='')
def en_rouge() : print(CL_RED,end='') # Un exemple !
def erase_line() : print(CLEARELN,end='')  

# La tache d'un cheval
def un_cheval(ma_ligne : int, keep_running, horse_pos, locki) : # ma_ligne commence à 0
    col=1

    while col < LONGEUR_COURSE and keep_running.value :
        
        move_to(ma_ligne+1,col)         # pour effacer toute ma ligne
        erase_line_from_beg_to_curs()
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        print('('+chr(ord('A')+ma_ligne)+'>')     #affiche le cheval a sa nouvelle position.

        col+=1
        locki.acquire()
        horse_pos[i] = col
        locki.release()
        
        time.sleep(0.1 * random.randint(1,5))
        
    # Le premier arrivée gèle la course !
    # J'ai fini, je me dis à tout le monde
    keep_running.value=False

def find_index_max(L):
    '''Cette fonction trouve le maximum d'une liste et renvoie son index'''
    
    i_max = 0

    for i in range(1, len(L)):
        if L[i] > L[i_max]:
            i_max = i

    return i_max

def find_indexes_max(L):
    '''Cette fonction trouve le ou les maximums d'une liste et renvoie leur index'''
    
    L_max = [0]

    for i in range(1, len(L)):
        if L[i] > L[L_max[0]]:
            L_max = [i]
        elif L[i] == L[L_max[0]]:
            L_max.append(i)

    return L_max

def find_index_min(L):
    '''Cette fonction trouve le minimum d'une liste et renvoie son index'''
    
    i_min = 0

    for i in range(1, len(L)):
        if L[i] < L[i_min]:
            i_min = i

    return i_min
    
def arbitre(keep_running, horse_pos, lock):
    '''Cette fonction arbitre la course en affichant le dernier, le premier et le resultat final (les vainqueurs).'''

    #Index du premier et du dernier
    ahead = 0
    last = 0

    while keep_running.value:

        #Copie de la position des chevaux
        for i in range(Nb_process): lock[i].acquire()
        horse_pos_tmp = horse_pos[:]
        for i in range(Nb_process): lock[i].release()

        #Determination de qui est premier et aui est dernier
        ahead = find_index_max(horse_pos_tmp)
        last = find_index_min(horse_pos_tmp)

        #Affichage du premier et du dernier
        move_to(Nb_process + 5, 80)         # pour effacer toute ma ligne
        erase_line_from_beg_to_curs()
        move_to(Nb_process + 5, 1)
        en_couleur(CL_RED)
        print('Best : (%s>    en ligne %d, position %d ; Worst : (%s>    en ligne %d, position %d'%(
            chr(ord('A')+ahead), ahead, horse_pos_tmp[ahead], chr(ord('A')+last), last, horse_pos_tmp[last]))

        time.sleep(.5) #Si temps inferieur impossible de lire car change trop vite

    
    #Resultat final
    #Copie de la position des chevaux
    for i in range(Nb_process): lock[i].acquire()
    horse_pos_tmp = horse_pos[:]
    for i in range(Nb_process): lock[i].release()
    winners = find_indexes_max(horse_pos_tmp)

    move_to(Nb_process + 5, 80)         # pour effacer toute ma ligne
    erase_line_from_beg_to_curs()
    move_to(Nb_process + 5, 1)
    en_couleur(CL_RED)
    print('Winners : ', end='')
    
    for i in winners:
        print('(%s>'%(chr(ord('A') + i)), end=' ')
        

#------------------------------------------------
def derouter_signal(signum, stack_frame) :
    '''Cette fonction deroute le ^C pour terminer la course prematurement'''

    #Affichage d'un message de fin
    move_to(Nb_process + 10, 1)
    erase_line()
    move_to(Nb_process + 10, 1)
    curseur_visible()
    print("La course est interrompu ...")

    #Arret du processus
    os._exit(0)

# ---------------------------------------------------
# La partie principale :
if __name__ == "__main__" :
         
    import platform
    if platform.system() == "Darwin" :
        mp.set_start_method('fork') # Nécessaire sous macos, OK pour Linux (voir le fichier des sujets)
        
    LONGEUR_COURSE = 50 # Tout le monde aura la même copie (donc no need to have a 'value')
    keep_running=mp.Value(ctypes.c_bool, True)
     
    Nb_process=20 #Nombre de chevaux car on ne compte ni le process qui cree (pere) ni l'arbitre.
    mes_process = [0 for i in range(Nb_process)]

    horse_pos = mp.Array('i', [0 for _ in range(Nb_process)], lock = False)
    # contient la liste des positions de chaque cheval

    lock = [mp.Lock() for _ in range(Nb_process)]
    
    effacer_ecran()
    curseur_invisible()
    
    # Détournement d'interruption
    signal.signal(signal.SIGINT, derouter_signal) # deroutement de CTRL_C

    for i in range(Nb_process):  # Lancer   Nb_process  processus
        mes_process[i] = mp.Process(target=un_cheval, args= (i, keep_running, horse_pos, lock[i]))
        mes_process[i].start()

    mes_process.append(mp.Process(target = arbitre, args= (keep_running, horse_pos, lock)))
    mes_process[-1].start()
    
    move_to(Nb_process + 10, 1)
    print("tous lancés, CTRL-C arrêtera la course ...")

    for i in range(Nb_process + 1): mes_process[i].join()


    move_to(Nb_process + 10, 50)
    erase_line()
    move_to(Nb_process + 10, 1)
    curseur_visible()
    print("Fini ... ", flush=True)
