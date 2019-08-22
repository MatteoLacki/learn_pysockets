import socket
import select

HEADER_LEN = 10
# IP = "127.0.0.1"
IP = socket.gethostname()
PORT = 0

server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allows to reconnect
server_s.bind((IP, PORT))

print("ip {}\tport {}".format(*server_s.getsockname()))

server_s.listen()

sockets_list = [server_s]
clients = {}


def receive_message(client_s):
    try:
        message_header = client_s.recv(HEADER_LEN)
        if not message_header:
            return False
        message_len = int(message_header.decode("utf-8"))
        return {'header': message_header,
                'data': client_s.recv(message_len)}
    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_s in read_sockets:
        if notified_s == server_s: # someone just connected
            client_s, client_add = server_s.accept()

            user = receive_message(client_s)
            if not user:
                continue

            sockets_list.append(client_s)
            clients[client_s] = user

            print(f"Accepted new connection from {client_add[0]}:{client_add[1]} username:{user['data'].decode('utf-8')}")

        else:
            message = receive_message(client_s)

            if not message:
                print(f"Closed connection from {clients[notified_s]['data'].decode('utf-8')}")
                sockets_list.remove(notified_s)
                del clients[notified_s]
                continue

            user = clients[notified_s]
            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            for client_s in clients:
                if client_s != notified_s:
                    client_s.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_s in exception_sockets:
        sockets_list.remove(notified_s)
        del clients[notified_s]
