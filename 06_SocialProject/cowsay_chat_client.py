import argparse
import cmd
import os
import threading
import socket
import readline
import time


class CowsayClient(cmd.Cmd):
    prompt = 'I`m >> '

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.buffer = ''
        self.flag = 0

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        os.system('clear')
        print('You connected to Cowsay chat')
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.recv_messages)
        self.thread.start()

    def close(self):
        self.sock.close()
        self.stop_event.set()
        self.thread.join()

    def send_data(self, data):
        self.sock.send(data.encode())
        time.sleep(0.2)

    def do_yield(self, arg):
        """
        Send message to all users of chat

        message: message you want to send

        yield message
        """

        self.flag = 2
        self.send_data('yield ' + arg + '\n')
        self.flag = 0

    def do_say(self, arg):
        """
        Send message to user with name [cow]

        cow: name of chat user
        message: message you want to send

        say cow message
        """

        self.flag = 2
        self.send_data('say ' + arg + '\n')
        self.flag = 0

    def complete_say(self, prefix, line, begidx, endidx):
        self.flag = 1
        self.send_data('who\n')

        while True:
            if not self.buffer:
                continue

            lst = self.buffer.split()[3:]
            if len(lst) == 1:
                variants = [elem for elem in lst]
            else:
                variants = [elem[0:-1] for elem in lst[0:-1]] + [lst[-1]]
            break

        self.flag = 0
        self.buffer = ''
        return [cow for cow in variants if cow.startswith(prefix)]

    def do_login(self, arg):
        """
        Register in chat under name [cow]

        cow: name, under which you want to register

        login cow
        """

        self.flag = 2
        self.send_data('login ' + arg + '\n')
        self.flag = 0

    def complete_login(self, prefix, line, begidx, endidx):
        self.flag = 1
        self.send_data('cows\n')

        while True:
            if not self.buffer:
                continue

            lst = self.buffer.split()[2:]
            if len(lst) == 1:
                variants = [elem for elem in lst]
            else:
                variants = [elem[0:-1] for elem in lst[0:-1]] + [lst[-1]]
            break

        self.flag = 0
        self.buffer = ''
        return [cow for cow in variants if cow.startswith(prefix)]

    def do_cows(self, arg):
        """
        Show available cows names

        cows
        """

        self.flag = 2
        self.send_data('cows ' + arg + '\n')
        self.flag = 0

    def do_who(self, arg):
        """
        Show registered users

        who
        """
        self.flag = 2
        self.send_data('who ' + arg + '\n')
        self.flag = 0

    def do_quit(self, arg):
        """
        Quit from Cowsay chat

        quit
        """

        self.flag = 2
        self.send_data('quit ' + arg + '\n')
        self.flag = 0
        if not arg:
            self.close()
            return True

    def emptyline(self):
        return

    def recv_messages(self):
        while not self.stop_event.is_set():
            if self.sock.fileno() != -1:
                message = self.sock.recv(4096)
                if message:
                    if self.flag == 1:
                        self.buffer = message.decode().strip()
                    elif self.flag == 2:
                        print("\033[A                             \033[A")
                        print('\n' + message.decode().strip() + '\n')
                        if readline.get_line_buffer():
                            print(f"{self.prompt}{readline.get_line_buffer()}", end="", flush=True)
                    else:
                        print("\033[A                             \033[A")
                        print('\n' + message.decode().strip() + '\n')
                        print(f"{self.prompt}{readline.get_line_buffer()}", end="", flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host', type=str)
    parser.add_argument('port', type=int)
    args = parser.parse_args()

    cmdline = CowsayClient(args.host, args.port)
    cmdline.cmdloop()
