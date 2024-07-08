#Auteur : Remi De Pretto
#Date 13/06/24
#Implementation de la methode des k-means sequentielle et parrallele.

from random import random, randint
from numpy import sqrt
import multiprocessing as mp
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def init_Lst(N):
    Lst = []
    while len(Lst) < N:
        p = (random() * 100, random() * 100)
        if p not in Lst:
            Lst.append(p)
    return Lst


def dist_euclid(p,q):
    '''calcule la dist euclidienne au carre car la racine carre est inutile sauf pour perdre du temps de calcul'''
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def find_nearest(p,L):
    '''Cette fonction renvoie l'indice du point le plus proche de p dans L'''
    i_min = 0
    dist_min = dist_euclid(p, L[0])
                           
    for i in range(1, len(L)):
        dist = dist_euclid(p, L[i])
        if dist < dist_min:
            dist_min = dist
            i_min = i

    return i_min


def barycentre(L):
    '''renvoie le point le plus proche du barycentre d'une liste de points'''
    assert len(L) != 0, "pas de barycentre pour une liste vide !"
    #Calcule le barycentre sans qu'il soit dans la liste
    sx,sy = 0,0
    for x,y in L:
        sx += x
        sy += y
    bar = sx / len(L), sy / len(L)

    #Renvoie le point le plus proche du barycentre
    return L[find_nearest(bar,L)]


def centroid_init(Lst, k):
    index_m = [randint(0, len(Lst) - 1)]

    #On fait k fois :
    #pour chaque points qui n'est pas un barycentre, ie pas son index dans index_m, on calcule
    #la dist a tous les barycentres. On prend le point qui minimisant la variance
    #en maximisant la moyenne des distances.

    for _ in range(1, k):
        i_tmp = -1
        moy_max = 0
        var_min = float('Inf')

        for i in range(len(Lst)):
            #Calcule de la moy et de la var
            if i not in index_m:
                dist_to_bary = [sqrt(dist_euclid(Lst[i], Lst[j])) for j in index_m]
                dist_moy = sum(dist_to_bary) / len(index_m)
                dist_var = 0
                for d in dist_to_bary:
                    dist_var += (d - dist_moy) ** 2

                #On stocke uniquement le meilleur point selon les conditions mentionees plus haut.
                #if (moy_max < dist_moy) or (moy_max - dist_moy < .0001 and var_min > dist_var) :
                if (var_min > dist_var) or (var_min - dist_var < .0001 and moy_max < dist_moy) :
                    i_tmp = i
                    moy_max = dist_moy
                    var_min = dist_var
        
        index_m.append(i_tmp)

    return [Lst[i] for i in index_m]


def min_dist(m, n):
    '''Cette fonction renvoie la distance la plus petite entre les points de meme indice de m et n'''
    dist_min = dist_euclid(m[0], n[0])
                           
    for i in range(1, len(m)):
        dist = dist_euclid(m[i], n[i])
        if dist < dist_min:
            dist_min = dist

    return dist_min


def max_dist(m, n):
    '''Cette fonction renvoie la distance la plus grande entre les points de meme indice de m et n'''
    dist_max = dist_euclid(m[0], n[0])
                           
    for i in range(1, len(m)):
        dist = dist_euclid(m[i], n[i])
        if dist > dist_max:
            dist_max = dist

    return dist_max


def plot_clusters(L, m, fig):
    '''renvoie les donnees de maniere a ce que plt puisse plot et avec des couleurs'''
    
    colors = list(mcolors.TABLEAU_COLORS)
    #Decommenter pour plus de couleur (15) mais perte de contraste.
    #colors = ['grey', 'brown', 'red', 'orangered', 'saddlebrown', 'gold', 'olive', 'palegreen',
    #          'forestgreen', 'lightseagreen', 'cyan', 'royalblue', 'navy', 'indigo', 'magenta']

    plt.figure(fig)
    
    for i in range(len(L)):
        X,Y = [],[]
        for x,y in L[i]:
            if (x,y) not in m:
                X.append(x)
                Y.append(y)

        plt.plot(X, Y, '+', color = colors[i%len(colors)])

    for i in range(len(m)):
        plt.plot(m[i][0], m[i][1], 'o', color = colors[(i+5)%len(colors)])


