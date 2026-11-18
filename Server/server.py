
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
  clients={}
  client_lock=th.Lock()

  def __init__(self,CONN,ADDR,i):
   self.CONN=CONN
   self.ADDR=ADDR
   self.i=i
   
  def naming(self):
        ok=False
        buffer=""
        send=""
        name=""
        data=""
        while "\n" not in buffer:
            data=self.CONN.recv(1048)
            if not data:
             return
            buffer+=data.decode()

        name,buffer=buffer.split("\n",1)
        send+=buffer
        with ClientHandler.client_lock:
            if name not in ClientHandler.clients:
             ClientHandler.clients[name]=self.CONN
             ok=True
            else:
              ok=False
        if ok:
         self.CONN.sendall("USERNAME_ACCEPTED\n".encode())
        else:
         self.CONN.sendall("USERNAME_TAKEN\n".encode())   

        return name,send,ok
  
  def handle(self):
   try:

    with self.CONN as c:
         while True:
          result=self.naming()
          if result is None:
            return
          name,buffer,ok=result
          if ok:
            break
        
         print(f"#{self.i} {name} Connected by {self.ADDR}")

         user=""
         check=False
         while True:
          while "\n" in buffer:
                frame , buffer = buffer.split("\n",1)
                if frame=='#':
                  check=False
                  continue
                elif not check:
                 if '#' in frame:
                   waste,user=frame.split('#',1)
                   if user !="":
                    check=True
                    continue    
                if check:
                   ClientHandler.clients[user].sendall(f"{name}:{frame}\n".encode())
                if not check:
                 user=""
                 with ClientHandler.client_lock:
                  recipients = ClientHandler.clients.copy()
                 
                 for client in recipients:
                  try: 
                   if recipients[client]!=self.CONN:
                     recipients[client].sendall(f"{name}:{frame}\n".encode())

                  except (ConnectionResetError,BrokenPipeError,OSError):
                   with ClientHandler.client_lock:
                   
                    if client in ClientHandler.clients:
                     ClientHandler.clients.pop(client)

                   print("Client disconnected during broadcast.") 

          data=c.recv(2048)
          if not data:
                print(f"#{self.i} {name} :{self.ADDR} disconnected normally.")
                break 
          
          buffer+=data.decode()

   except(ConnectionResetError,ConnectionAbortedError):
         print(f"#{self.i} {name} :{self.ADDR} disconnected abruptly.")
           
   finally:
          with ClientHandler.client_lock:
           if ClientHandler.clients.get(name)==self.CONN: 
            ClientHandler.clients.pop(name)


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
    c=ClientHandler(CONN,ADDR,i)
    t1=th.Thread(target=c.handle)
    t1.start()