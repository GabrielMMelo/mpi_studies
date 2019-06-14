from mpi4py import MPI

def is_prime(n):
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

# to check between the process ranges
last_prime = 0
first_prime = False

# to flow control
last_position = rank * chunk
first_position = last_position - chunk + 1

extra_position = 0  # extra position if the chunk result isn't an integer

# the first _chunk process will receive the extra position
if _chunk >= rank:
    extra_position = 1

previous_prime = False
biggest_interval = 0

# each process look for the biggest interval inside their range (chunk)
for i in range(first_position, last_position + extra_position + 1):
    if is_prime(i):
        last_prime = i
        if not first_prime:  # check if it isn't set
            first_prime = i
        if not previous_prime:  # check if it isn't set
            previous_prime = first_prime
        actual_interval = i - previous_prime
        if actual_interval > biggest_interval:
            biggest_interval = actual_interval
        previous_prime = i

# gathers
biggest_interval = comm.gather(biggest_interval, root=0)
first_prime = comm.gather(first_prime, root=0)
last_prime = comm.gather(last_prime, root=0)

if rank-1 == 0:
    total = max(biggest_interval)

    # look for bigger intervals between the processes' range
    for i in range(1, size):
        between_interval = first_prime[i] - last_prime[i-1]
        if  between_interval > total:
            total = between_interval
    print("Maximum interval:", total)
