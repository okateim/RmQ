#!/usr/bin/env python
# -*- coding: utf-8 -*-

from  pathlib import Path
import sys
sys.path.append(str(Path(__file__).absolute().parents[1]))
from lib import config as cfg
from lib.utils import debug
from lib.rmq import RmQDataStructure

DEFAULT_INPUT_FILE = Path(__file__).absolute().parents[0] / "test.csv"

def main():
    ############ Preprocess ###############
    print("Now preprocessing...")
    filename = "test.csv"
    with open(filename, 'r') as f:
        str_list = f.read().split(',')
    A = [int(val) for val in str_list]
    ds = RmQDataStructure(A)
    print("Complete!")
    #######################################

    N = len(A)
    for i in range(N):
        for j in range(i+1, N):
            test_ans    = ds.RmQ(i, j)       # query
            correct_ans = naiveRmQ(A, i, j)  # naive algorithm for test
            if A[test_ans] == A[correct_ans]:
                pass;
#                print("ok RmQ(%d, %d) = %d" % (i, j, test_ans));
            else:
                print("NG");
                print(f"\nyour output    = {str(test_ans)}")
                print(f"\nRmQ({i}, {j})  = {str(correct_ans)}")
                print(f"\nA[correct_ans] = {str(A[correct_ans])}")
                print(f"\nA[test_ans]    = {str(A[test_ans])}")
                sys.exit(1);
            # end if
        # end for j
    # end for i
# end main

def naiveRmQ (A, i, j):
    minval = cfg.INF
    argmin = -1
    for index in range(i, j+1):
        if A[index] < minval:
            minval = A[index]
            argmin = index
    return argmin

if __name__ == "__main__":
    main()
