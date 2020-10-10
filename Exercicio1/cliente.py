# Cliente
import socket
import sys

IP_ACESSADO = 'localhost'  # Endereco IP do Servidor
#IP_ACESSADO = '26.158.231.204'
PORT = 6000      

# Cria o Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configurações (quem deve ser acessado?)
server_address = (IP_ACESSADO, PORT)
print('Acessando o IP: {} Porta: {}'.format(*server_address))

# Enviando mensagem
sock.connect(server_address)

try:   
    message = b'Sou uma mensagem, muito longo do esperado'
    #message = b'Sou uma mensagem'
    print('Enviando para {!r}'.format(message))
    sock.sendall(message)

    # Espera por resposta
    #amount_received = 0
    #amount_expected = len(message)

    #while amount_received < amount_expected:
    #    data = sock.recv(16)
    #    amount_received += len(data)
    #    print('Recebeu: {!r}'.format(data))

finally:
    print('Fechando conexão')
    sock.close()
