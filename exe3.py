from mpi4py import MPI

def isprime(n):
    """ Returns True if n is prime """
    if n == 2:
        return True
    if n == 3:
        return True
    if n % 2 == 0:
        return False
    if n % 3 == 0:
        return False
    i = 5
    w = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += w
        w = 6 - w
    return True

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

N = 1000000
chunk = N // size
_chunk = N % size  # remaining

rank = rank + 1  # to make index easier

last_position = rank * chunk
first_position = last_position - chunk + 1

extra_position = 0

if _chunk >= rank:
    extra_position = 1

subtotal = 0
last_prime = False

for i in range(first_position, last_position + extra_position + 1, 2):
    if isprime(i):
        if last_prime:
            subtotal = subtotal + 1
        else:
            last_prime = True
    else:
        last_prime = False

subtotal = comm.gather(subtotal, root=0)

if rank-1  == 0:
    total = sum(subtotal)
    print(total)
