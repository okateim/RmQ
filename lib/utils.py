import sys
import math

def mask(target, mask_num):
    """
        clear the lower 'mask_num' bits of the integer 'target'
    """
    w = (target >> mask_num) << mask_num
    return w

def lsb(w):
    """
        return LSB(w)
    """
    return int(math.log2(w & (~w+1)))

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
