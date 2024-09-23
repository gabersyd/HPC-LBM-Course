from mpi4py import MPI
import numpy as np 

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

#print('rank=',rank,'size=',size)


# automatic MPI datatype discovery
if rank == 0:
    data = np.arange(100, dtype=np.float64)
    chunks=data.shape[0]//(size-1)
    for core in np.arange(1,size):
        dataToSend=data[chunks*(core-1):chunks*core]
        comm.Send(dataToSend, dest=core)
        print('I am core',rank,' and I have sent',dataToSend,'to destination',core)
else:
    data = np.empty(100//(size-1), dtype=np.float64)
    #print('I am core',rank,'I have an empty array',data,'to received data from source',0)
    comm.Recv(data, source=0)
    print('I am core',rank,'I have received',data,'from source',0)
