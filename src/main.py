#!/usr/bin/env python3
#encoding:utf-8
#coding:utf-8
import lib
import sys

#debug mode
debug = ("--debug" in sys.argv)
#open the message
with open("The_Adventures_of_Sherlock_Holmes_A_Scandal_In_Bohemia.txt") as livre:
    message = livre.read()
"""
--- First Part ---
"""
#calculate huffman table
codec = lib.gencodetable(message)[0]
#output a byte array
enc_data = lib.encode(message, codec)
#output some binary
bit_stream = lib.bytes_to_bitstream(enc_data)
"""
--- Second Part ---
"""
#Parameters for cyclic codage
n, k = 31, 26
#padding process
bit_stream_padded = lib.padding(bit_stream, k)
#convert into an array
bit_array = lib.string_to_array(bit_stream_padded)
#do the cyclic codage
gen_poly_bits = lib.cyclic_codage(bit_array, n, k, debug)
"""
--- Third part ---
"""
