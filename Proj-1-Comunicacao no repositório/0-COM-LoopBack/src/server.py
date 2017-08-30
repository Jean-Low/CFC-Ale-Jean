#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enlace import *
import time
import serial.tools.list_ports


# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

def main():
    #encontra a porta do arduino
    serialName = None 
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'Arduino' in p[1]:
            serialName = p[0]
    print(serialName)
    if(serialName == None):
        print('Arduino não encontrado!')
        return
    # Inicializa enlace
    com = enlace(serialName)
    
    # Ativa comunicacao
    com.enable()


    # Endereco da imagem a ser salva
    imageW = "./imgs/recebida.png"
    
    # Handshake
    timeout = 2000
    error= False
    while True:
        print('Esperando por canal de comunicação . . .')
        state = 0
        if state == 0:
            answer = com.listenSignal(-1111)
            if (answer == 'SYN'):
                state = 1
            else:
                error= True
                state = 1
        if state == 1:
            time.sleep(0.1)
            com.sendSignal('SYN')
            
            if (error):
                error= False
                time.sleep(0.1)
                com.sendSignal('ACK')
                
                state= 0
            else:
                state = 2
            
        if state == 2:
            time.sleep(0.1)
            com.sendSignal('ACK')
            state = 3
        if state == 3:
            answer = com.listenSignal(timeout)
            if (answer == 'ACK'):
                break
            state = 0
        print('ERROR: ' , answer, '\nTrying again')
    
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
    
    fim = time.time()
    
    print('end of packet is ', potentialEop)
    
    if(potentialEop == 'S.L.O.W.'.encode()):
        print('probably not corrupted')
    else:
        print('file corrupted')

    # Inicia a contagem do tempo de transmissão

    # log
    print ("Received        {} bytes of usefull data".format(size))
    

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
