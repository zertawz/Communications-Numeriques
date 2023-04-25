#!/usr/bin/env python3
#encoding:utf-8
#coding:utf-8
import numpy as np
import dahuffman
import math
import sk_dsp_comm.fec_block as block 
from commpy.channelcoding import cyclic_code_genpoly

"""
--- SENDING PART ---
"""
#Generate the huffman table from a message
def gencodetable(message, debug = False):
    #generating the working dictionnary
    dic = {}
    for i in message:
        if i not in dic.keys():
            dic[i] = 1/len(message)
        else:
            dic[i] += 1/len(message)
    #calculate the entropy
    entropie = math.log(len(list(dic.keys())))
    #huffman table
    codec = dahuffman.HuffmanCodec.from_data(message)
    table = codec.get_code_table()
    #ligne de debugage
    if debug:
        print(table)
    #output codec correspond à l'instance
    return(codec, table, entropie)

#Encoding the message with a huffman table
def encode(message, codec, debug = False):
    enc_data = codec.encode(message)
    if debug:
        print(enc_data)
    return(enc_data)

#Converting byte to binary
def bytes_to_bitstream(enc_data, debug = False):
    binary = ''.join(f'{x:08b}' for x in enc_data)
    if debug:
        print(binary)
    return(binary)

#adding padding before converting
def padding(bit_stream, k, debug = False):
    #number of bits to add
    bourrage = k - len(bit_stream) % k
    #generating the string to add
    padding = "0" * bourrage
    #bit_stream with padding
    bit_stream_padded = bit_stream + padding
    if debug:
        print(bit_stream_padded)
    return (bit_stream_padded)

#convert bit stream string to an array
def string_to_array(bit_stream_padded, debug = False):
    bit_array = np.array(list(bit_stream_padded), int)
    if debug:
        print(bit_array)
    return (bit_array)

#Calculate Polynomes of the cyclic codage
def cyclic_codage(bit_array, n, k, debug = False):
    #Calculate polynomial
    gen_polynomial_int = cyclic_code_genpoly(n, k)[0]
    #Convert into binary string
    gen_poly_bits = str(bin(gen_polynomial_int))[2:]
    #generate an object that makes you able to do cyclic coding
    cyclic_coder = block.FECCyclic(gen_poly_bits)
    if debug:
        print(cyclic_coder)
    return (cyclic_coder)

#Encoding bit stream with the cyclic codage
def cyclic_encoding(bit_array, cyclic_coder, debug = False):
    #Encode bit stream using cyclic_coder generated before
    channel_encoded = np.array(cyclic_coder.cyclic_encoder(bit_array), int)
    if debug:
        print(channel_encoded)
    return channel_encoded

#Adding padding before modulation
#Modulation
#Gaussian Noise

"""
--- RECEIVING PART ---
"""
def bitstring_to_bytes(encry):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')
