#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enlace import *
import time

# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
#serialName = "COM4"                  # Windows(variacao de)

def main():
    # Inicializa enlace
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    # Endereco da imagem a ser salva
    imageW = "./imgs/recebida.rar"

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

    # Faz a recepção dos dados
    print ("Recebendo dados .... ")
    tempBuffer1,nRx = com.getData(1)
    inicio = time.time()
   
    tempBuffer2, tx = com.getData(130180285)

    rxBuffer = tempBuffer1 + tempBuffer2

    print("temp buffer 1 = " , tempBuffer1)
    print(type(tempBuffer2))

    fim = time.time()
    # Inicia a contagem do tempo de transmissão

    # log
    print ("Lido              {} bytes ".format(nRx))

    # Salva imagem recebida em arquivo
    print("-------------------------")
    print ("Salvando dados no arquivo :")
    print (" - {}".format(imageW))
    f = open(imageW, 'wb')
    f.write(rxBuffer)
    
    # Finaliza o tempo e calcula o tempo de transmissão
    print("O tempo total para a transmissão dos dados foi de: {}".format(fim - inicio))

    # Fecha arquivo de imagem
    f.close()

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

if __name__ == "__main__":
    main()
