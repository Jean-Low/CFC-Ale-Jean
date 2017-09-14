#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Prof. Rafael Corsi
#  Abril/2017
#  Camada de Enlace
####################################################

import time
import sys
import threading

# Class
class RX(object):
    """ This class implements methods to handle the reception
        data over the p2p fox protocol
    """
    
    def __init__(self, fisica):
        """ Initializes the TX class
        """
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.threadStop  = False
        self.threadMutex = True
        self.READLEN     = 1024

    def thread(self):
        """ RX thread, to send data in parallel with the code
        """
        while not self.threadStop:
            if(self.threadMutex == True):
                rxTemp, nRx = self.fisica.read(self.READLEN)
                if (nRx > 0):
                    self.buffer += rxTemp
                time.sleep(0.001)

    def threadStart(self):
        """ Starts RX thread (generate and run)
        """
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        """ Kill RX thread
        """
        self.threadStop = True

    def threadPause(self):
        """ Stops the RX thread to run

        This must be used when manipulating the Rx buffer
        """
        self.threadMutex = False

    def threadResume(self):
        """ Resume the RX thread (after suspended)
        """
        self.threadMutex = True

    def getIsEmpty(self):
        """ Return if the reception buffer is empty
        """
        if(self.getBufferLen() == 0):
            return(True)
        else:
            return(False)

    def getBufferLen(self):
        """ Return the total number of bytes in the reception buffer
        """
        return(len(self.buffer))

    def getAllBuffer(self, len):
        """ Read ALL reception buffer and clears it
        """
        self.threadPause()
        b = self.buffer[:]
        self.clearBuffer()
        self.threadResume()
        return(b)

    def getBuffer(self, nData):
        """ Remove n data from buffer
        """
        self.threadPause()
        b           = self.buffer[0:nData]
        #self.buffer = self.buffer[nData:]
        self.threadResume()
        return(b)

    def getNData(self, size):
        """ Read N bytes of data from the reception buffer

        This function blocks until the number of bytes is received
        """
        while(self.getBufferLen() < size):
            
            sys.stdout.write("Received: " + str(self.getBufferLen()) + "/" + str(size))
            sys.stdout.write("\r")
            sys.stdout.flush()
            time.sleep(0.05)

        sys.stdout.write("\nReceived: "+str(self.getBufferLen()) + "/" + str(size) + "\n")



        return(self.getBuffer(size))


    def clearBuffer(self):
        """ Clear the reception buffer
        """
        self.buffer = b""
        
    def clearBufferUntilSignature(self, signature):
        #passo 1: tirar o primeiro byte
        temp= self.buffer[1:]
        
        i=0
        while(i!=len(temp)):
            if(temp[i]==signature[0]):
                if(temp[i:i+len(signature)] == signature):
                    break
            i+=1
            
        i+=1
        #i é o que eu quero
        
        if(i!=len(self.buffer)):
            self.buffer = self.buffer[i:]
        else:
            self.clearBuffer()
            

