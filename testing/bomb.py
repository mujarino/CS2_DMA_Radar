import pymem
import struct
import time
import pygame
import pygame_gui
import json
import math
import numpy as np
import os
import re
from requests import get

#######################################

offsets = get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/offsets.json').json()
clientdll = get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/client_dll.json').json()

#######################################

dwGlobalVars = offsets['client.dll']['dwGlobalVars']


print('[+] offsets parsed')


pm = pymem.Pymem("cs2.exe")
client_base = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

print(f"[+] Client_base {client_base}")


dwGlobalVarsvar = pm.read_longlong(client_base + dwGlobalVars)
for i in range(4096):
	try:
		dwGlobalVarsvaradress = pm.read_longlong(dwGlobalVarsvar + i)
		mapname1 = pm.read_string(dwGlobalVarsvaradress)
		if mapname1 == 'de_mirage':
			print(i)
		print(mapname1)
	except Exception as e:
		pass
