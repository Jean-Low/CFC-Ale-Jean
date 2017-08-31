# CFC-Ale-Jean
Descrição do handshake implementado: 
	O handshake funciona com 3 transmissões.
	Primeiro o cliente transmite um pacote de sincronização (SYN) e espera por 50 milissegundos, após esse tempo, ele verifica se recebeu alguma resposta, em caso negativo, ele retransmite o sinal, se esse processo demorar 2000 milissegundos, o cliente retorna um erro de Timeout.
	O server espera receber um sinal, quando ele recebe algo maior do que a quantidade de bits esperada no sinal de sincronização (SYN), ele verifica a integridade do sinal. Em caso negativo, ele descarta o buffer atual e transmite um SYN e um pacote de não reconhecimento (NACK), em caso positivo ele transmite o SYN e um pacote de reconhecimento (ACK), e passa a aguardar a resposta do client por 2000 milissegundos.
    Quando o client recebe a resposta, no caso de um pacote ACK, ele devolve outro pacote ACK e assume que a comunicação esta estabelecida.

Diagrama dos pacotes (SYN,ACK,NACK):
    
Diagramas de transmição e recepção:

Timeout:
    O timeout de 2000 milissegundos foi escolhido depois de realizado o seguinte teste:
    Em 4000 milissegundos, rodar o codigo 8 vezes, no caso de todos funcionarem, reduzir na metade o tempo do timeout.
    Com 1000 milisegundos houve dois erros entre os 8 testes, então ficou definido 2000 milissegundos.

A diferenciação dos pacotes contra pacotes com payload:
    O header inclue um byte responsavel por informar o tipo do pacote, caso esse byte (nomeado label no codigo) seja b'0x00', é um arquivo de payload.
    outros valores nesse byte informão outros tipos de pacotes, o SYN, ACK e NACK são, espectivamente: b'0xff' , b'0xf0' , b'0x0f'.
    Esse valores foram escolhidos de forma que seja dificil ara o codigo binario, se corrompido, se transforme em outro valor possivel, esse caso o destinatario não perceberia um erro e prosseguiria a operação com um pacote errado.
