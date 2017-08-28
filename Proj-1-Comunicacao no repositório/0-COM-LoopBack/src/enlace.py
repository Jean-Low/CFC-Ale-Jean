#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Prof. Rafael Corsi
#  Abril/2017
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Construct Struct
from construct import *

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
    def sendData(self, data):
        """ Send data over the enlace interface
        """
        
        n = 1 # ;3  change
        size= len(data)       

        signature = 'F.A.S.T.'.encode()
        label = bytes([0])
        counter = bytes([n // 256, n % 256])
        size = bytes([size//256,size%256])
        
        header = signature + label + counter + size
        
        #TODO Checksum
        signature = 'S.L.O.W.'.encode()
        
        eop = signature
        
        data = header + data + eop
        
        self.tx.sendBuffer(data)

    def getData(self, size):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        data = self.rx.getNData(size)
        return(data, len(data))
