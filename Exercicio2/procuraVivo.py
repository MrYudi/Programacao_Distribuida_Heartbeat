# Gabriel Yudi Sanefugi - 160027
# Wallacy Rychard Sousa Cabral - 155336

import socket
import _thread as thread
import time

HOST = ''              # Endereco IP do Servidor (não alterar)
PORT = 6000            # Porta que o Servidor esta

#IP_ACESSADO = 'localhost' # Endereco IP de quem será acessado
LISTA_ATIVA = ['127.0.0.1'] # Essa lista contem todas as maquinas
LISTA_FALHA = [] # Essa lista são os que falharam

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
    print('Remetente: Acessando o IP: {} Porta: {}'.format(*server_address))

    # Enviando mensagem
    sock.connect(server_address)

    try:   
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
    
    while True:
        print("Server: Enviando...")
        # ENVIANDO MENSAGENS
        LISTA_TMP = LISTA_ATIVA.copy()
        for ip in LISTA_TMP:
            thread.start_new_thread(enviar,(ip,6000)) # Envia
        LISTA_TMP = []

        # ESPERA POR RESPOSTA
        print("Server: Esperando conexão...")
        tcp.settimeout(10)
        try:
            while True:
                con, cliente = tcp.accept()
                LISTA_TMP.append(cliente[0]) # Colocana na lista o IP
                thread.start_new_thread(conectado, (con, cliente))   
        except socket.timeout:
            print ('Server: Fim do tempo')  
            tcp.settimeout(None)

        # ATUALIZAR LISTA
        print("Server: Lista sendo atualizada...")
        for i in LISTA_ATIVA:
            if not i in LISTA_TMP: # se não esta na lista e nem as que falho
                LISTA_FALHA.append(i) # Coloca na lista que falho
                LISTA_ATIVA.remove(i) # Remove da lista ativa

        print("Lista falha:")
        print(LISTA_FALHA)
        print("Lista ativa:")
        print(LISTA_ATIVA)

        time.sleep(60) # 1 min para repetir de novo

    tcp.close()
