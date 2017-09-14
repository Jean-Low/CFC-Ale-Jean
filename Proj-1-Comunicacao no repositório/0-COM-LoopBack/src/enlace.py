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
        self.queuedPck   = []
        self.receivedPck = []
        self.meta        = None

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
        packet= None
        
        dic = {
            'small': 17,
            'medium': 543, #signature + label + thresh + pckAmount + filenameSize + content + checksum + signature : +8 +1 +2 +2 +2 +512 +8 +8
            'big': 13 + 2**16 + 16} #header + payload + eop
        size= dic[size]
        
        while timeout > 0 or timeout == -1111:
            if (timeout != -1111):
                timeout -= 100
            time.sleep(0.1)
            if(self.rx.getBufferLen() >= size ):
                packet = self.rx.getBuffer(size)
                label= packet[8]
                break
        
        
        if(  packet!=None and (packet[0:8] != 'F.A.S.T.'.encode() or packet[-8:] != 'S.L.O.W.'.encode())): #confere as assinaturas de header e eop
            label = 170
            
        if( (label==0 or label==131) and checksum(packet[0:-16]) != packet[-16:-8]): #confere o checksum de header+payload contra o checksum no eop
            label= 151
        
        
        dic = {
            255 :'SYN',
            240 :'ACK',
            170 :'MALFORMED',
            151 :'CORRUPTED',
            131 :'META',
            85  :'TIMEOUT',
            15  :'NACK'}
        
        label= dic[label]
        print ("Resultado do packet ouvido: "+label)
        self.rx.clearBufferUntilSignature('F.A.S.T.'.encode())
        return (label, packet)

    def getMetaName(self, packet):
        return packet[15: 15+512].decode('utf-8') #torcemos para que não tenhamos que nos preocupar algo que não utf-8

    def getMetaPacketAmount(self, packet):
        return int.from_bytes(packet[11:13], byteorder='big')

    def collapseData(self):
        data= bytes(bytearray())
        i=0
        while(i!= len(self.receivedPck)):
            data+= self.receivedPck[i][13:-16]
            i+= 1
        self.receivedPck= []
        return data
    
    def sendPacket(self, label, number= 0):
        time.sleep(0.1) #pra dar tempo do outro se preparar pra receber, testar diminuir ou remover este valor depois

        print ("Enviando packet tipo ", label)

        dic = {'SYN' : bytes([255]),
                'ACK' : bytes([240]),
                'NACK' : bytes([15]),
                'META' : bytes([131]),
                'DATA' : bytes([0])}
        label = dic[label]

        if(label==bytes([255]) or label==bytes([240]) or label==bytes([15])):

            signature = 'F.A.S.T.'.encode()
            
            header = signature + label
            
            signature = 'S.L.O.W.'.encode()
            
            eop = signature
            packet= header + eop

        elif(label==bytes([131])):
            packet= self.meta

        elif(label==bytes([0])):
            packet= self.queuedPck[number]
        
        self.tx.sendBuffer(packet)

    def packageData(self, data, filename):
        
        self.queuedPck=[]        

        #bytes do payload de cada packet: 2**16
        payloadsize= 2**16
        packetamount= ( (len(data)-1)//payloadsize )+1
        
        ##Fazer metadata
        #Para suportar o maior número possível de filesystems, suportaremos filenames de até 512 bytes
        #tamanho máximo de um arquivo transferido por uma sprint apenas, 4Gb = 2^32, 4 bytes
        signature = 'F.A.S.T.'.encode()
        label= bytes([131])
        thresh= len(data)%payloadsize
        thresh= bytes([((thresh//256)%256), (thresh%256)])
        content= filename.encode()
        filenameSize= bytes([(((len(content)//256)%256)), (len(content)%256)])
        pckAmount= bytes([((packetamount//256)%256), (packetamount%256)])
        header= signature + label + thresh + pckAmount + filenameSize

        content= content+bytes([0])*(512-len(content))

        signature= 'S.L.O.W.'.encode()
        eop= self.checksum(header + content) + signature
        
        self.meta=(header+content+eop)

        
        #Fazer o packaging        

        data+= (((2**16) - (len(data)%2**16)) %2**16)*bytes([0]) #oh god
        
        counter=0
        while(counter != packetamount):
            thisdata=data[counter*(2**16): (counter+1)*(2**16)]
            self.queuedPck.append( self.createPacket( thisdata, counter) )
            counter+= 1

    def createPacket(self, payload, counter):
    
        signature = 'F.A.S.T.'.encode()
        label = bytes([0])
        #size= 2**16 #size do payload, constante para packets com payload
        size= bytes([0 , 0]) #TODO: consertar  
        counter= bytes([((counter//256)%256), (counter%256)])
        
        header= signature + label + counter + size
        #13 bytes
        
        signature = 'S.L.O.W.'.encode()
        
        eop = self.checksum(header+payload) + signature
        #16 bytes
        
        return header + payload + eop

    def checksum (self, data):
    #Implementação nossa de um CRC-64 bits

        data= int.from_bytes(data, 'big')
        data=data*(2**63) #append com zeros
        print("Rodando checksum")
        while (data.bit_length() > 63):
            print(data.bit_length())
            sumNum = 2 ** (data.bit_length()-64)
            key = 9241846741563846107 #um int aleatoriamente selecionado de 64 bits
            powerkey=key*sumNum
            
            data^=powerkey
        
        return bytes([  (data//(256**7)) % 256, (data//(256**6)) % 256,
            (data//(256**5)) % 256, (data//(256**4)) % 256, (data//(256**3)) % 256,
            (data//(256**2)) % 256, (data//256) % 256, data % 256])

    ##def sendData(self, data):
    #    """ Send data over the enlace interface
    #    """
    #    
    #    #bytes do payload de cada packet: 2**16
    #    packetamount= ( len(data)//2**16 )+1
    #    
    #    data+= (((2**16) - (len(data)%2**16)) %2**16)*bytes([0]) #oh god
    #    
    #    counter=0
    #    while(counter!=packetamount):
    #        thisdata=data[counter*(2**16), (counter+1)*(2**16)]
    #        packet= createPacket( counter);
    #        #sleep + listen?
    #        
    #        #
    #        counter+= 1
    #    
    #    counter = bytes([n // 256, n % 256])
    #    
    ##    self.tx.sendBuffer(data)

    ##def getData(self, size):
    #    """ Get n data over the enlace interface
    #    Return the byte array and the size of the buffer
    #    """
    #    data = self.rx.getNData(size)
    #    
    #    #checar checksum
    ##    return(data, len(data))
