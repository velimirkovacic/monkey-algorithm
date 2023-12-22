import ma
import numpy as np
import matplotlib.pyplot as plt

f = lambda x : -np.dot(x, x)
cond=lambda x : np.max(x) < 100 and np.min(x) > -100

ma = ma.MA(M=5, N=60, Nc=50, a=0.0001, b=10, c=-1, d=1)
x, fs = ma.optimize(f=f, cond=cond, n=10, l=-100, r=100)

print("x* =", x)
print("f(x*) =", f(x))

plt.plot(range(1, len(fs)), fs[1:])
plt.title("Monkey algorithm")
plt.xlabel("iterations")
plt.ylabel("f(x*)")
plt.show()