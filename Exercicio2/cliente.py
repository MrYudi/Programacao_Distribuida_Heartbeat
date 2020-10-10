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

print('Fechando conexão')
sock.close()
