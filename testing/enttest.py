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
m_bPawnHasDefuser = 0x800
m_iPawnHealth = 0x7F8
dwPlantedC4 = 0x18317D8
m_pGameSceneNode = 0x310
m_vecAbsOrigin = 0xC8

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
        try:
            EntityENTRY = struct.unpack("<Q", cs2.memory.read((entList + 0x8 * (entityId >> 9) + 0x10), 8, memprocfs.FLAG_NOCACHE))[0]
            print(entityId)
            entity = struct.unpack("<Q", cs2.memory.read(EntityENTRY + 120 * (entityId & 0x1FF), 8, memprocfs.FLAG_NOCACHE))[0]
            team = struct.unpack("<I", cs2.memory.read(entity + m_iTeamNum, 4, memprocfs.FLAG_NOCACHE))[0]
            print(team)
            if int(team) == 1 or int(team) == 2 or int(team) == 3:
                entitys.append(entity)
            else:
                pass
        except:
            pass
    return(entitys)

print(len(getentitys()))



