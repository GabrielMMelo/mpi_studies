from mpi4py import MPI

def f(x):
     return x*x + 2*x


a = 2
b = 22
n = 5

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

chunk = n // size
_chunk = n % size  # remaining


# to flow control
last_position = rank * chunk
first_position = last_position - chunk

extra_position = 0  # extra position if the chunk result isn't an integer

# the first _chunk process will receive the extra position
if _chunk >= rank + 1:
    extra_position = 1

h = int((b-a)/n)

subtotal = (f(a) + f(b))/2.0

print(a, h, first_position)
for i in range(a + h*first_position, last_position + extra_position, h):
    subtotal = subtotal + f(i)

subtotal = comm.gather(subtotal, root=0)

if rank == 0:
    total = sum(subtotal);


    print("With n =", n, "trapezoids, our estimate \n");
    print("of the integral from", a, "to", b, "=", total);
