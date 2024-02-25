import math
import numpy as np
from mpi4py import MPI

globCom = MPI.COMM_WORLD.Dup()
nbp     = globCom.size
rank    = globCom.rank
name    = MPI.Get_processor_name()

taille = 100

if rank==0 :
    T = np.random.random(taille)
    local_buckets=[[]]*nbp
    for nombre in T :
        i = math.floor(nombre*nbp)        #répartition locale
        local_buckets[i].append(nombre)
        
    for r in range(1,nbp) :
        globCom.send(local_buckets[r],r)
        
    bucket=local_buckets[0]
    bucket.sort()
    
else :
    bucket = globCom.recv(source=0)
    bucket.sort()

res = globCom.gather(bucket, root=0)[0]

if rank==0 :
    print(res)
    
    
    
    
    
    
    
    
    
    

