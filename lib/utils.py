import sys
import math
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parents[1]))
from lib import config as cfg

def debug(msg):
    if cfg.DEBUG_MODE:
        frame_obj = sys._getframe(1)
        method_name =     frame_obj.f_code.co_name
        file_name   =     frame_obj.f_code.co_filename
        lineno      = str(frame_obj.f_lineno)
        sys.stderr.write(f"[DEBUG]:{file_name}:{lineno}:{method_name}: {msg}\n")

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
