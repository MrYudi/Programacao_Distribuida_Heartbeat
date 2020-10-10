# Gabriel Yudi Sanefugi - 160027
# Wallacy Rychard Sousa Cabral - 155336

import socket
import _thread as thread
import time

HOST = ''              # Endereco IP do Servidor (não alterar)
PORT = 6000            # Porta que o Servidor esta

IP_ACESSADO = 'localhost' # Endereco IP de quem será acessado

def enviar(IP_ACESSADO,PORT):

    # Cria o Socket (Transmissor)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configurações (quem deve ser acessado?)
    server_address = (IP_ACESSADO, PORT)
    print('Cliente: Acessando o IP: {} Porta: {}'.format(*server_address))

    # Enviando mensagem
    sock.connect(server_address)

    print('Cliente: Fechando conexão')
    sock.close()

if __name__ == "__main__":
    
    # Cria o Socket (Receptor)
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configurações do servidor
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(1)

    print("Cliente: Esperando conexão...")

    while True:
        con, cliente = tcp.accept()
        print('Cliente: Conectado por '+ str(cliente))
        con.close()

        thread.start_new_thread(enviar,(cliente[0],6000))  

    tcp.close()
