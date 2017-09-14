import math
import random

def checksum (data):
    data= int.from_bytes(data, 'big')
    data=data*(2**63) #append
    #agora funciona?
    
    while (data.bit_length() > 63):
        sumNum = 2 ** (data.bit_length()-64)
        key = 9241846741563846107 #um int aleatoriamente selecionado de 64 bits
        powerkey=key*sumNum
        
        data^=powerkey
    
    print(bin(data))
    print(data)
    return bytes([  (data//(256**7)) % 256, (data//(256**6)) % 256, (data//(256**5)) % 256, (data//(256**4)) % 256, (data//(256**3)) % 256, (data//(256**2)) % 256, (data//256) % 256, data % 256])
    
hash= checksum(b'Pedro may be a huge lolicon... maybe...I have no proof...\nyet.')
#print(hash)