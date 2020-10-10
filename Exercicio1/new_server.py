# Gabriel Yudi Sanefugi - 160027
# Wallacy Rychard Sousa Cabral - 155336

import socket
import _thread as thread
import time

HOST = ''              # Endereco IP do Servidor (não alterar)
PORT = 6000            # Porta que o Servidor esta

IP_ACESSADO = 'localhost' # Endereco IP de quem será acessado

def conectado(con, cliente):

    print('Server: Conectado por '+ str(cliente))

    while True:
        msg = con.recv(1024)
        if not msg: break
        print ('Server: '+str(cliente) +" envior: "+ str(msg))

    print('Server: Finalizando conexao do cliente do: '+ str(cliente))
    con.close()
    thread.exit()

def enviar(IP_ACESSADO,PORT):

    # Cria o Socket (Transmissor)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configurações (quem deve ser acessado?)
    server_address = (IP_ACESSADO, PORT)
    print('Remetente: Acessando o IP: {} Porta: {}'.format(*server_address))

    # Enviando mensagem
    sock.connect(server_address)

    try:   
        message = b'Sou uma mensagem, muito longo do esperado'
        print('Remetente: Enviando para {!r}'.format(message))
        sock.sendall(message)

    finally:
        print('Remetente: Fechando conexão')
        sock.close()

if __name__ == "__main__":
    
    # Cria o Socket (Receptor)
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configurações do servidor
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(1)

    print("Server: Esperando conexão...")

    while True:
        thread.start_new_thread(enviar,(IP_ACESSADO,6000))

        con, cliente = tcp.accept()
        thread.start_new_thread(conectado, (con, cliente))

        time.sleep(1)

    tcp.close()
