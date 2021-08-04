path = "C:\\Users\\luigu\\PycharmProjects\\PythonProjects\\Chat_users"
content = open(path).read().split('\n')
all_items = [x.split(':') for x in content if x]
database = dict(all_items)

import socket
import time
print('Waiting some connection', end="")
time.sleep(0.5)
print('.', end="")
time.sleep(0.5)
print('.', end="")
time.sleep(0.5)
print('.')
HOST = '127.0.0.1'
PORT = 12999
def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    client_s, addr = server_socket.accept()
    confirmation = client_s.recv(1024)
    print('connected by', addr)
    if confirmation.decode() == 'login':
        login_confirmation(client_s)
    if confirmation.decode() == 'register':
        register(client_s)

def login_confirmation(client_socket):
    while True:
        user = client_socket.recv(1024).decode()
        if user in database:
            client_socket.sendall('correct'.encode('utf-8'))
            confirmation = 'correct'
        else:
            confirmation = 'incorrect'
            encode_conf = confirmation.encode('utf-8')
            client_socket.sendall(encode_conf)
            continue
        if confirmation == 'correct':
            while True:
                password = client_socket.recv(1024).decode()
                if password == database[user]:
                    confirmation = 'correct'
                    client_socket.sendall(confirmation.encode('utf-8'))
                    break
                else:
                    confirmation = 'incorrect'
                    client_socket.sendall(confirmation.encode('utf-8'))
                    continue
        break



def register(server_socket):
    name = server_socket.recv(1024).decode()
    password = server_socket.recv(1024).decode()
    open_database_to_read = open('Chat_users', 'r')
    read_database = open_database_to_read.readlines()
    new_user = read_database.append(f'\n{str(name)}:{str(password)}')
    open_database_to_write = open('Chat_users', 'w')
    open_database_to_write.writelines(read_database)
server()

