import math
import sys
from  pathlib import Path

sys.path.append(str(Path(__file__).absolute().parents[1]))

class MyStack():
    def __init__(self):
        self.stack = []

    def empty(self):
        return len(self.stack) == 0

    def push(self, x):
        self.stack.append(x)
        return 0

    def pop(self):
        if self.empty():
            return None
        return self.stack.pop()

    def top(self):
        if self.empty():
            return None
        return self.stack[-1]

class InBlock():
    """
        self.array: input array
        self.l    : integer (representation of bit arrays)
    """
    __slots__ = ['array', 'l']
    def __init__(self, array):
        self.array = array
        M = len(array)
        st = MyStack()
        st.push((-1, -1))  # sentinel 

        # create bit array l[0..M-1]
        self.l = [1 for i in range(M)]
        for j in range(M):
            if j != 0:
                self.l[j] = self.l[j-1] 
            while self.array[j] < st.top()[0]:
                pop = st.pop()
                self.l[j] = self.l[j] ^ (1 << pop[1])
            st.push((self.array[j], j))
            self.l[j] = self.l[j] | 1 << j
        del st
     
    def _mask(self, target, mask_num):
        """
            clear the lower 'mask_num' bits of the integer 'target'
        """
        w = (target >> mask_num) << mask_num
        return w

    def _lsb(self, w):
        """
            return LSB(w)
        """
        return int(math.log2(w & (~w+1)))

    def RmQ(self, i, j):
        """
            return RmQ(i, j)
            if j < i, swap i, j
        """
        if i == j:
            return i
        if i > j:
            i, j = j, i
        
        w = self._mask(self.l[j], i)
        return 0 if w == 0 else self._lsb(w)
