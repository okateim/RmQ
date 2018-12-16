from pathlib import Path
from copy import copy
import sys
import math
import itertools

sys.path.append(str(Path(__file__).absolute().parents[1]))
from lib.utils import mask,lsb
from lib.utils import MyStack
from lib import config as cfg

class RmQDataStructure():
    """
        A         : array of integer    (copy of input array)
        ST        : 2d-array of integer (sparse table)
        BA        : array of integer    (each element represents bit array)
        InblockMin: array of integer    (minimum values of blocks)
    """
    __slots__ = ['A', 'ST', 'BA', 'InblockMin', ]

    def __init__(self, A):
        self.A = copy(A)
        N          = len(self.A)
        block_size = math.floor(math.log2(N)/2.0)
        block_num  = math.ceil(N / block_size)

        # create array of min value of blocks InblockMin
        self.InblockMin = list()
        m, argm = cfg.INF, -1
        for i in range(N):
            if A[i] < m:
                m, argm = A[i], i
            if (i+1) % block_size == 0 or i == N-1:
                self.InblockMin.append((m, argm))
                m, argm = cfg.INF, -1

        # create sparse table ST for RmQ between blocks
        M     = len(self.InblockMin)
        log_M = math.floor(math.log2(M))
        self.ST = [[0 for j in range(log_M+1)] for i in range(M)]
        for p, i in itertools.product(range(log_M+1), range(M)):
            if p == 0:
                self.ST[i][p] = i
            elif self.InblockMin[self.ST[i][p-1]] < self.InblockMin[self.ST[min(i+2**(p-1),M-1)][p-1]]:
                self.ST[i][p] = self.ST[i][p-1]
            else:
                self.ST[i][p] = self.ST[min(i+2**(p-1),M-1)][p-1]
                
        # create bit arrays for RmQ in block
        self.BA = list()             # array of integer (bit array).
        for i in range(block_num):
            s = i * block_size
            t = s + block_size
            subarray = A[s:t]
            M = len(subarray)
            l = [1 for i in range(M)]
            stack = MyStack()
            stack.push((-1, -1))  # sentinel 
            for j in range(M):
                if j != 0:
                    l[j] = l[j-1] 
                while subarray[j] < stack.top()[0]:
                    pop = stack.pop()
                    l[j] = l[j] ^ (1 << pop[1])
                stack.push((subarray[j], j))
                l[j] = l[j] | 1 << j
            del stack
            self.BA.append(l) 

    def RmQ(self, i, j):
        N = len(self.A)
        block_size = math.floor(math.log2(N)/2.0)
        block_num  = math.ceil(N / block_size)
        if not (0 <= i <= N-1 and 0 <= j <= N-1 and i <= j):
            sys.exit(1)
        if i == j:
            return i
        if i > j:
            i, j = j, i
        block_num_of_i     = i // block_size
        block_num_of_j     = j // block_size
        inblock_index_of_i = i %  block_size
        inblock_index_of_j = j %  block_size

        # when i, j belong same block, just check inblock RmQ
        if block_num_of_i == block_num_of_j:
            l = self.BA[block_num_of_i]
            inblock_argmin = self._RmQ_l(l, inblock_index_of_i, inblock_index_of_j)
            return block_size * block_num_of_i + inblock_argmin
        
        # RmQ in left block
        l = self.BA[block_num_of_i]
        left_inblock_argmin  = self._RmQ_l(l, inblock_index_of_i, block_size-1)
        left_argmin          = block_size * block_num_of_i + left_inblock_argmin
        left_min             = self.A[left_argmin]

        # RmQ in right block
        l = self.BA[block_num_of_j]
        right_inblock_argmin = self._RmQ_l(l, 0, inblock_index_of_j)
        right_argmin         = block_size * block_num_of_j + right_inblock_argmin
        right_min            = self.A[right_argmin]
        
        # RmQ between blocks
        center_min = cfg.INF
        if block_num_of_i + 1 <= block_num_of_j - 1:
            block_index   = self._RmQ_ST(block_num_of_i+1, block_num_of_j-1)
            center_argmin = self.InblockMin[block_index][1]
            center_min    = self.A[center_argmin]
    
        minval = min(left_min, center_min, right_min)
        if minval == left_min:
            ret = left_argmin
        elif minval == center_min:
            ret = center_argmin
        else:  # minval == right_min
            ret = right_argmin
        return ret

    def _RmQ_ST(self, i, j):
        if i == j:
            return i
        if j < i:
            i, j = j, i 
        k = math.floor(math.log2(j-i))
        if self.A[self.ST[i][k]] < self.A[self.ST[j-2**k+1][k]]:
            return self.ST[i][k]
        else:
            return self.ST[j-2**k+1][k]
     
    def _RmQ_l(self, l, i, j):
        if i == j:
            return i
        if i > j:
            i, j = j, i
        
        w = mask(l[j], i)
        return 0 if w == 0 else lsb(w)

