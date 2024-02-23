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
m_iIDEntIndex = 0x15A4
m_iHealth = 0x334

vmm = memprocfs.Vmm(['-device', 'fpga'])


cs2 = vmm.process('cs2.exe')


client = cs2.module('client.dll')
client_base = client.base
print(f"[+] Client_base {client_base}")
entList = struct.unpack("<Q", cs2.memory.read(client_base + dwEntityList, 8, memprocfs.FLAG_NOCACHE))[0]


while True:
    player = struct.unpack("<Q", cs2.memory.read(client_base + dwLocalPlayerPawn, 8, memprocfs.FLAG_NOCACHE))[0]
    entityId = struct.unpack("<I", cs2.memory.read(player + m_iIDEntIndex, 4, memprocfs.FLAG_NOCACHE))[0]
    print(entityId)
    if entityId > 0:
        try:
            entEntry = struct.unpack("<Q", cs2.memory.read(entList + 0x8 * (entityId >> 9) + 0x10, 8, memprocfs.FLAG_NOCACHE))[0]
            entity_pawn = struct.unpack("<Q", cs2.memory.read(entEntry + 120 * (entityId & 0x1FF), 8, memprocfs.FLAG_NOCACHE))[0]
            IsDefusing = struct.unpack("<I", cs2.memory.read(entity_pawn +(m_bIsDefusing +0x4) , 4, memprocfs.FLAG_NOCACHE))
            print(entityId,IsDefusing)
        except:
            pass

