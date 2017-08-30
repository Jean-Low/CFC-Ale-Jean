#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Prof. Rafael Corsi
#  Abril/2017
#  Aplicação
####################################################

import sys
from enlace import *
import time
# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"       # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)

def main():
    # Inicializa enlace
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    # Endereco da imagem a ser transmitida
	#imageR = "./imgs/imageC.png"
    imageR = sys.argv[1]


    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

    # Carrega imagem
    print ("Carregando imagem para transmissão :")
    print (" - {}".format(imageR))
    print("-------------------------")
    txBuffer = open(imageR, 'rb').read()
    txLen    = len(txBuffer)
    
    # Handshake
    while true:
        print('Estabelecendo canal de comunicação')
        state = 0
        if state == 0:
            com.sendSignal('SYN')
            state = 1
        if state == 1:
            answer = com.listenSignal(2500)
            if (answer == 'SYN' or answer == 'ACK')
                tmp=answer
                state = 2
            else:
                state = 0
        if state == 2:
            answer = com.listenSignal(2500)
            if (answer == 'SYN' or answer == 'ACK') and tmp != answer
                state = 3
            else:
                state = 0
        if state == 3:
            com.sendSignal('ACK')
            break
        print('ERROR: ' , answer, '\nTrying again')

    
    # Transmite imagem
    print("Transmitindo .... {} bytes".format(txLen))
    com.sendData(txBuffer)
    inicio = time.time()

    # espera o fim da transmissão
    while(com.tx.getIsBussy()):
        pass

    # Atualiza dados da transmissão
    txSize = com.tx.getStatus()
    print ("Transmitido       {} bytes ".format(txSize))
	
	# Calcula e exibe o tempo de execução
    mil = 1000
    deltaT = (time.time() - inicio)
    print("Tempo de transmição: " , "%.2f" % deltaT , " segundos\n")

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

if __name__ == "__main__":
    main()
