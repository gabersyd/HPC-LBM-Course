from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

sendbuf = None
if rank == 0:
    data = np.arange(100, dtype='i')
    sendbuf = data.reshape((size,100//size))
    #np.empty([size, 10], dtype='i')
    print('I am core',rank,' and I created data ',sendbuf)
recvbuf = np.empty(100//size, dtype='i')
comm.Scatter(sendbuf, recvbuf, root=0)
print('I am core',rank,' and received data is',recvbuf)