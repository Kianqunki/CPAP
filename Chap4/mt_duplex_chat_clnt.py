#!/usr/bin/env python

from socket import *
from threading import Thread


class ChatClient():
    def __init__(self, bufsiz):
        self.HOST = raw_input('Enter host: ')
        if not self.HOST:
            self.HOST = 'localhost'
        self.PORT = raw_input('Enter port: ')
        if not self.PORT:
            self.PORT = 33000
        else:
            self.PORT = int(self.PORT)

        self.BUFSIZ = bufsiz
        self.hostAddr = (self.HOST, self.PORT)

        self.chatCliSock = socket(AF_INET, SOCK_STREAM)
        self.msg = ""
        self.your_msg = ""
        self.connected = False
        self.recv_thread = Thread(target=self.get_msg)
        self.raw_input_thread = Thread(target=self.get_your_msg)

    def get_msg(self):
        while 1:
            self.msg = self.chatCliSock.recv(self.BUFSIZ)
            if self.msg == 'quit()':
                print "\t\tServer left the chat."
                self.connected = False
                break
            print "\t\tServer:", self.msg
            print "-|"

    def get_your_msg(self):
        while self.connected:
            while self.your_msg == "":
                self.your_msg = raw_input("-|\n")

            self.chatCliSock.send(self.your_msg)
            if self.your_msg == 'quit()':
                self.connected = False
                break
            self.your_msg = ""

    def run(self):
        self.chatCliSock.connect(self.hostAddr)
        self.connected = True
        self.recv_thread.start()

        self.raw_input_thread.start()

        self.recv_thread.join()
        self.raw_input_thread.join()

        self.chatCliSock.close()

if __name__ == '__main__':
    chatClient = ChatClient(1024)
    chatClient.run()
