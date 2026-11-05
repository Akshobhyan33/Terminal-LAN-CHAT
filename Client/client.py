import socket as soc

HOST="127.0.0.1"
PORT=5000
with soc.socket(soc.AF_INET,soc.SOCK_STREAM) as c:
    try:
     c.connect((HOST,PORT))
     while True:
      name=input("Enter your name? ")
      if name.strip():
        c.sendall((name+"\n").encode())
        break
    except ConnectionRefusedError:
          print("Server not available.") 
          exit()
    c.settimeout(5)
    buffer=""
    while True:
      try: 
          while not "\n" in buffer:
           data=c.recv(1048)
           if not data:
             exit()
           buffer+=data.decode()
          frame,buffer=buffer.split("\n",1)
          print(frame)
          message=input("What message you want to send: ")
          if message.lower()=="exit":
            break
          if message.strip():
            c.sendall((message+"\n").encode())

      except TimeoutError:
        print("the server didnt respond in 5 seconds")
        break
      except ConnectionResetError:
        print("Server closed.")
        break 
      except ConnectionAbortedError:
        print("Connection aborted.")
        break       
                  