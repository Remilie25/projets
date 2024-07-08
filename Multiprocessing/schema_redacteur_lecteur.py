#Auteur : Remi De Pretto
#Date : 18/06/24
#Ceci est une implementation d'un gestionnaire de fichier donnant la priorite aux redacteurs.

import multiprocessing as mp
from time import sleep
from random import random, randint
import os, signal

##Fonctions

#Redacteur
def debut_redaction(mutex, nbr_redacteur, prio_redacteur, redacteur_lecteur_ex):
    '''Cette fonction gere l'acces au fichier partage pour les redacteurs'''
    
    mutex.acquire()
        
    nbr_redacteur.value += 1
    
    if nbr_redacteur.value == 1:
        prio_redacteur.acquire()
        
    mutex.release()

    redacteur_lecteur_ex.acquire()


def fin_redaction(mutex, nbr_redacteur, prio_redacteur, redacteur_lecteur_ex):
    '''Cette fonction gere la fin de la redaction sur le fichier partage (pour les redacteurs)'''

    redacteur_lecteur_ex.release()
    mutex.acquire()
        
    nbr_redacteur.value -= 1

    if nbr_redacteur.value == 0:
        prio_redacteur.release()
        
    mutex.release()
    

def redacteur(nom_fichier, mutex, nbr_redacteur, prio_redacteur, redacteur_lecteur_ex, stdout_lock, tps_max_op, r_id):
    '''Cette fonction simule le comportement d'un redacteur'''

    #messages possibles d'ecrire
    messages = ["Bonjour", "Informatique", "Dijkstra", "Mathematiques", "Riemann", "Au revoir"]
    
    while True:

        #Pour gerer le fichier partage
        debut_redaction(mutex, nbr_redacteur, prio_redacteur, redacteur_lecteur_ex)
        
        #Ecriture dans un fichier commun
        fichier = open(nom_fichier, 'w') #Chaque redacteur ecrase le travail du precedent.
        
        index = randint(0, len(messages) - 1)
        fichier.write(" Le process %d a ecrit "%(os.getpid()) + messages[index] + '.')
        sleep(tps_max_op * random()) #pour simuler un temps de travail

        stdout_lock.acquire()
        print("Je suis le processus %d et j'ai ecrit"%(os.getpid()), messages[index])
        stdout_lock.release()

        fichier.close()

        #Pour gerer le fichier partage
        fin_redaction(mutex, nbr_redacteur, prio_redacteur, redacteur_lecteur_ex)
        
        sleep(tps_max_op * r_id * random()) #pour simuler un temps de pause


#Lecteur
def debut_lecture(mutex, nbr_lecteur, prio_redacteur, redacteur_lecteur_ex):
    '''Cette fonction gere l'acces au fichier partage pour les lecteurs'''

    prio_redacteur.acquire()
    mutex.acquire()
        
    nbr_lecteur.value += 1
    
    if nbr_lecteur.value == 1:
        redacteur_lecteur_ex.acquire()

    mutex.release()
    prio_redacteur.release()


def fin_lecture(mutex, nbr_lecteur, prio_redacteur, redacteur_lecteur_ex):
    '''Cette fonction gere la fin de la lecture sur le fichier partage (pour les lecteurs)'''
    
    mutex.acquire()
        
    nbr_lecteur.value -= 1

    if nbr_lecteur.value == 0:
        redacteur_lecteur_ex.release()
        
    mutex.release()
    

def lecteur(nom_fichier, mutex, nbr_lecteur, prio_redacteur, redacteur_lecteur_ex, stdout_lock, tps_max_op, l_id):
    '''Cette fonction simule le comportement d'un redacteur'''
    
    while True:

        #Pour gerer le fichier partage
        debut_lecture(mutex, nbr_lecteur, prio_redacteur, redacteur_lecteur_ex)

        #lecture d'un message
        fichier = open(nom_fichier, 'r')
        message = fichier.readline()
        
        sleep(tps_max_op * random()) #pour simuler un temps de travail
        stdout_lock.acquire()
        print("Je suis le process %d et j'ai lu le message suivant :"%(os.getpid()), message)
        stdout_lock.release()

        #Pour gerer le fichier partage
        fin_lecture(mutex, nbr_lecteur, prio_redacteur, redacteur_lecteur_ex)

        sleep(tps_max_op * l_id * random()) #pour simuler un temps de pause

##Deroutement de signal
def derouter_signal(signum, stack_frame) :
    '''Cette fonction arrete tous les process.'''
    if __name__ == "__main__":
        for i in range(len(process)):
            process[i].terminate()

def close_properly():
    '''Cette fonction ferme le programme proprement : message de fin + supression du pipe'''
    print("\nFin de la simulation")
    os.unlink(nom_fichier)

##Programme principal
if __name__ == "__main__":

    #Deroutement d'interruption
    signal.signal(signal.SIGINT, derouter_signal)

    #Creation d'un fichier qui jouera le role de la ressource sur laquelle l'equipe de
    #redacteurs et lecteurs travailleront.
    nom_fichier = "fichier_sur_lequel_on_travail.txt"
    
    if os.path.exists(nom_fichier):
        os.unlink(nom_fichier)
        
    fichier = open(nom_fichier, 'w')
    fichier.close()

    #temps max, en seconde, d'attente pour simuler les temps de travail et de pause
    temps_max_entre_operation =  3
    nbr_redacteur = mp.Value('i', 0, lock = False)
    nbr_lecteur = mp.Value('i', 0, lock = False)


    #mutex sert a ce que chaque processus de debut ou de fin de lecture ou d'ecriture soit
    #traite d'un coup.
    mutex = mp.Lock()
    
    #redacteur_lecteur_ex sert a ce qu'il y ait que des redacteurs ou des lecteurs.
    redacteur_lecteur_ex = mp.Lock()
    
    #prio_redacteur donne la priorite au redacteur, coupant l'arrivee de nouveau lecteur.
    prio_redacteur = mp.Lock()
    
    #sdtout_lock sert a proteger la ressource sdtout.
    stdout_lock = mp.Lock()
    
    #Indiquent le nombre de process redacteurs et lecteurs. 
    nbr_process_redacteur = 2
    nbr_process_lecteur = 4
    
    process = []

    print("Pour arreter la simulation : ^C")
    
    #Creation des process
    for i in range(nbr_process_redacteur):
        process.append(mp.Process(target = redacteur, args = (nom_fichier, mutex, nbr_redacteur,
                                                              prio_redacteur, redacteur_lecteur_ex,
                                                              stdout_lock, temps_max_entre_operation,
                                                              i + 1)))
    
    for i in range(nbr_process_lecteur):
        process.append(mp.Process(target = lecteur, args = (nom_fichier, mutex, nbr_lecteur,
                                                            prio_redacteur, redacteur_lecteur_ex,
                                                            stdout_lock, temps_max_entre_operation,
                                                            i + 1)))
        
    #Lancement des process
    for i in range(len(process)):
        process[i].start()
        
    #Attente de la fin des process
    for i in range(len(process)):
        process[i].join()

    close_properly()
