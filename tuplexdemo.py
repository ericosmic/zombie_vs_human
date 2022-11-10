from tuplex import *
import time
import random

def cl(k):
    if random.randint(0,10)>3:
        n = k[0] + k[1]
        m = k[0] + 1
    else:
        n = k[0]
        m = k[1]
    return n, m

st = time.time()
c = Context()
a = [12, 3, 4, 5, 5]
b = [1, 2, 3, 4, 5, 5, 6]

k = list(zip(a, b))
res = c.parallelize(k).map(cl).collect()

print(res)

sp = time.time()-st
print(f'sp time: {sp}')