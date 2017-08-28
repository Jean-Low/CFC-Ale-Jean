#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enlace import *
import time

# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)

def main():
    # Inicializa enlace
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    # Endereco da imagem a ser salva
    imageW = "./imgs/recebida.png"

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

    # Faz a recepção dos dados
    eopSize = 8 #16 when checksum is in
    print ("Recebendo dados .... ")
    #tempBuffer1,nRx = com.getData(1)
    #inicio = time.time()

   
    headerBuffer, tx = com.getData(13)
    inicio = time.time()


    #headerBuffer = tempBuffer1 + tempBuffer2
    #print('headerBuffer : ',headerBuffer)
    size = int(headerBuffer[-2]) * 256 + int(headerBuffer[-1])
    print('expecting ', size + 21,' bytes of data')
    
    rxBuffer,tx = com.getData(size)
    potentialEop, tx = com.getData(eopSize)
    print('end of packet is ', potentialEop)
    
    if(potentialEop == 'S.L.O.W.'.encode()):
        print('probably not corrupted')
    else:
        print('file corrupted')

    fim = time.time()
    # Inicia a contagem do tempo de transmissão

    # log
    print ("Received        {} bytes of usefull data".format(size))
    
    print(inicio)
    

    # Salva imagem recebida em arquivo
    print("-------------------------")
    print ("Salvando dados no arquivo :")
    print (" - {}".format(imageW))
    f = open(imageW, 'wb')
    f.write(rxBuffer)
    
    # Finaliza o tempo e calcula o tempo de transmissão
    print("O tempo total de transmissão: ", '%.2f' % ((fim - inicio) * 1000), 'ms')

    # Fecha arquivo de imagem
    f.close()

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

if __name__ == "__main__":
    main()
