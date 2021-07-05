import socket
import time
print('Waiting someone a client', end="")
time.sleep(0.5)
print('.', end="")
time.sleep(0.5)
print('.', end="")
time.sleep(0.5)
print('.')
HOST = '127.0.0.1'
PORT = 12999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

conn, addr = s.accept()
print('Connected by', addr)
if_tchau = ''

while True:
    try:
        data = conn.recv(1024)
    except:
        s.close()
        conn.close()
        exit()
    else:
        if not data:
            break
        else:
            print(f'Recieved: \033[1;36m{data.decode()}\033[m')
            if if_tchau == 'Tchau' or if_tchau == 'tchau':
                s.close()
                conn.close()
                exit()
            msg = input('Digite sua mensagem: ')
            if msg == 'tchau' or msg == 'Tchau':
                if_tchau = msg
            if data.decode() != 'tchau' and data.decode() != 'Tchau':
                final_msg = msg.encode('utf-8')
                conn.sendall(final_msg)
                print('\033[1;92mMensagem enviada\033[m')
                continue
            else:
                final_msg = msg.encode('utf-8')
                conn.sendall(final_msg)
                print('\033[1;92mMensagem enviada\033[m')
                s.close()
                conn.close()
                break