##Version sequentielle
def K_means_seq(k, N, epsilon, Lst = []) :
    '''Cette fonciton realise la methode des k-means sequentiellement.
       N est le nbr de points, epsilon est la condition d'arret : les centres des clusters se 
       sont deplaces de moins de epsilon. Les couleurs pour les clusters sont cycliques de cycle
       10. Donc s'il y a plus que 10 clusters, au moins deux cluster seront de la meme couleurs.'''

    epsilon *= epsilon #car nous travaillons avec les normes au carre !
    if Lst == []: #Les points sont fournis ou pas
        Lst = init_Lst(N)
    m = centroid_init(Lst, k)
    nbr_iter = 0
    plot_clusters([Lst], m, nbr_iter)
    old_m = m[:]
    
    
    fini = False
    
    while not(fini):
        nbr_iter += 1
        L = [[] for _ in range(k)]
        
        for p in Lst:
            L[find_nearest(p,m)].append(p)
            
        m = list(map(barycentre, L))

        plot_clusters(L, m, nbr_iter)

        #J'ai mis un max et non un min, car trop souvent l'algo terminer trop vite avec des
        #barycentres proches de ceux avec un max. Cependant la partition L de Lst n'est souvent
        #pas assez bonnes. De plus, nous sommes exposes bien plus souvent que nous le pensons
        #au cas ou au moins un barycentre ne bouge pas entre initialisation et le 1er tour de
        #boucle, surtout avec k grand (ex : 10).
        #Csq : Attention plus couteux !
        #Si vous voulez tester, echanger la condition commentee avec celle non commentee.

        #if min_dist(m, old_m) < epsilon:
        if max_dist(m, old_m) < epsilon:
            fini = True
        old_m = m [:]

    plt.show()
    #return m, L



##Version en parallele

#definition de la fonction qui sera utilisee dans la pool
def assigner_points_aux_clusters(param):
    (slice_of_Lst, m) = param
    L = [[] for _ in range(len(m))]
    for p in slice_of_Lst:
        i_to_put_p = find_nearest(p,m)
        
        #lock.acquire()
        L[i_to_put_p].append(p)
        #lock.release()
    return L


def merge_result(r):
    '''Cette fonction fusionne les contributions de tous les process'''
    L = []
    for i in range(len(r[0])): #len(r[0]) = k = nbr de cluster
        cluster = []
        for l in r:
            cluster += l[i]
        L.append(cluster)
    return L
            

def K_means_para(k, N, epsilon, nbr_coeur, Lst = []) :
    '''Cette fonciton realise la methode des k-means en parallele.
       N est le nbr de points, epsilon est la condition d'arret : les centres des clusters se 
       sont deplaces de moins de epsilon. Les couleurs pour les clusters sont cycliques de cycle
       10. Donc s'il y a plus que 10 clusters, au moins deux cluster seront de la meme couleurs.'''

    epsilon *= epsilon #car nous travaillons avec les normes au carre !
    if Lst == []: #Les points sont fournis ou pas
        Lst = init_Lst(N)
    m = centroid_init(Lst, k)
    nbr_iter = 0
    plot_clusters([Lst], m, nbr_iter)
    old_m = m[:]
    trunc_length = N // nbr_coeur
    #lock = mp.Lock()
    
    fini = False
    
    while not(fini):
        nbr_iter += 1

        splitted_Lst = [(Lst[i * trunc_length : (i + 1) * trunc_length], m)
                        for i in range(nbr_coeur - 2)]
        splitted_Lst.append((Lst[(nbr_coeur - 1) * trunc_length :], m))
        
        pool = mp.Pool(nbr_coeur)
        result = pool.map(assigner_points_aux_clusters, splitted_Lst) 
        pool.close()

        pool.join()

        L = merge_result(result)

        m = list(map(barycentre, L))

        plot_clusters(L, m, nbr_iter)

        #meme discussion que pour la version seq
        if max_dist(m, old_m) < epsilon:
            fini = True
        old_m = m [:]

    plt.show()
    #return m, L

if __name__ == "__main__":
    k = 10 #Nombre de cluster.
    N = 500 #Nombre de points
    epsilon = .001 #Precision
    nbr_coeur = 4 #Nombre de travailleur de la pool.
    Lst = [] #Liste des points a fournir si l'on souhaite garder la meme liste.
    K_means_para(k, N, epsilon, nbr_coeur, Lst)
