# Auteur : Remi De Pretto
# Date : 06/06/24
# Implementation d'un service de calcul (calculettes) et de clients

import multiprocessing as mp    
import time,random,os,signal,sys
 
def calculette(op_to_do_queue, results_queues, stdout_lock):
    '''Cette fonction realise les calcules venant de op_to_do_queue et envoye le resultat dans results_queue'''
    
    pid = os.getpid()
    stdout_lock.acquire()
    print('Bonjour de la calculette', pid)
    stdout_lock.release()
      
    while True:
        cmd = op_to_do_queue.get()
        client, cmd = cmd.split(';'.encode())
        
        try:
            res = eval(cmd)
            results_queues[int(client)].put(str(res).encode())
            stdout_lock.acquire()
            print("La calculatrice", pid, "a recu ", cmd.decode(), "du client", client.decode(), "et a envoyé", res)
            print('-'* 60)
            stdout_lock.release()
            time.sleep(1)
            
        except:
            print("L'operation demadee est syntaxiquement incorrect !")


        
def client(c_id, op_to_do_queue, results_queue, stdout_lock):
    '''Cette fonction simule les demandes d'un client. Les demandes de calculs sont envoyees dans op_to_do et recoie les resultats dans results_queue.'''
    pid = os.getpid()
    stdout_lock.acquire()
    print('Bonjour du client', c_id, "dont le pid est", pid)
    stdout_lock.release()
    
    while True :
        # Le client envoie aux calculettes un calcul à faire et récupère le résultat
        opd1 = random.randint(1,10)
        opd2 = random.randint(1,10)
        operateur=random.choice(['+', '-', '*', '/'])
        str_commande = str(opd1) + operateur + str(opd2)
        
        op_to_do_queue.put((str(i) + ';' + str_commande).encode()) #l'ajout str(i) de permet aux calculettes de savoir a qui renvoyer le resultat.
        res = results_queue.get() #Mise en attente d'un resultat et recuperation de ce dernier.

        #affichage
        stdout_lock.acquire()
        print("Le client", c_id, "a demande à faire : ", str_commande)
        print("Le client", c_id, "a recu ", res.decode())
        print('-'* 60)
        stdout_lock.release()
        time.sleep(1)
            
## Catch sigint

def derouter_signal(signum, stack_frame) :
    global sigint
    print("Les clients et calculettes sont interrompus ...", os.getpid())
    os._exit(0)

##

if __name__ == "__main__" :
    import platform
    if platform.system() == "Darwin" :
        mp.set_start_method('fork') # Nécessaire sous macos, OK pour Linux (voir le fichier des sujets)
    # Détournement d'interruption
    signal.signal(signal.SIGINT, derouter_signal)
        
    Nbr_calculette = 5
    Nbr_client = 5

    #Initialisation des queues
    stdout_lock = mp.Lock()
    op_to_do_queue = mp.Queue()
    results_queues = [mp.Queue() for _ in range(Nbr_client)]

    #Initialisation des process
    calculettes = [mp.Process(target= calculette, args= (op_to_do_queue, results_queues, stdout_lock)) for _ in range(Nbr_calculette)]
    clients = [mp.Process(target= client, args= (i, op_to_do_queue, results_queues[i], stdout_lock)) for i in range(Nbr_client)]

    for i in range(Nbr_calculette):calculettes[i].start()
    for i in range(Nbr_client): clients[i].start()

    for i in range(Nbr_calculette): calculettes[i].join()
    for i in range(Nbr_client): clients[i].join()

