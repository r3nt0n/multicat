#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/multicat
# multicat - multithread reverse shell listener

import socket, threading, time, argparse, os

name = 'multicat'
desc = 'Multithread reverse shell listener'
__version__ = '0.1.1'
__author__ = 'r3nt0n'
__status__ = 'Development'

def process_args():
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-p', '--port', action="store", metavar='', type=int, dest='port',
                        help='port to listen (default: 28000)', default=28000)
    parser.add_argument('-m', '--max-clients', action="store", metavar='', type=int, dest='max_clients',
                        default=5, help='max number of new clients to queue before establish connection (default: 5)')
    parser.add_argument('-t', '--timeout', action="store", metavar='', type=int, dest='timeout',
                        default=10, help='connections timeout (default: 10)')
    args = parser.parse_args()
    return args.port, args.max_clients, args.timeout

class color:
    PURPLE = u'\033[95m'
    CYAN = u'\033[96m'
    DARKCYAN = u'\033[36m'
    BLUE = u'\033[94m'
    GREEN = u'\033[92m'
    YELLOW = u'\033[93m'
    RED = u'\033[91m'
    BOLD = u'\033[1m'
    UNDERLINE = u'\033[4m'
    ORANGE = u'\033[33m'
    GREY = u'\033[90m'
    END = u'\033[0m'


class ThreadedServer(object):
    def __init__(self, host, port, max_clients=5, timeout=10):
        self.host = host
        self.port = port
        self.max_clients = max_clients
        self.timeout = timeout
        self.clients = []
        self.current_session = ''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        super().__init__()

    def listen(self):
        self.sock.listen(self.max_clients)
        print(f'{color.GREEN}[+]{color.END} Listening on port {color.GREEN}{color.BOLD}{self.port}{color.END}...\n')
        while True:
            client, address = self.sock.accept()
            client.settimeout(self.timeout)
            print(f'\n\n{color.GREEN}[+]{color.END} New client connected: %s:%d' % client.getpeername())
            self.clients.append((client, address))

    def listenToClient(self, client_object):
        client = client_object[0]
        address = client_object[1]
        print(f'\n{color.GREEN}[*]{color.END} Connected to %s:%d' % client.getpeername())
        buff_size = 1024
        while True:
            try:
                recv_len = 1
                output = b''
                while recv_len:
                    data = client.recv(buff_size)
                    recv_len = len(data)
                    output += data
                    if recv_len < buff_size:
                        break
                try:
                    print(output.decode('utf-8'), end='')
                except UnicodeDecodeError:
                    print(output.decode('latin-1'), end='')

                command = input('')
                if command.upper() in ('HELP', '?'):
                    print(f'\n{color.BOLD}COMMAND\t\tDESCRIPTION{color.END}')
                    print(f'------------------------------------')
                    print('STOP\t\tStop interacting with the current session')
                    print('CLOSE \t\tClose the current connection')
                    command = ''
                if command.upper() == 'STOP':
                    if input(f'\n{color.ORANGE}[?]{color.END} Do you want to {color.ORANGE}stop{color.END} this session? [y/N] ').lower() == 'y':
                        print()
                        self.current_session = ''
                        client.sendall('\n'.encode())
                        break
                if command.upper() == 'CLOSE':
                    if input(f'\n{color.RED}[?]{color.END} Do you want to {color.RED}close{color.END} this connection? [y/N] ').lower() == 'y':
                        # client.sendall(command.encode())
                        client.close()
                        del self.clients[self.current_session]
                        self.current_session = ''
                        break
                    else:
                        command = ''

                client.sendall((command + '\n').encode())

                time.sleep(0.1)

            except (socket.timeout, BrokenPipeError):
                print(f'{color.RED}[?]{color.END} Client %s:%d disconnected' % address)
                client.close()
                del self.clients[self.current_session]
                self.current_session = ''
                break

            finally:
                if self.current_session == '':
                    self.menu()

    def create_client_thread(self, client):
        threading.Thread(target=self.listenToClient, args=(client,)).start()

    def menu(self):
        print(f'Type help or ? to list commands.\n')
        new_session = self.current_session
        while True:
            while new_session == '':
                user_input = input(f'{color.BLUE}[{len(self.clients)}]{color.END} > ')
                if user_input.upper() in ('HELP', '?'):
                    print(f'\n{color.BOLD}COMMAND\t\tDESCRIPTION{color.END}')
                    print(f'------------------------------------')
                    print('HELP\t\tList available commands')
                    print('SESSIONS\tList established sessions')
                    print('START <id>\tInteract with a client')
                    print('CLOSE <id>\tClose an specific connection')
                    print('EXIT / QUIT\tExit the entire application')
                    print()

                elif user_input.upper() in ('EXIT', 'QUIT'):
                    os._exit(0)

                elif user_input.upper().startswith('SESSIONS'):
                    print(f'\n{color.BOLD}ID\tRemote address\tRemote port{color.END}')
                    print(f'------------------------------------')
                    for client in self.clients:
                        print(f'{self.clients.index(client)}\t{client[1][0]}\t{client[1][1]}')
                    print()
                if not (user_input.upper().startswith('START') or user_input.upper().startswith('CLOSE')):
                    continue
                else:
                    new_session = user_input.split()[-1]
            try:
                new_session = int(new_session)
                if new_session+1 > len(self.clients):
                    raise TypeError()
            except (TypeError, IndexError, ValueError):
                print(f'{color.RED}[!]{color.END} ERROR: You have entered a non-valid session ID')
                new_session = ''
                continue
            if new_session != self.current_session:
                if user_input.upper().startswith('START'):
                    self.create_client_thread(self.clients[new_session])
                    self.current_session = new_session
                    break
                elif user_input.upper().startswith('CLOSE'):
                    self.clients[new_session][0].close()
                    del self.clients[new_session]
                    print(f'\n{color.ORANGE}[!]{color.END} Connection {new_session} closed\n')
                    self.current_session = ''
                    new_session = ''
        return

    def run(self):
        threads = []
        threads.append(threading.Thread(target=self.listen, args=()))
        if self.current_session == '':
            threads.append(threading.Thread(target=self.menu))
        for thread in threads:
            thread.start()
        return


def main():
    print(f'\n{name} by r3nt0n - https://github.com/r3nt0n/multicat\n')
    port, max_clients, timeout = process_args()
    ThreadedServer('', port, max_clients, timeout).run()


if __name__ == "__main__":
    main()



