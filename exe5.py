from mpi4py import MPI

def get_number(number, position):
    return number // 10**position % 10

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

N = 900000  # 9*10*10*10*10*10
chunk = N // size
_chunk = N % size  # remaining

rank = rank + 1  # to make index easier

# to flow control
last_position = rank * chunk
first_position = last_position - chunk + 1

print(rank, first_position, last_position)

extra_position = 0  # extra position if the chunk result isn't an integer

# the first _chunk process will receive the extra position
if _chunk >= rank:
    extra_position = 1

subtotal = 0
previous_number = None

for i in range(first_position, last_position + extra_position + 1):
    sum_digits = 0
    for j in range(0, 6):
        current_number = get_number(i, j)
        sum_digits = sum_digits + current_number
        if previous_number == current_number:
            subtotal = subtotal + 1
        previous_number = current_number
    if sum_digits in [7, 11, 13]:
        subtotal = subtotal + 1

# gathers
subtotal = comm.gather(subtotal, root=0)

if rank-1 == 0:
    total = N - sum(subtotal)
    print(total)

