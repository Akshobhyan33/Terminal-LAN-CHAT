import socket as soc
import threading as th

def receivemsg(c,stop_event,b):
    try:
     buffer=b
     while True:
             while not "\n" in buffer:
              data=c.recv(1048)
              if not data:
                print("server closed.")
                stop_event.set()
                return
              buffer+=data.decode()
             frame,buffer=buffer.split("\n",1)
             print("\n"+frame)

    except OSError:
           print("Connection error.")
           stop_event.set()   
           
    
HOST="127.0.0.1"
PORT=5000
with soc.socket(soc.AF_INET,soc.SOCK_STREAM) as c:
    try:
     c.connect((HOST,PORT))

     while True:
      name=input("Enter your name? ")

      if name.strip():
        c.sendall((name+"\n").encode())
        confirmation=""
        while "\n" not in confirmation:
         data=c.recv(1048) 

         if not data:
            print("server closed")
            break  
         confirmation+=data.decode()
        confirmation,buffer=confirmation.split("\n",1)
        if(confirmation=="USERNAME_ACCEPTED"): 
         break
        if(confirmation=="USERNAME_TAKEN"):
           print("Username already exists.")

     stop_event=th.Event()
     t1=th.Thread(target=receivemsg,args=(c,stop_event,buffer))
     t1.start()

     while True:

      if stop_event.is_set():
        break
      
      message=input("What message you want to send: ")

      if message.lower()=="exit":
       break
      
      if message.strip():
          c.sendall((message+"\n").encode())

    except ConnectionResetError:
            print("Server closed.") 

    except ConnectionAbortedError:
               print("Connection aborted.")             