#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Prof. Rafael Corsi
#  Abril/2017
#  Camada de Enlace
####################################################

import time
import math

# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx
from enlaceRx import RX
from enlaceTx import TX


class enlace(object):
    """ This class implements methods to the interface between Enlace and Application
    """

    def __init__(self, name):
        """ Initializes the enlace class
        """
        self.fisica      = fisica(name)
        self.rx          = RX(self.fisica)
        self.tx          = TX(self.fisica)
        self.connected   = False

    def enable(self):
        """ Enable reception and transmission
        """
        self.fisica.open()
        self.rx.threadStart()
        self.tx.threadStart()

    def disable(self):
        """ Disable reception and transmission
        """
        self.rx.threadKill()
        self.tx.threadKill()
        time.sleep(1)
        self.fisica.close()

    ################################
    # Application  interface       #
    ################################
    
    def listenPacket(self ,timeout, size='small'): #valor -1111 desativa o timeout
        label = 85
        buffer= None
        
        dic = {
            'small': 17,
            'big': 2**16 + 13 + 16} #payload + header + eop
        size= dic[size]
        
        while timeout > 0 or timeout == -1111:
            if (timeout != -1111):
                timeout -= 100
            time.sleep(0.1)
            if(self.rx.getBufferLen() >= size ):
                buffer = self.rx.getBuffer(size)
                label= buffer[8]
                break
        
        
        if(  buffer!=None and (buffer[0:8] != 'F.A.S.T.'.encode() or buffer[-8:] != 'S.L.O.W.'.encode())): #confere as assinaturas de header e eop
            label = 170
            
        if( label=0 and checksum(buffer[0:-16]) != buffer(-16:-8)): #confere o checksum de header+payload contra o checksum no eop
            label= 151
        
        
        dic = {
            255 :'SYN',
            240 :'ACK',
            170 :'MALFORMED',
            151 :'CORRUPTED'
            85 :'TIMEOUT',
            15 :'NACK'}
        
        label= dic[label]
        print ("Resultado do packet ouvido: "+label)
        self.rx.clearBufferUntilHeader()
        return dic[label]
            
        #clear buffer afterward if data
    
    def clearBufferUntilHeader():
        #tira o primeiro byte
        
        
    
    def sendSignal(self, signal):
        dic = {'SYN' : bytes([255]),
                'ACK' : bytes([240]),
                'NACK' : bytes([15])}
                    

        signature = 'F.A.S.T.'.encode()
        label = dic[signal]
        
        header = signature + label
        
        signature = 'S.L.O.W.'.encode()
        
        eop = signature
        
        print ("Packet Enviado: ",signal)
        signal = header + eop
        
        self.tx.sendBuffer(signal)
        
    def sendData(self, data):
        """ Send data over the enlace interface
        """
        
        #bytes do payload de cada packet: 2**16
        packetamount= ( len(data)//2**16 )+1
        
        data+= (((2**16) - (len(data)%2**16)) %2**16)*bytes([0]) #oh god
        
        counter=0
        while(counter!=packetamount):
            thisdata=data[counter*(2**16), (counter+1)*(2**16)]
            packet= createPacket( counter);
            #sleep + listen?
            
            #
            counter+= 1
        
        counter = bytes([n // 256, n % 256])
        
        self.tx.sendBuffer(data)
        
    def createPacket(payload, counter):
    
        signature = 'F.A.S.T.'.encode()
        label = bytes([0])
        size= 2**16 #size do payload, constante pra packets com payload
        
        header= signature + label + counter + size
        #13 bytes
        
        signature = 'S.L.O.W.'.encode()
        
        eop = checksum(header+payload) + signature
        #16 bytes
        
        return header + payload + eop
        
        

    ##def getData(self, size):
    #    """ Get n data over the enlace interface
    #    Return the byte array and the size of the buffer
    #    """
    #    data = self.rx.getNData(size)
    #    
    #    #checar checksum
    ##    return(data, len(data))
    
    def checksum (self, data): #Implementação nossa de um CRC-64 bits
        data= int.from_bytes(data, 'big')
        data=data*(2**63) #append
        
        while (data.bit_length() > 63):
            sumNum = 2 ** (data.bit_length()-64)
            key = 9241846741563846107 #um int aleatoriamente selecionado de 64 bits
            powerkey=key*sumNum
            
            data^=powerkey
        
        print(bin(data))
        print(data)
        return bytes([  (data//(256**7)) % 256, (data//(256**6)) % 256,
            (data//(256**5)) % 256, (data//(256**4)) % 256, (data//(256**3)) % 256,
            (data//(256**2)) % 256, (data//256) % 256, data % 256])
            
        