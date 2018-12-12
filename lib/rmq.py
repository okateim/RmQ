from  pathlib import Path
import sys
import math
from copy import copy

sys.path.append(str(Path(__file__).absolute().parents[1]))
from lib import config as cfg
from lib.sparse import SparseTable as ST
from lib.inblock import InBlock as IB

class RmQDataStructure():
    def __init__(self, A):
        self.A = copy(A)
        self.N = len(A)
        self.block_size = math.floor(math.log2(self.N)/2.0)
        self.block_num  = math.ceil(self.N / self.block_size)
        
        self.InblockMin = list()
        m, argm = cfg.INF, -1
        for i in range(self.N):
            if A[i] < m:
                m, argm = A[i], i
            if (i+1) % self.block_size == 0 or i == self.N-1:
                self.InblockMin.append((m, argm))
                m, argm = cfg.INF, -1
        self.st = ST(self.InblockMin)
        
        self.blocks = list()
        for i in range(self.block_num):
            s = i * self.block_size
            t = s + self.block_size
            inblock_DS = IB(A[s:t])
            self.blocks.append(inblock_DS) 

    def RmQ(self, i, j):
        if not (0 <= i <= self.N-1 and 0 <= j <= self.N-1 and i <= j):
            print("invalid value")
            sys.exit(1)
        if i == j:
            return i
        if i > j:
            i, j = j, i
        
        block_num_of_i     = i // self.block_size
        block_num_of_j     = j // self.block_size
        inblock_index_of_i = i % self.block_size
        inblock_index_of_j = j % self.block_size

        # when i, j belong same block, just check inblock RmQ
        if block_num_of_i == block_num_of_j:
            inblock_argmin = self.blocks[block_num_of_i].RmQ(inblock_index_of_i, inblock_index_of_j)
            return self.block_size * block_num_of_i + inblock_argmin
        
        # RmQ in left block
        left_inblock_argmin  = self.blocks[block_num_of_i].RmQ(inblock_index_of_i, self.block_size-1)
        left_argmin          = self.block_size * block_num_of_i + left_inblock_argmin
        left_min             = self.A[left_argmin]
        # RmQ in right block
        right_inblock_argmin = self.blocks[block_num_of_j].RmQ(0, inblock_index_of_j)
        right_argmin         = self.block_size * block_num_of_j + right_inblock_argmin
        right_min            = self.A[right_argmin]

        center_min = cfg.INF
        if block_num_of_i + 1 <= block_num_of_j - 1:
            # RmQ between blocks
            center_argmin = self.InblockMin[self.st.RmQ(block_num_of_i + 1, block_num_of_j - 1)][1]
            center_min = self.A[center_argmin]
    
        minval = min(left_min, center_min, right_min)

        if minval == left_min:
            ret = left_argmin
        elif minval == center_min:
            ret = center_argmin
        else:  # minval == right_min
            ret = right_argmin
        return ret
