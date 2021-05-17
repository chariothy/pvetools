import math, sys
def pad_size(ori_size, block_size=64): 
    return math.ceil(ori_size*1.0/block_size/1024)*block_size*1024-ori_size
print(pad_size(int(sys.argv[1])))
