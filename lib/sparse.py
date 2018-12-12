import math
import itertools

class SparseTable():
    """
        self.array: inputu array (size N)
        self.st   : sparse table (size N x log_N + 1)
    """
    def __init__(self, array):
        """
            create sparse table
        """
        self.array = array
        N     = len(self.array)
        log_N = math.floor(math.log2(N))

        self.st = [[0 for j in range(log_N+1)] for i in range(N)]
        for p, i in itertools.product(range(log_N+1), range(N)):
            if p == 0:
                self.st[i][p] = i
            elif self.array[self.st[i][p-1]] < self.array[self.st[min(i+2**(p-1),N-1)][p-1]]:
                self.st[i][p] = self.st[i][p-1]
            else:
                self.st[i][p] = self.st[min(i+2**(p-1),N-1)][p-1]

    def RmQ(self, i, j):
        """
            return RmQ(i, j)
            if j < i, swap i, j
        """
        if i == j:
            return i
        if j < i:
            i, j = j, i 

        k = math.floor(math.log2(j-i))
        if self.array[self.st[i][k]] < self.array[self.st[j-2**k+1][k]]:
            return self.st[i][k]
        else:
            return self.st[j-2**k+1][k]
