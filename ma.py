import numpy as np
import random

class MA:

    def __init__(self, M=5, N=60, Nc=2000, a=0.001, b=0.5, c=-1, d=1):
        """
        Parameters
        ----------
        M : int, optional
            Number of monkeys
        N : int, optional
            Number of algorithm iterations
        Nc : int, optional
            Number of monkey climb iterations
        a : float, optional
            Step length
        b : float, optional
            View distance
        c : float, optional
            Left bound of sumersault range [c, d]
        d : float, optional
            Right bound of sumersault range [c, d]
        """
        self.M = M
        self.Nc = Nc
        self.N = N
        self.a = a
        self.b = b
        self.c = c
        self.d = d



    def sampleHypercube(self, n, l, r):
        x = []
        for i in range(n):
            x += [random.uniform(l, r)]
        return np.array(x)

    def sampleWatch(self, n, x, b):
        y = []
        for i in range(n):
            y += [random.uniform(x[i] - b, x[i] + b)]
        return np.array(y)

    def sampleDx(self, n, a):
        dx = []
        for i in range(n):
            dx += [(a if random.uniform(0, 1) > 0.5 else -a)]
        return np.array(dx)
    

    def initialize(self, cond, iLeft, iRight, M, n):
        X = []

        for i in range(M):
            x = self.sampleHypercube(n, iLeft, iRight)
            while not cond(x):
                x = self.sampleHypercube(n, iLeft, iRight)
            
            X += [x]
        return X
    

    def optimize(self, f, cond, n, l, r):
        """
        Parameters
        ----------
        f : function
            Number of monkeys
        cond : function
            Number of monkeys
        n : int
            Problem dimension
        l : float
            Left bound of initial range [c, d]
        r : float
            Right bound of initial range [c, d]

        Returns
        -------
        list
            a list of strings used that are the header columns
        """
        self.f = f
        self.cond = cond
        X = self.initialize(cond, l, r, self.M, n)
        opts = []
        self.x_opt = X[0]
        self.f_opt = self.f(X[0])
        for iter in range(self.N):
            print(iter, "/", self.N )
            self.climb(self.M, self.Nc, n, X, self.a)
            self.watchJump(self.M, n, X, self.b)
            self.climb(self.M, self.Nc, n, X, self.a)
            self.sumersault(self.M, n, X, self.c, self.d)
            opts += [self.f_opt]
            print("f(x*) =", self.f_opt)
        return self.x_opt, opts
    

    def climb(self, M, Nc, n, X, a):
        print("climb")
        for i in range(M):
            history = []
            for iter in range(Nc):

                dx = self.sampleDx(n, a)

                f_ps = []
                for j in range(n):
                    f_ps += [(self.f(X[i] + dx) - self.f(X[i] - dx))/(2 * dx[j])]                

                y = X[i] + a * np.sign(np.array(f_ps))

                if self.cond(y):
                    X[i] = y

                f_tmp = self.f(X[i])

                if f_tmp > self.f_opt:
                    self.f_opt = f_tmp
                    self.x_opt = X[i]
                                
                #if iter > 10:
                    #print(history[iter],  history[iter - 10])
                 #   if np.abs(history[iter] - history[iter - 10]) < 0.05:
                  #      break

    def watchJump(self, M, n, X, b):
        print("wj")
        for i in range(M):
            y = self.sampleWatch(n, X[i], b)
            j = 0
            while not (self.cond(y) and self.f(y) >= self.f(X[i])):
                if not j < 10000:
                    break
                y = self.sampleWatch(n, X[i], b)
                j += 1

            if j < 100:
                X[i] = y
    
    def sumersault(self, M, n, X, c, d):
        print("sault")
        p = np.array([0.0]*n)
        for i in range(M):
            p += X[i]
        p /= M

        for i in range(M):
            y = X[i] + random.uniform(c, d) * (p - X[i])

            while not self.cond(y):
                y = X[i] + random.uniform(c, d) * (p - X[i])
            X[i] = y
