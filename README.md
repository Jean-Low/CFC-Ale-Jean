# CFC-Ale-Jean
Descrição da fragmentação:
    A fragmentação separa a data em pacotes menores, reduzindo a chance de erros durante a transmição e facilitando a correção dos mesmos. É definido o tamanho que cada pacote tera e, antes da execução do handshake, ele é separado nos n pacotes, cada um contem um HEAD e um EOP proprio. O Head indica, entre outras coisas, o tipo de pacote, existe o METADATA, que contem informações como o nome do arquivo e tamanho, o PAYLOAD, que basicamente é um pacote de dados prontos para serem concatenados. O EOP contem um signature e um Checksun, TODOS OS PACOTES DE METADATA E PAYLOAD CONTEM UM CHECKSUM, esse checksum verifica o HEADER + CONTENT de cada pacote. os pacotes tem tamanhos fixos, o METADATA contem 543 bytes, e os PAYLOADS tem um tamanho definido no enlace (normalmente 64 KB). Quando a data é fragmentada, o ultimo payload recebe menos dados do que o nescesario para completar um pacote cheio, como o protocolo espera um tamanho fixo, esse ultimo pacote recebe um numero de bytes vazios (0x00) para completar o tamanho, o server usa o tamanho do arquivo para saber onte separar esses bytes extras.
    
Campos do HEAD:
    Metadata:
        Signature + Label + FileSize + FileNameSize
        
        Signature - Assinatura do protocolo F.A.S.T.
        Label - Indica que é um Metadata
        FileSize - Tamanho total do arquivo em bytes
        FileNameSize Tamanho do nome do arquivo em bytes
    
    Payload:
        Signature + Label + Counter + Size(obrigatorio, mas não nescessario)
        
        Counter - Mostra a contagem de pacotes, usado para saber a ordem dos dados.
        Size - Tamanho do pacote (fixo, mas nescessario para a entrega, sera removido após o projeto)
        

Tempo de timeout:
    1 segundo, por que antes usavamos 2 segundos, com as modificações atuais, não teremos mais um problema usando um tempo menor, mas como ja tivemos problemas com apenas 1 segundo antes, decidimos não diminuir muito.
    
Explicação do Key do CRC:
    Fizemos um CRC proprio, que usa uma key de 64 bits. Como o a key usamos um numero random de 64 bits. no caso:
        9241846741563846107
    Ou em binario:
        1000000001000001101000101010010101100011100000111010110111011011