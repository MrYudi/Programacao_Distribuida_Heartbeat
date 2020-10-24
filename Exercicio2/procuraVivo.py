# Gabriel Yudi Sanefugi - 160027
# Wallacy Rychard Sousa Cabral - 155336

import socket
import _thread as thread
import time

HOST = ''              # Endereco IP do Servidor (não alterar)
PORT = 6000            # Porta que o Servidor esta

#IP_ACESSADO = 'localhost' # Endereco IP de quem será acessado
LISTA_ATIVA = ['26.158.231.204','26.135.202.158','192.168.0.31',
'192.1.70.240','192.1.70.100','192.1.70.2'] # Essa lista contem todas as maquinas
LISTA_FALHA = [] # Essa lista são os que falharam

def escuta(tcp):
    # Cria o Socket (Receptor)
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configurações do servidor
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(1)

    while True:
        con, cliente = tcp.accept()
        LISTA_RESPOSTA.append(cliente[0]) # Colocana na lista o IP
        thread.start_new_thread(conectado, (con, cliente))     

    tcp.close()

def conectado(con, cliente):

    print('Server: Conectado por '+ str(cliente))

    while True:
        msg = con.recv(1024)
        if not msg: break
        print ('Server: '+str(cliente) +" envior: "+ str(msg))

    print('Server: Finalizando conexao do cliente do: '+ str(cliente))
    con.close()
    thread.exit() # verifica esse kill

def enviar(IP_ACESSADO,PORT):

    # Cria o Socket (Transmissor)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configurações (quem deve ser acessado?)
    server_address = (IP_ACESSADO, PORT)
    print('Thread Enviar: Acessando o IP: {} Porta: {}'.format(*server_address))

    try:   
        # Enviando mensagem
        sock.connect(server_address)

        message = b'heartbeat'
        #print('Remetente: Enviando para {!r}'.format(message))
        sock.sendall(message)

    finally:
        #print('Remetente: Fechando conexão')
        sock.close()
        thread.exit()

if __name__ == "__main__":
    
    # Cria o Socket (Receptor)
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configurações do servidor
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(1)
    #thread.start_new_thread(escuta,(ip,6000)) # Envia
    
    while True:
        print("Server: Enviando...")
        # ENVIANDO MENSAGENS
        LISTA_RESPOSTA = LISTA_ATIVA.copy()
        for ip in LISTA_RESPOSTA:
            thread.start_new_thread(enviar,(ip,6000)) # Envia
        LISTA_RESPOSTA = []

        print("\n----------------------------------------------------\n")
        # ESPERA POR RESPOSTA
        print("Server: Esperando conexão...")
        #time.sleep(60) # 1 min para repetir de novo
        tcp.settimeout(10)
        try:
            while True:
                con, cliente = tcp.accept()
                LISTA_RESPOSTA.append(cliente[0]) # Colocana na lista o IP
                thread.start_new_thread(conectado, (con, cliente))   
        except socket.timeout:
            print ('Server: Fim do tempo')  
            tcp.settimeout(None)

        print("\n----------------------------------------------------\n")
        # ATUALIZAR LISTA
        print("Server: Lista sendo atualizada...")
        LISTA_TMP = LISTA_ATIVA.copy()
        for i in LISTA_TMP:
            if not i in LISTA_RESPOSTA: # se não esta na lista e nem as que falho
                LISTA_FALHA.append(i) # Coloca na lista que falho
                LISTA_ATIVA.remove(i) # Remove da lista ativa

        print("Lista falha: " + str(LISTA_FALHA))
        print("Lista ativa: " + str(LISTA_ATIVA))

        if len(LISTA_ATIVA) <= 0:
            break

        time.sleep(10) # 1 min para repetir de novo
        print("\n****************************************************\n")

    tcp.close()

    print("*** FIM ***")
