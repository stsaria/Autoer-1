import sys
import socket
from threading import Thread

def received_from(connection):
    buffer = b''
    connection.settimeout(2)
    try:
        recv_len = 1
        while recv_len:
            data = connection.recv(4096)
            buffer += data
            recv_len = len(data)
            if recv_len < 4096:
                break
    except:
        pass
    return buffer

def hexdump(src, length=16):
    result = []
    for i in range(0, len(src), length):
        s = src[i:i+length]
        hexa = ' '.join(['{:02X}'.format(x) for x in s])
        text = ''.join([chr(x) if x >= 32 and x < 127 else '.' for x in s])
        result.append('{:04X}   {}{}    {}'.format(i, hexa, ((length-len(s))*3)*' ', text))
    for s in result:
        print(s)

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    if receive_first:
        remote_buffer = received_from(remote_socket)
        hexdump(remote_buffer)
        if len(remote_buffer):
            print('ログ：localhostに {}バイト を送信しています'.format(len(remote_buffer)))
            client_socket.send(remote_buffer)
    while True:
        local_buffer = received_from(client_socket)
        if len(local_buffer):
            print('ログ：localhostから {}バイト を受信しました'.format(len(local_buffer)))
            hexdump(local_buffer)
            remote_socket.send(local_buffer)
            print('ログ：リモートに送信されます')
        remote_buffer = received_from(remote_socket)
        if len(remote_buffer):
            print('[<==] Received {} bytes from remote.'.format(len(remote_buffer)))
            hexdump(remote_buffer)
            client_socket.send(remote_buffer)
            print('ログ：localhostに送信されます')

def server_loop(local_host, local_port, remote_host, remote_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except:
        print("接続できません")
        return 0;
    print('{}:{}が受信しています'.format(local_host, local_port))
    server.listen(5)
    while True:
        client_socket, addr = server.accept()
        proxy_thread = Thread(target=proxy_handler,
                        args=[client_socket,remote_host, remote_port, False])
        proxy_thread.start()