import math
import numpy as np
from mpi4py import MPI

globCom = MPI.COMM_WORLD.Dup()
nbp     = globCom.size
rank    = globCom.rank
name    = MPI.Get_processor_name()

taille = 100

if rank==0 :
    T = np.random.random(taille) * 100
    m,M=min(T),max(T)
    t=[[]]*nbp
    for k in range(taille) :
        j = math.floor((nbp-1)*(T[k]-m)/(M-m))
        t[j].append(T[k])
    for r in range(1,nbp) :
        globCom.send(t[r],r)
    
else :
    liste = globCom.recv(source=0)
    liste=liste.sort()
    globCom.send(liste,dest=0)

if rank==0 :
    T_final=[]
    for r in range(1,nbp) :
        T_final+=globCom.recv(source=0)
    T_final+=t[nbp]
    print(T_final)
    
    
    
    
    
    
    
    
    
    

