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

dwEntityList = 0x17CE6A0
dwLocalPlayerPawn = 0x16D4F48
m_iIDEntIndex = 0x1544
m_iHealth = 0x32C
m_angEyeAngles = 0x1518
m_iCompTeammateColor = 0x738
m_iItemDefinitionIndex = 0x1BA

vmm = memprocfs.Vmm(['-device', 'fpga'])


cs2 = vmm.process('cs2.exe')


client = cs2.module('client.dll')
client_base = client.base
print(f"[+] Client_base {client_base}")

entList = struct.unpack("<Q", cs2.memory.read(client_base + dwEntityList, 8, memprocfs.FLAG_NOCACHE))[0]
print(f"[+] Entitylist {entList}")

player = struct.unpack("<Q", cs2.memory.read(client_base + dwLocalPlayerPawn, 8, memprocfs.FLAG_NOCACHE))[0]
print(f"[+] Player {player}")

def getinfo(entityId):
    EntityENTRY = struct.unpack("<Q", cs2.memory.read((entList + 0x8 * (entityId >> 9) + 0x10), 8, memprocfs.FLAG_NOCACHE))[0]
    entity = struct.unpack("<Q", cs2.memory.read(EntityENTRY + 120 * (entityId & 0x1FF), 8, memprocfs.FLAG_NOCACHE))[0]
    for i in range(1,16):
        try:
            color = struct.unpack("<H", cs2.memory.read(entity + m_iItemDefinitionIndex, i, memprocfs.FLAG_NOCACHE))[0]
            print(f"[+] entityId {entityId} | hasbomb {color}")
        except:
            print('чтение не удалось')
    return 

entitys = []
for entityId in range(1,2048):
    EntityENTRY = struct.unpack("<Q", cs2.memory.read((entList + 0x8 * (entityId >> 9) + 0x10), 8, memprocfs.FLAG_NOCACHE))[0]
    try:
        entity = struct.unpack("<Q", cs2.memory.read(EntityENTRY + 120 * (entityId & 0x1FF), 8, memprocfs.FLAG_NOCACHE))[0]
        entityHp = struct.unpack("<I", cs2.memory.read(entity + m_iHealth, 4, memprocfs.FLAG_NOCACHE))[0]
        if int(entityHp) != 0:
            entitys.append(entityId)
        else:
            pass
    except:
        pass
print(entitys)

for entity in entitys:
    print(getinfo(entity))

