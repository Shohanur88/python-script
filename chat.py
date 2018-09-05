'''Simple Local Server ChatApp
   Aurthor: Md.Shohanur Rahman
'''

import socket
import threading

CLOSE = b'--close--'

class App(socket.socket,threading.Thread):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.port = 8000;

    def host(self):
        self.sock.bind(('',self.port))
        self.sock.listen(1)
        self.hostname = socket.gethostbyname(socket.gethostname())
        print('Server started at host: '+self.hostname+' on port: ' + str(self.port))
        self.client_sock,addr = self.sock.accept()
        print('\nConnection established. Press enter to send message. ')
        print('Press Ctrl+C to end conversation \n')
    
    def server_send(self):
        while True:
            try:	
                reply = input('I say: ')
                self.client_sock.send(reply.encode())
            except keyboardInterrupt:
                self.client_sock.send(CLOSE)
                self.client_sock.close()
                self.sock.close()
                break

    def server_receive(self):
        while True:
            message = self.client_sock.recv(4096)
            print('\nFriend said: ',message.decode())
            if message == CLOSE:
                self.client_sock.close()
                self.sock.close()
                break

    def server_thread(self):
        receive_thread = threading.Thread(target=self.server_receive,name='receive_thread')
        send_thread = threading.Thread(target=self.server_send,name='send_thread')
        receive_thread.start()
        send_thread.start()
        receive_thread.join()
        send_thread.join()
    
    def join(self,hostname):
        self.sock.connect((hostname,self.port))
        print('\nConnection established. Type and press enter to send message')
        print('Press Cntrl+C to end conversation\n')

    def client_send(self):
        while True:
            try:
                message = input('\nI say: ')
                self.sock.send(message.encode())
            except KeyboardInterrupt:
                self.sock.send(CLOSE)
                break

    def client_receive(self):
        while True:
            reply = self.sock.recv(4096)
            print('\nFriend said: ',reply.decode())
            if reply == CLOSE:
                self.sock.close()
                break

    def client_thread(self):
        receive_thread = threading.Thread(target=self.client_receive,name='receive_thread')
        send_thread = threading.Thread(target=self.client_send,name='send_thread')
        receive_thread.start()
        send_thread.start()
        receive_thread.join()
        send_thread.join()

if __name__=="__main__":
    chatroom = App()
    choice = input('1. Host\n2. Join\nYour choice: ')
    if choice[0] in '1Hh':
        chatroom.host()
        chatroom.server_thread()
    else:
        hostname = input('Enter host IP or hostname: ')
        chatroom.join(hostname)
        chatroom.client_thread()
