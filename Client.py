import socket
import threading

HOST = '127.0.0.1'
PORT = 12999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conectado = s.connect((HOST, PORT))

def login():
    while True:
        name = input('Digite seu nome: ')
        s.sendall(name.encode('utf-8'))
        answer = s.recv(1024)
        if answer.decode() == 'incorrect':
            print('\033[1;31mNome inválido\033[m')
        else:
            while True:
                password = input('Digite sua senha: ')
                s.sendall(password.encode('utf-8'))
                answer = s.recv(1024)
                if answer.decode() == 'incorrect':
                    print('\033[1;31mSenha incorreta\033[m')
                    continue
                if answer.decode() == 'correct':
                    break
            break

def register():
    while True:
        name = input('Digite o seu nome: ')
        your_name = name
        s.sendall(name.encode('utf-8'))
        answer = s.recv(1024).decode()
        if answer == 'ok':
            password = input('Crie uma senha: ')
            s.sendall(password.encode('utf-8'))
            break
        if answer == 'change_this_name':
            print('Este nome já está sendo usado')
            continue

def menu():
    print('Enviar mensagens(s)\n'
          'Ver inbox (c)')
    while True:
        option = input('Sua opção: ')

        if option == 'c':
            s.sendall('inbox'.encode('utf-8'))
            confirmation = s.recv(1024).decode()
            if confirmation == 'give_me_the_name':
                while True:
                    name = input('Digite o seu nome: ')
                    s.sendall(name.encode('utf-8'))
                    confirmation = s.recv(1024).decode()
                    if confirmation == 'valid_name':
                        break
                    if confirmation == 'invalid_name':
                        print('Nome inválido')
                        continue
            if confirmation == 'ok':
                pass
            inbox = s.recv(1024).decode()
            if len(inbox) > 1:
                print('Suas mensagens:', inbox)
            else:
                print('Não há mensagens')

        if option == 's':
            s.sendall('send'.encode('utf-8'))
            while True:
                friend_name = input('Nome da pessoa que deseja enviar a mensagem: ')
                s.sendall(friend_name.encode('utf-8'))
                confirmation = s.recv(1024).decode()
                if confirmation == 'valid_name':
                    pass
                if confirmation == 'invalid_name':
                    print('Este usuário esta offline ou não existe')
                    continue
                message = input('Digite a sua mensagem: ')
                s.sendall(message.encode('utf-8'))
                print('\033[1;32mMensagem enviada!\033[m')
                break

while True:
    option = input('Login(l), register(r): ')
    if option == 'l':
        s.sendall('login'.encode('utf-8'))
        login()
        print('\033[1;32mLogin realizado com sucesso!\033[m\n')

    if option == 'r':
        s.sendall('register'.encode('utf-8'))
        register()
        print('\033[1;32mRegistro realizado com sucesso!\033[m\n')

    if option != 'l' and option != 'r':
        print('Opção inválida')
        continue
    menu()
    break
