#!/bin/env python3
#encoding:utf-8
#coding:utf-8

import math
import numpy as np

from dahuffman import HuffmanCodec
from commpy.channelcoding import cyclic_code_genpoly
from commpy.modulation import QAMModem
import sk_dsp_comm.digitalcom as digcom
import sk_dsp_comm.fec_block as block

import matplotlib.pyplot as plt


def bitstring_to_bytes(s:str) -> bytes:
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

def bytes_to_bitstream(b:bytes) -> str:
    return ''.join(f'{x:08b}' for x in b)


def main():

    #with open("book.txt", "br") as file:
    #    phrase = file.read()

    phrase = "Hello World !"

    print('#### Reading input')

    alphabet = {}
    for char in phrase:
        alphabet[char] = alphabet.get(char, 0) + 1
    
    freqs = alphabet.copy()
    for key, value in alphabet.items():
        freqs[key] = value / len(phrase)
    
    #plt.bar(list(alphabet.keys()), list(alphabet.values()))
    #plt.show(block=True)

    print("Alphabet:", alphabet)
    print("Frequencies", freqs)
    print("Length:", len(alphabet))
    print("Entropy:", math.log(len(alphabet), 2))

    print('\n##### Generating codec')

    HuffCodec = HuffmanCodec.from_data(phrase)
    #print("Code table:")
    HuffCodec.print_code_table()

    print('\n##### Encoding using codec')

    #vencodedData = codec.encode(phrase)
    # decodedData = codec.decode(encodedData)
    # print("Equality test:", decodedData == phrase)

    HuffEncodedBytes = HuffCodec.encode(phrase)
    HuffEncodedBitstream = bytes_to_bitstream(HuffEncodedBytes)

    bitstream = np.array(list(HuffEncodedBitstream), int)
    print(bitstream)

    print('\n##### Generating Cyclic coder')

    n, k = 31, 26
    genPolynomialInt = cyclic_code_genpoly(n, k)[-1]
    genPolyBits = str(bin(genPolynomialInt))[2:]
    print("Polynome générateur:", genPolyBits)
    CyclicCoder = block.FECCyclic(genPolyBits)

    print('\n##### Channel Coding')

    # Padding
    paddingLen1 = k - np.size(bitstream) % k
    bitstreamPadded = np.pad(bitstream, (0, paddingLen1))

    # Channel coding
    channelEncoded = np.array(CyclicCoder.cyclic_encoder(bitstreamPadded), int)
    #print(np.reshape(channelCoded,(-1, n)))
    print(channelEncoded)

    # print('# Introducing 1 bit error

    # # introduce 1 bit error into each code word and decode
    # codewords = np.reshape(codewords,(16,7))
    # for i in range(16):
    #     error_pos = i % 6
    #     codewords[i,error_pos] = (codewords[i,error_pos] +1) % 2
    # codewords = np.reshape(codewords,np.size(codewords))
    # decoded_blocks = cc1.cyclic_decoder(codewords)
    # print(np.reshape(decoded_blocks,(16,4)))

    print('\n##### Generating modem')
    M = 16
    l = int(math.log(M, 2))
    modem = QAMModem(M)

    print('\n##### Modulating using modem')

    # Padding
    paddingLen2 = l - np.size(channelEncoded) % l
    channelEncodedPadded = np.pad(channelEncoded, (0, paddingLen2))

    modulatedCodewords = np.array(modem.modulate(channelEncodedPadded), complex)
    print(modulatedCodewords)

    print('\n##### Adding noise')

    EsN0 = 10
    noisedModulatedCodewords = digcom.cpx_awgn(modulatedCodewords, EsN0, l)
    
    print(noisedModulatedCodewords)

    print('\n##### Demodulating')
    demodulatedCodewords = np.array(modem.demodulate(noisedModulatedCodewords, 'hard'), int)
    depaddedDemodulatedDepadded = demodulatedCodewords[:-paddingLen2]

    print(depaddedDemodulatedDepadded)
    print("Equality test:", all(channelEncoded == depaddedDemodulatedDepadded))

    print('\n##### De-channel coding')
    channelDecoded = np.array(CyclicCoder.cyclic_decoder(depaddedDemodulatedDepadded), int)
    depaddedBitstream = channelDecoded[:-paddingLen1]

    print(depaddedBitstream)
    print("Equality test:", HuffEncodedBitstream == ''.join(depaddedBitstream.astype(str)))

    print('\n##### Decoding')
    print(depaddedBitstream.tolist())

    bytesArray = bitstring_to_bytes(''.join(depaddedBitstream.astype(str)))
    output = HuffCodec.decode(bytesArray)

    print(output)
    print("Equality test:", phrase == output)

if __name__ == "__main__":
    main()