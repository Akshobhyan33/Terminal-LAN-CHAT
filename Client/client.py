import socket as soc

HOST="127.0.0.1"
PORT=5000
with soc.socket(soc.AF_INET,soc.SOCK_STREAM) as c:
    c.connect((HOST,PORT))
    c.settimeout(5)
    while True:
     message=input("What message you wanna send: ")
     if(message.lower()=="exit"):
        break
     if message.strip():
       c.sendall((message+"\n").encode())
       try:
         data = c.recv(1024)
         print(data.decode())
       except TimeoutError:
         print("the server didnt respond in 5 seconds") 

