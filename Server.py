import threading

path = "C:\\Users\\luigu\\PycharmProjects\\PythonProjects\\Chat_users"
content = open(path).read().split('\n')
all_items = [x.split(':') for x in content if x]
database = dict(all_items)
online_users = {}
online_users_name = []
online_users_addr = {}
online_users_inbox = {}
online_users_addr_to_name = {}

import time
from time import sleep
import socket
print('Waiting some connection')
HOST = '127.0.0.1'
PORT = 12999
def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    def handle_client(client_s, addr):
        print('connected by', addr)
        try:
            confirmation = client_s.recv(1024)
        except:
            print(f'O cliente "{addr}" vazou!')
            return
        if confirmation.decode() == 'login':
            login_confirmation(client_s)
        if confirmation.decode() == 'register':
            register(client_s)
        inbox(client_s)

    while True:
        client_s, addr = server_socket.accept()
        individual_client = threading.Thread(target=handle_client, args=(client_s, addr))
        individual_client.start()

def login_confirmation(client_socket):
    while True:
        try:
            user = client_socket.recv(1024).decode()
        except:
            break
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
                try:
                    password = client_socket.recv(1024).decode()
                except:
                    break
                if password == database[user]:
                    confirmation = 'correct'
                    client_socket.sendall(confirmation.encode('utf-8'))
                    if user not in online_users:
                        online_users[user] = password
                        online_users_name.append(user)
                        online_users_addr[user] = client_socket
                        online_users_inbox[user] = []
                        online_users_addr_to_name[client_socket] = user
                    break
                else:
                    confirmation = 'incorrect'
                    client_socket.sendall(confirmation.encode('utf-8'))
                    continue
        break


def register(client_socket):
    while True:
        name = client_socket.recv(1024).decode()
        if name not in database:
            client_socket.sendall('ok'.encode('utf-8'))
            password = client_socket.recv(1024).decode()
            open_database_to_read = open('Chat_users', 'r')
            read_database = open_database_to_read.readlines()
            new_user = read_database.append(f'\n{str(name)}:{str(password)}')
            open_database_to_write = open('Chat_users', 'w')
            open_database_to_write.writelines(read_database)
            database[name] = password
            online_users[name] = password
            online_users_name.append(name)
            online_users_addr[name] = client_socket
            online_users_inbox[name] = []
            online_users_addr_to_name[client_socket] = name

            break
        else:
            client_socket.sendall('change_this_name'.encode('utf-8'))
            continue

def inbox(client_socket):
    saved_name = ''
    while True:
        try:
            confirmation = client_socket.recv(1024).decode()
        except:
            continue
        if confirmation == 'inbox':
            if len(saved_name) == 0:
                client_socket.sendall('give_me_the_name'.encode('utf-8'))
                while True:
                    name = client_socket.recv(1024).decode()
                    if name in online_users_name:
                        saved_name = name
                        client_socket.sendall('valid_name'.encode('utf-8'))
                        break
                    else:
                        client_socket.sendall('invalid_name'.encode('utf-8'))
                        continue
            else:
                client_socket.sendall('ok'.encode('utf-8'))
                name = saved_name
            whole_inbox = '\n'
            number_of_messages = len(online_users_inbox[name])
            for messages in online_users_inbox[name]:
                whole_inbox += f'{messages}\n'
            client_socket.sendall(whole_inbox.encode('utf-8'))
            continue

        if confirmation == 'send':
            while True:
                receiver_name = client_socket.recv(1024).decode()
                if receiver_name in online_users_name:
                    confirmation = client_socket.sendall('valid_name'.encode('utf-8'))
                else:
                    confirmation = client_socket.sendall('invalid_name'.encode('utf-8'))
                    continue
                message = client_socket.recv(1024).decode()
                online_users_inbox[receiver_name].append((f'From {online_users_addr_to_name[client_socket]}: {message}'))
                break

server()
