#!/usr/bin/env python3
#encoding:utf-8
#coding:utf-8 
import math
import numpy as np

# introduce 1 bit error into each code word and decode
codewords = np.reshape(codewords,(16,7))
for i in range(16):
    error_pos = i % 6
    codewords[i,error_pos] = (codewords[i,error_pos] +1) % 2
codewords = reshape(codewords,size(codewords))
decoded_blocks = cc1.cyclic_decoder(codewords)
print(reshape(decoded_blocks,(16,4)))
