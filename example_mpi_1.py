from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print('rank=',rank,'size=',size)

if rank == 0:
    data = {'a': 7, 'b': 3.14}
    comm.send(data, dest=1, tag=11)
    print('rank=',rank,'I have sent',data)
    data2 = comm.recv(source=1, tag=21)
    print('rank=',rank,'I have received',data2)


elif rank == 1:
    data2 = 'this is a test string'
    comm.send(data2, dest=0, tag=21)    
    data = comm.recv(source=0, tag=11)
    print('rank=',rank,'I have received',data)
