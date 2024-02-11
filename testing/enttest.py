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

dwEntityList = 0x18B0FC8 # offsets.py
dwLocalPlayerPawn = 0x17262E8 #offsets.py
m_iPawnHealth = 0x7F0
m_iPawnArmor = 0x7F4
m_bPawnIsAlive = 0x7EC
m_angEyeAngles = 0x1578
m_iTeamNum = 0x3CB
m_hPlayerPawn = 0x7E4
m_vOldOrigin = 0x127C

vmm = memprocfs.Vmm(['-device', 'fpga'])


cs2 = vmm.process('cs2.exe')


client = cs2.module('client.dll')
client_base = client.base
print(f"[+] Client_base {client_base}")

EntityList = struct.unpack("<Q", cs2.memory.read(client_base + dwEntityList, 8, memprocfs.FLAG_NOCACHE))[0]
EntityList = struct.unpack("<Q", cs2.memory.read(EntityList + 0x10, 8, memprocfs.FLAG_NOCACHE))[0]
print(f"[+] Entered entitylist")

EntityPawnListEntry = struct.unpack("<Q", cs2.memory.read(client_base + dwEntityList, 8, memprocfs.FLAG_NOCACHE))[0]



def getentitys():
    entitys = []
    for index in range(1,64):
        try:
            EntityAddress = struct.unpack("<Q", cs2.memory.read(EntityList + (index + 1) * 0x78, 8, memprocfs.FLAG_NOCACHE))[0]
            Pawn = struct.unpack("<Q", cs2.memory.read(EntityAddress + m_hPlayerPawn, 8, memprocfs.FLAG_NOCACHE))[0]
            EntityPawnListEntry = struct.unpack("<Q", cs2.memory.read(EntityPawnListEntry + 0x10 + 8 * (Pawn & 0x7FFF) >> 9, 8, memprocfs.FLAG_NOCACHE))[0]
            Pawn = struct.unpack("<Q", cs2.memory.read(EntityPawnListEntry + 0x78 * (Pawn & 0x1FF), 8, memprocfs.FLAG_NOCACHE))[0]
            entityHp = struct.unpack("<I", cs2.memory.read(EntityAddress + m_iPawnHealth, 4, memprocfs.FLAG_NOCACHE))[0]
            if entityHp>0 and entityHp<=100:
                print(entityHp)
                entitys.append(entity)
            else:
                pass
            except:
                pass
    return(entitys)

print(len(getentitys()))

