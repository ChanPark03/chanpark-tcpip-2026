#ex1_oneshot_server.py 교재 p21

import socket 
import sys 

def error_handling(message):
    sys.stderr.write(message + '\n')
    sys.exit(1)