import sys
from  pathlib import Path
sys.path.append(str(Path(__file__).absolute().parents[1]))
from lib.rmq import RmQDataStructure

def main():
    A = [2, 5, 6, 1, 9, 4]
    ds = RmQDataStructure(A) # preprocess
    i, j = 1, 4
    ans = ds.RmQ(i, j)       # query
    print(ans);
      
if __name__ == "__main__":
    main()
