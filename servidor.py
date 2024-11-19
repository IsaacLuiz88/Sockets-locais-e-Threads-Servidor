import socket
import threading
import time

# Configurações do servidor
HOST = '127.0.0.1'
PORT = 65432
TIMEOUT = 30

# Lista para gerenciar conexões ativas
active_clients = []
server_running = True

def handle_client(client_socket, client_address):
    global server_running
    try:
        client_id = client_socket.recv(1024).decode('utf-8')
        print(f"Cliente conectado: {client_id} ({client_address})")
        
        while server_running:
            try:
                # Tenta receber mensagens do cliente
                message = client_socket.recv(1024).decode('utf-8')
                if not message:  # Se a mensagem for vazia, desconecta
                    print(f"Cliente desconectado: {client_id}")
                    break
                print(f"Mensagem de {client_id}: {message}")
            except ConnectionResetError:
                print(f"Conexão com o cliente {client_id} foi encerrada abruptamente.")
                break
    finally:
        # Remove o cliente da lista e fecha o socket
        active_clients.remove(client_socket)
        client_socket.close()

def start_server():
    global server_running
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.settimeout(TIMEOUT)  # Define o timeout do servidor
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Servidor aguardando conexões em {HOST}:{PORT}...")

    try:
        while server_running:
            try:
                client_socket, client_address = server.accept()
                active_clients.append(client_socket)
                # Cria uma thread para gerenciar cada cliente
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                client_thread.start()
            except socket.timeout:
                print(f"Tempo limite de {TIMEOUT} segundos atingido. Encerrando o servidor...")
                server_running = False
    finally:
        # Fecha todas as conexões ativas e notifica os clientes
        for client_socket in active_clients:
            try:
                client_socket.sendall("Servidor encerrando...".encode('utf-8'))
            except:
                pass
            client_socket.close()
        
        server.close()
        print("Servidor encerrado.")

if __name__ == "__main__":
    start_server()
