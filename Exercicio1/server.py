# Servidor
      
import socket
import sys

PORT_LOCAL = 6000 
IP_LOCAL = 'localhost'

# Cria socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configuração do SOCKET (no caso local)
server_address = (IP_LOCAL, PORT_LOCAL)
print('IP: {} Porta: {}'.format(*server_address))
sock.bind(server_address)

# Ativar leitura (1 conexão)
sock.listen(1) 

while True:
    # Espera conexão
    print('Espera conexão...')
    connection, client_address = sock.accept()
    try:
        print('Conectando do ', client_address)   

        # Receba a mensagem e envia de volta.
        while True: 
            data = connection.recv(16)
            print('Recebeu {!r}'.format(data))
            if data:
                #print('Manda de volta para o cliente')
                connection.sendall(data)
            else:
                print('Nenhum dado do ', client_address)
                break

    finally:
        # Limpa conexão
        connection.close()