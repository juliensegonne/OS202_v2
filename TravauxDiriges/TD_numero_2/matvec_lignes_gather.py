# Produit matrice-vecteur v = A.u
import numpy as np
from mpi4py import MPI


globCom = MPI.COMM_WORLD.Dup()
nbp     = globCom.size
rank    = globCom.rank
name    = MPI.Get_processor_name()

# Dimension du problème (peut-être changé)
dim = 120

Nloc=dim//nbp

# Initialisation de la matrice
A = np.array([[(i+j) % dim+1. for i in range(dim)] for j in range(dim)])
#print(f"A = {A}")

# Initialisation du vecteur u
u = np.array([i+1. for i in range(dim)])
#print(f"u = {u}")

v=np.zeros(Nloc)

for k in range(dim):    
    for j in range(Nloc) :
        v[j]+=A[j+rank*Nloc,k]*u[k]


res = np.zeros(dim)
globCom.Allgather(v,res)

print("A.u = ",res)



