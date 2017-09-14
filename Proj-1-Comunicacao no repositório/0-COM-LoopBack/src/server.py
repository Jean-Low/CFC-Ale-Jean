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

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")
    
    inicio = time.time()

    ###STATE MACHINE START###

    # Handshake
    timeout= 100
    while True:
        print('Esperando por canal de comunicação . . .')
        state = 0
        if state == 0:
            answer, null = com.listenPacket(-1111, 'small')
            if (answer == 'SYN'):
                state = 1
        if state == 1:
            com.sendPacket('SYN')
            com.sendPacket('ACK')
            answer, null= com.listenPacket(timeout, 'small')
            if (answer == 'ACK'):
                break
        com.sendPacket('NACK')
        print('Erro;  ' , answer, '. Recomeçando handshake')
    print('Handshake realizado com sucesso!')

    # Metadata
    timeout= 100
    while True:
        print('Esperando metadata...')
        answer, meta= com.listenPacket(-1111, 'medium')
        if(answer=='META'):
            com.sendPacket('ACK')
            com.meta= meta
            packetAmount= com.getMetaPacketAmount(meta)
            filename= com.getMetaName(meta)
            break
        com.sendPacket('NACK')
        print('Erro;  ' , answer, '. Recomeçando recebimento de metadata')
    print('Recebimento da metadata realizado com sucesso!')

    # File Transmission
    timeout= 100
    counter= 0
    while True:
        print('Esperando packet '+str(counter)+' de '+str(packetAmount) )
        answer, packet= com.listenPacket(-1111, 'big')
        if (answer== 'DATA'):
            counter+= 1
            com.receivedPck.append(packet)
            com.sendPacket('ACK')
            if (counter==packetAmount):
                break
        else:
            com.sendPacket('NACK')
            print('Erro;  ' , answer, '. Recomeçando a receber a partir do packet ', counter)
    print('Fim do recebimento do arquivo')

    ###STATE MACHINE END###


    data= com.collapseData()
    
    fim = time.time()

    # log
    print ("Recebemos {} bytes de data útil".format(len(data)))
    

    # Salva imagem recebida em arquivo
    print("-------------------------")
    print ("Salvando dados no arquivo :")
    print (" - {}".format(filename))
    f = open(filename, 'wb')
    f.write(data)
    
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
