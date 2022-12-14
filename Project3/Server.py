'''
Script for server
@author: hao
'''

import config
import protocol
import os
from socket import *
class server:

    # Constructor: load the server information from config file
    def __init__(self):
        self.port, self.path=config.config().readServerConfig()
        #print(f"{self.path}")

    # Get the file names from shared directory
    def getFileList(self):
        return os.listdir(self.path)
    
    # Function to send file list to client       
    def listFile(self, serverSocket):
        serverSocket.send(protocol.prepareFileList(protocol.HEAD_LIST, self.getFileList()))

    # Function to send a file to client       
    def sendFile(self,serverSocket,fileName):
        f = open(fileName,'rb')
        l = f.read(1024) # each time we only send 1024 bytes of data
        while (l):
            serverSocket.send(l)
            l = f.read(1024)
        print(fileName+" has been sent to client!")

    #JT Function to recive file from client
    def receiveFile(self,serverSocket,fileName):
        with open(fileName, 'wb') as f:
            while True:
                #print('receiving data...')
                data = serverSocket.recv(1024)
                #print('data=%s', (data))
                if not data:
                     break
            # write data to a file
                f.write(data)
        print(fileName+" has been uploaded!")
        


    # Main function of server, start the file sharing service
    #JT - Added section to upload file to server.
    def start(self):
        serverPort=self.port
        serverSocket=socket(AF_INET,SOCK_STREAM)
        serverSocket.bind(('',serverPort))
        serverSocket.listen(20)
        print('The server is ready to receive')
        while True:
            connectionSocket, addr = serverSocket.accept()
            dataRec = connectionSocket.recv(1024)
            header,msg=protocol.decodeMsg(dataRec.decode()) # get client's info, parse it to header and content
            # Main logic of the program, send different content to client according to client's requests
            if(header==protocol.HEAD_REQUEST):
                self.listFile(connectionSocket)
            elif(header==protocol.HEAD_DOWNLOAD):
                self.sendFile(connectionSocket, self.path+"/"+msg)
            elif(header==protocol.HEAD_UPLOAD):
                self.receiveFile(connectionSocket, self.path+"/"+msg)
            else:
                connectionSocket.send(protocol.prepareMsg(protocol.HEAD_ERROR, "Invalid Message"))
            connectionSocket.close()

def main():
    s=server()
    s.start()

main()
