
# TD1

`pandoc -s --toc README.md --css=./github-pandoc.css -o README.html`





## lscpu

```
CPU family:          23
    Model:               24
    Thread(s) per core:  2
    Core(s) per socket:  4
    Socket(s):           1
    Stepping:            1
    BogoMIPS:            4192.00
```
Caches (sum of all):     
  L1d:                   128 KiB (4 instances)
  L1i:                   256 KiB (4 instances)
  L2:                    2 MiB (4 instances)
  L3:                    4 MiB (1 instance)

*Des infos utiles s'y trouvent : nb core, taille de cache*



## Produit matrice-matrice



### Permutation des boucles

*Expliquer comment est compilé le code (ligne de make ou de gcc) : on aura besoin de savoir l'optim, les paramètres, etc. Par exemple :*

`make TestProduct.exe && ./TestProduct.exe 1024`


  ordre           | time    | MFlops  | MFlops(n=2048) 
------------------|---------|---------|----------------
i,j,k (origine)   | 24.4173 | 87.9494 |                
j,i,k             | 24.1074 | 89.08   |    
i,k,j             | 31.6681 | 67.8122 |    
k,i,j             | 33.5638 | 63.9821 |    
j,k,i             | 1.32807 | 1616.99 |    
k,j,i             | 2.03138 | 1057.15 |    


*Discussion des résultats*

Nous savons que les matrices sont stockées colonne par colonne. Or si la première variable à varier
(la boucle la plus profonde) correspond aux colonnes d'une matrice, il y aura une redondance de chargement,
à chaque itération une colonne sera rechargée (alors que pour aller de ligne en ligne on ne charge qu'une seule colonne). Ainsi, les coeurs sont surchargés.


### OMP sur la meilleure boucle 

`make TestProduct.exe && OMP_NUM_THREADS=8 ./TestProduct.exe 1024`

  OMP_NUM         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
1                 | 2097.46 |
2                 | 3735.89 |
3                 | 5303.45 |
4                 | 5741.66 |
5                 | 5678.63 |
6                 | 5938.99 |
7                 | 6552.21 |
8                 | 6703.14 |

On cherche à avoir un nombre de threads qui maximise l'accélération.

### Produit par blocs

`make TestProduct.exe && ./TestProduct.exe 1024`

  szBlock         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
origine (=max)    |  |
32                | 2442.15 |
64                | 3361.72 |
128               | 2841.04 |
256               | 5607.6 |
512               | 3719.04 | 
1024              | 5124.47 |




### Bloc + OMP



  szBlock      | OMP_NUM | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)|
---------------|---------|---------|-------------------------------------------------|
A.nbCols       |  1      | 1976.1  |                |                |               |
512            |  8      | 3947.09 |                |                |               |
---------------|---------|---------|-------------------------------------------------|
Speed-up       |         |         |                |                |               |
---------------|---------|---------|-------------------------------------------------|



### Comparaison with BLAS


# Tips 

```
	env 
	OMP_NUM_THREADS=4 ./produitMatriceMatrice.exe
```

```
    $ for i in $(seq 1 4); do elap=$(OMP_NUM_THREADS=$i ./TestProductOmp.exe|grep "Temps CPU"|cut -d " " -f 7); echo -e "$i\t$elap"; done > timers.out
```
