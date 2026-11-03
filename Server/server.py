"""
1)create a socket object 
2)give it a host and address           //bind
3)listen for connections(backlogs)     //listen
4)accept the clients                   //accept
5)receive data from the client till it disconnects  //recv
"""
import socket as soc
msg="Message received"
HOST="127.0.0.1"
PORT=5000
with soc.socket(soc.AF_INET,soc.SOCK_STREAM) as s:
  s.bind((HOST,PORT))
  s.listen(1)
  print(f"Server listening on {HOST}:{PORT}")
  while True:
   CONN,ADDR=s.accept()
   with CONN as c:
    print(f"Connected by {ADDR}")
    buffer=""
    while True:
      data=c.recv(2048)
      if not data:
        break
      buffer+=data.decode()
      while "\n" in buffer:
        frame , buffer = buffer.split("\n",1)
        print(frame)
        c.sendall((msg+"\n").encode())
      
