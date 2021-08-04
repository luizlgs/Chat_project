import socket

HOST = '127.0.0.1'
PORT = 12999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conectado = s.connect((HOST, PORT))
exit_farewell = 0

def send_message():
    message = input('Digite sua mensagem: ')
    encode_message = message.encode('utf-8')
    s.sendall(encode_message)

def receive_message():
    received = s.recv(1024)
    return received

def login():
    while True:
        name = input('Digite seu nome: ')
        s.sendall(name.encode('utf-8'))
        answer = s.recv(1024)
        if answer.decode() == 'incorrect':
            print('Nome inválido')
        else:
            while True:
                password = input('Digite sua senha: ')
                s.sendall(password.encode('utf-8'))
                answer = s.recv(1024)
                if answer.decode() == 'incorrect':
                    print('Senha incorreta')
                    continue
                if answer.decode() == 'correct':
                    print('senha correta')
                    s.close()
                    break
            break

def register():
    while True:
        name = input('Digite seu nome: ')
        s.sendall(name.encode('utf-8'))
        password = input('Digite sua senha: ')
        s.sendall(password.encode('utf-8'))
        print('Conta criada!')
        break

while True:
    option = input('Login(l), register(r): ')
    if option == 'l':
        s.sendall('login'.encode('utf-8'))
        login()

    if option == 'r':
        s.sendall('register'.encode('utf-8'))
        register()
    break
