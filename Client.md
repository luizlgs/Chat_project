import socket

HOST = '127.0.0.1'
PORT = 12999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conectado = s.connect((HOST, PORT))
exit_farewell = 0
if_tchau = ''
while True:
    if conectado:
        break
    if if_tchau == 'Tchau' or if_tchau == 'tchau':
        s.close()
        exit()
    msg = input('Digite sua mensagem: ')
    if msg == 'tchau' or msg == 'Tchau':
        if_tchau = msg
    final_msg = msg.encode('utf-8')
    s.sendall(final_msg)
    print('\033[1;92mMensagem enviada\033[m')
    if exit_farewell >= 1:
        s.close()
        exit()
    try:
        data = s.recv(1024)
        print(f'Recieved: \033[1;36m{data.decode()}\033[m')
    except:
        s.close()
        exit()
        continue
    else:
        if data.decode() == 'Tchau' or data.decode() == 'tchau':
            exit_farewell += 1
