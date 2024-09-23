from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
    data = [[i+1,i+2,i+3] for i in range(size)]
    print('I am core',rank,' and I created data ',data)
else:
    data = None
data = comm.scatter(data, root=0)
print('I am core',rank,' and data is',data,'and should be', (rank+1)**2)