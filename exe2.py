from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

subtotal = rank + 1
subtotal = comm.gather(subtotal, root=0)

if rank == 0:
    p = 0
    for i in range(size):
        p = subtotal[i] + p
    print("p:", p)
    result = p*(p+1)/2
    print("Result:", result)
