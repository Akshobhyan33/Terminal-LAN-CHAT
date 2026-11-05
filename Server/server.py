"""
1)create a socket object 
2)give it a host and address           //bind
3)listen for connections(backlogs)     //listen
4)accept the clients                   //accept
5)receive data from the client till it disconnects  //recv
6)send data so that client knows it is connected to the server
7)implemented message framing since TCP is byte based.
"""
import socket as soc
import threading as th

class ClientHandler:
  def __init__(self,CONN,ADDR,i,msg):
   self.CONN=CONN
   self.ADDR=ADDR
   self.i=i
   self.msg=msg

  def handle(self):
    with self.CONN as c:
        buffer=""
        while not "\n" in buffer:
         data=c.recv(1048)
         if not data:
           return
         buffer+=data.decode()
        name,buffer=buffer.split("\n",1)
        c.sendall("The name is received\n".encode())
        
        print(f"#{self.i} {name} Connected by {self.ADDR}")
          
        while True:
          while "\n" in buffer:
                frame , buffer = buffer.split("\n",1)
                print(f"{name}:{frame}")
                c.sendall((self.msg+"\n").encode())
          try:
            data=c.recv(2048)

          except (ConnectionResetError,ConnectionAbortedError):
           print(f"#{self.i} {name} :{self.ADDR} disconnected abruptly.")
           break

          if not data:
            print(f"#{self.i} {name} :{self.ADDR} disconnected normally.")
            break

          buffer+=data.decode()

          
  
msg="Message received"
HOST="127.0.0.1"
PORT=5000
with soc.socket(soc.AF_INET,soc.SOCK_STREAM) as s:
  s.bind((HOST,PORT))
  s.listen(20)
  print(f"Server listening on {HOST}:{PORT}")
  i=0
  while True:
    CONN,ADDR=s.accept()
    i+=1
    c=ClientHandler(CONN,ADDR,i,msg)
    t1=th.Thread(target=c.handle)
    t1.start()