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

serialName = "/dev/ttyACM0"       # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
#serialName = "COM3"                  # Windows(variacao de)

def main():
    # Inicializa enlace
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    # Endereco da imagem a ser transmitida
    filename = sys.argv[1]


    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

    # Carrega imagem
    print ("Carregando imagem para transmissão :")
    print (" - {}".format(filename))
    print("-------------------------")

    com.packageData(open(filename, 'rb').read(), filename)

    inicio= time.time()
    ###STATE MACHINE START###

    # Handshake
    timeout = 512
    while True:
        print('Estabelecendo canal de comunicação...')
        state = 0
        if state == 0:
            com.sendPacket('SYN')
            state = 1
        if state == 1:
            answer, null = com.listenPacket(timeout, 'small')
            if (answer == 'SYN' or answer == 'ACK'):
                tmp=answer
                state = 2
            else:
                state = 0
        if state == 2:
            answer, null = com.listenPacket(timeout, 'small')
            if ((answer == 'SYN' or answer == 'ACK') and tmp != answer):
                state = 3
            else:
                com.sendPacket('NACK')
                state = 0
        if state == 3:
            com.sendPacket('ACK')
            break
        com.sendPacket('NACK')
        print('Erro;  ' , answer, '. Recomeçando handshake')
    print('Handshake realizado com sucesso!')
    
    # Metadata
    timeout= 512
    while True:
        print('Enviando metadata...')
        com.sendPacket('META')
        answer, null= com.listenPacket(timeout, 'small')
        if(answer=='ACK'):
            break
        com.sendPacket('NACK')
        print('Erro;  ' , answer, '. Recomeçando envio de metadata')
    print('Envio da metadata realizado com sucesso!')

    # File Transmission
    timeout= 512
    counter= 0
    while True:
        print('Enviando packet '+str(counter+1)+' de '+str(len(com.queuedPck)))
        com.sendPacket('DATA', counter)
        answer, null= com.listenPacket(timeout, 'small')
        print(com.queuedPck[counter])
        if (answer== 'ACK'):
            counter+= 1
            if (counter==len(com.queuedPck)):
                break
        else:
            com.sendPacket('NACK')
            print('Erro;  ' , answer, '. Recomeçando o envio a partir do packet ', counter+1)
    print('Fim do envio do arquivo')

    ###STATE MACHINE END###

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
