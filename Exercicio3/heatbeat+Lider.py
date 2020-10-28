# Gabriel Yudi Sanefugi - 160027
# Wallacy Rychard Sousa Cabral - 155336

import socket
import _thread as thread
import time

PORT = 6000            # Porta que o Servidor esta

ListaLider = {
    1: "26.139.227.213", # Alexander
    2: "26.139.134.240", # Alishow
    3: "26.130.240.169", # Giron
    4: "26.139.134.20", # Ariel
    5: "26.136.12.80", # Breda
    6: "26.139.134.120", # Christian
    7: "26.139.134.100", # David
    8: "26.186.90.172", # David
    9: "26.139.134.60", # Eduardo
    10: "26.139.135.64", # Galhardo
    11: "26.139.134.160", # Belchior
    12: "26.130.240.69", # Yudi
    13: "26.159.190.84", # Guilherme
    14: "26.135.202.138", # Juliano
    15: "26.139.135.24", # Leonardo
    16: "26.133.240.81", # Lorene
    17: "26.135.201.234", # Lucas Fonseca
    18: "26.130.240.89", # Lucas Passos
    19: "26.145.208.62", # Marcio
    20: "26.135.202.98", # Rafael Santana
    21: "26.130.245.89", # Rafael Santos
    22: "26.135.201.194", # Renan
    23: "26.130.241.233", # Vanessa
    24: "26.135.201.174", # Vinicius
    25: "26.135.204.126", # Vitor
    26: "26.158.231.204", # Wallacy
    27: "26.150.255.169", # Kortez
    28: "26.135.202.178", # Kortez
    29: "26.155.216.74", # Menassa
    30: "26.139.135.144", # Rafael Ritter
    31: "26.139.135.144" # Wallacy 
}

#-------------------------------------------------------------------------------------------------

# Define o novo Lider
def newLider(lista):
    # Novo lider sera escolhido pelo menor numero inteiro, no caso da ListaLider

    for i in ListaLider: # O primeira IP encontrada, será o lider, pois a esta ordenado de forma crescente
        for j in lista:
            if ListaLider[i] == j:
                return i # Retorna seu index do dicionario

# A ListaLider é atualizado na Lista_Ativo
def atualizaLista():
    
    listaAux = []
    for i in ListaLider.values():
        listaAux.append(i)

    return listaAux

# Funcao de escuta
def escuta():
    # Cria o Socket (Receptor)
    #tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configurações do servidor
    #orig = ('', PORT)
    #tcp.bind(orig)
    #tcp.listen(1)

    while True:
        con, cliente = tcp.accept()
        if(ADD_LISTA):
            LISTA_RESPOSTA.append(cliente[0]) # Colocana na lista o IP
        thread.start_new_thread(conectado, (con, cliente))     

    tcp.close()

# Quando capturado algo na escuta, é finalizado sua conexao
def conectado(con, cliente):

    print('Server: Conectado por '+ str(cliente))

    while True:
        msg = con.recv(1024)
        if not msg: break
        print ('Server: '+str(cliente) +" envior: "+ str(msg))

    print('Server: Finalizando conexao do cliente do: '+ str(cliente))
    con.close()
    thread.exit()

# Funcao de enviar
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
    orig = ('', PORT)
    tcp.bind(orig)
    tcp.listen(1)
    ADD_LISTA = False

    thread.start_new_thread(escuta,()) # Thread de escuta

    LISTA_ATIVA  = atualizaLista() # Essa lista contem todas as maquinas
    LISTA_FALHA = [] # Essa lista são os que falharam
    Lider_atual = 1 # Index do primeiro lider

    time.sleep(5)
    
    while True:
        print("Server: Enviando...")
        # ENVIANDO MENSAGENS
        ADD_LISTA = True
        LISTA_RESPOSTA = []
        for ip in LISTA_ATIVA.copy():
            thread.start_new_thread(enviar,(ip,6000)) # Envia

        print("\n----------------------------------------------------\n")
        # ESPERA POR RESPOSTA
        print("Server: Esperando conexão...")
        time.sleep(10) #Quanto tempo para responde?
        ADD_LISTA = False

        print("\n----------------------------------------------------\n")
        # ATUALIZAR LISTA
        print("Server: Lista sendo atualizada...")
        LISTA_TMP = LISTA_ATIVA.copy() # Obs.: essa lista_tmp pode ter ip repitido
        for i in LISTA_TMP:
            if not i in LISTA_RESPOSTA: # se não esta na lista e nem as que falho
                LISTA_FALHA.append(i) # Coloca na lista que falho
                LISTA_ATIVA.remove(i) # Remove da lista ativa

        del LISTA_TMP # Apenas otimização

        print("Lista falha: " + str(LISTA_FALHA))
        print("Lista ativa: " + str(LISTA_ATIVA))

        if len(LISTA_ATIVA) <= 0:
            break  # Se não houver nenhum ativo, fecha o programa

        print("\n----------------------------------------------------\n")
        # DEFINIR LIDER
        Lider_atual = newLider(LISTA_ATIVA)
        print("Server: O lider atual é " + str(ListaLider[Lider_atual])+ " | index: "+ str(Lider_atual))

        time.sleep(30) # Quando manda outro heatbeat?
        print("\n****************************************************\n")

    tcp.close()

    print("*** FIM ***")
