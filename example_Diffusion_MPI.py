from mpi4py import MPI
import numpy as np 
import matplotlib.pyplot as plt

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print('rank=',rank,'size=',size)

nxp=1000; nxc=nxp-1; xTot=1.0; 
dx=xTot/nxc; xMin=-xTot/2.0; xMax=xTot/2.0
steps=30000; totalTime=1.e-1; plotEverySteps = 100; 
deltaTime=totalTime/steps
diffusivity=1e-1; r = deltaTime*diffusivity/(dx*dx)

nxp_core=nxp//size
xMin_core=xMin+rank*xTot/size

#if rank == 0:
#    X_all = np.arange(nxp)*dx+xMin
#    T_all = np.zeros(nxp,np.Float)

X = np.arange(nxp_core)*dx+xMin_core
T = np.sin(2*np.pi*X)
X_extended = np.arange(nxp_core+2)*dx+xMin_core-dx
T_extended = np.sin(2*np.pi*X_extended)

if rank==0: print('r=',r)

DT=np.zeros(nxp_core)
for time in np.arange(steps):

    #send data to the right:
    if rank==0:
        T_extended[0:1]=0
        comm.send(T[-1], dest=rank+1)
        T_extended[-1]=comm.recv(source=rank+1)
    elif rank==size-1:
        T_extended[-2:-1]=0
        comm.send(T[0], dest=rank-1)
        T_extended[0]=comm.recv(source=rank-1)
    else:
        comm.send(T[-1], dest=rank+1)
        T_extended[-1]=comm.recv(source=rank+1)
        comm.send(T[0], dest=rank-1)
        T_extended[0]=comm.recv(source=rank-1)

    #print('I am core',rank,'I have received and sent data at step',time)
    T_extended[1:nxp_core+1]=T[:]
    DT[0:nxp_core]=T_extended[0:nxp_core]-2*T_extended[1:nxp_core+1]+T_extended[2:nxp_core+2]
    T += r * DT

    print('rank=',rank,'time=',time,np.max(T));
    T_all = comm.gather(T, root=0)
    if rank==0 and time%1000==0:
        T_all = np.asarray(T_all)
        T_all = T_all.reshape(-1)
        print(T_all)
        plt.plot(T_all);plt.savefig('pardiff_'+str(time)+'.png')


