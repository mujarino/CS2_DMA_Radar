import memprocfs
import struct
import time
import pygame
import pygame_gui
import json
import math
import numpy as np
import os
import re

dwEntityList = 0x18AFFB8 # offsets.py
dwLocalPlayerPawn = 0x17252B8 #offsets.py
m_iHealth = 0x14F8  #client.dll.py
m_vOldOrigin = 0x127C #client.dll.py
m_iTeamNum = 0x3CB #client.dll.py
m_angEyeAngles = 0x1578 #client.dll.py
mapNameVal = 0x1CC200 #I don't know where you found it
m_iCompTeammateColor = 0x7300 #client.dll.py
m_bIsDefusing = 0x1408 #client.dll.py

vmm = memprocfs.Vmm(['-device', 'fpga'])


cs2 = vmm.process('cs2.exe')


client = cs2.module('client.dll')
client_base = client.base
print(f"[+] Client_base {client_base}")

entList = struct.unpack("<Q", cs2.memory.read(client_base + dwEntityList, 8, memprocfs.FLAG_NOCACHE))[0]
print(f"[+] Entered entitylist")

def getentitys():
    entitys = []
    for entityId in range(1,2048):
        EntityENTRY = struct.unpack("<Q", cs2.memory.read((entList + 0x8 * (entityId >> 9) + 0x10), 8, memprocfs.FLAG_NOCACHE))[0]
        try:
            entity = struct.unpack("<Q", cs2.memory.read(EntityENTRY + 120 * (entityId & 0x1FF), 8, memprocfs.FLAG_NOCACHE))[0]
            entityHp = struct.unpack("<I", cs2.memory.read(entity + m_iHealth, 4, memprocfs.FLAG_NOCACHE))[0]
            if entityHp>0 and entityHp<=100:
                print(entityHp)
                entitys.append(entity)
            else:
                pass
        except:
            pass
    return(entitys)

print(len(getentitys()))



