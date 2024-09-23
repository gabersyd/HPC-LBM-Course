from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print('rank=',rank,'size=',size)

if rank == 0:
    data = {'a': 7, 'b': 3.14}

    req2 = comm.irecv(source=1,tag=21)
    req1 = comm.isend(data, dest=1, tag=11)

    req1.wait()
    data2=req2.wait()

    print('I have sent ',data,' from core',1)
    print('rank=',rank,'I have received',data2)

elif rank == 1:
    data2 = 'testString'

    req1 = comm.irecv(source=0, tag=11)
    req2 = comm.isend(data2,dest=0,tag=21)

    data = req1.wait()
    req2.wait()

    print('I have received ',data,' from core',0)
    print('I have sent',data2,'to core',0)

