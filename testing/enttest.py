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
from requests import get

#######################################

offsets = get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/generated/offsets.json').json()
clientdll = get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/generated/client.dll.json').json()

#######################################

maps_with_split = ['de_nuke','de_vertigo']
dwEntityList = offsets['client_dll']['data']['dwEntityList']['value']
dwLocalPlayerPawn = offsets['client_dll']['data']['dwLocalPlayerPawn']['value']
m_iPawnHealth = clientdll['CCSPlayerController']['data']['m_iPawnHealth']['value']
m_iPawnArmor = clientdll['CCSPlayerController']['data']['m_iPawnArmor']['value']
m_bPawnIsAlive = clientdll['CCSPlayerController']['data']['m_bPawnIsAlive']['value']
m_angEyeAngles = clientdll['C_CSPlayerPawnBase']['data']['m_angEyeAngles']['value']
m_iTeamNum = clientdll['C_BaseEntity']['data']['m_iTeamNum']['value']
m_hPlayerPawn = clientdll['CCSPlayerController']['data']['m_hPlayerPawn']['value']
m_vOldOrigin = clientdll['C_BasePlayerPawn']['data']['m_vOldOrigin']['value']
m_iIDEntIndex = clientdll['C_CSPlayerPawnBase']['data']['m_iIDEntIndex']['value']
m_iHealth = clientdll['C_BaseEntity']['data']['m_iHealth']['value']
mapNameVal = offsets['matchmaking_dll']['data']['dwGameTypes_mapName']['value']


print('[+] offsets parsed')


vmm = memprocfs.Vmm(['-device', 'fpga'])


cs2 = vmm.process('cs2.exe')


client = cs2.module('client.dll')
client_base = client.base
print(f"[+] Client_base {client_base}")
EntityList = struct.unpack("<Q", cs2.memory.read(client_base + dwEntityList, 8, memprocfs.FLAG_NOCACHE))[0]
EntityList = struct.unpack("<Q", cs2.memory.read(EntityList + 0x10, 8, memprocfs.FLAG_NOCACHE))[0]
for i in range(1,64):

    EntityAddress = struct.unpack("<Q", cs2.memory.read(EntityList + (index + 1) * 0x78, 8, memprocfs.FLAG_NOCACHE))[0]
    EntityPawnListEntry = struct.unpack("<Q", cs2.memory.read(client_base + dwEntityList, 8, memprocfs.FLAG_NOCACHE))[0]
    Pawn = struct.unpack("<Q", cs2.memory.read(EntityAddress + m_hPlayerPawn, 8, memprocfs.FLAG_NOCACHE))[0]
    EntityPawnListEntry = struct.unpack("<Q", cs2.memory.read(EntityPawnListEntry + 0x10 + 8 * ((Pawn & 0x7FFF) >> 9), 8, memprocfs.FLAG_NOCACHE))[0]
    Pawn = struct.unpack("<Q", cs2.memory.read(EntityPawnListEntry + 0x78 * (Pawn & 0x1FF), 8, memprocfs.FLAG_NOCACHE))[0]
    pX = struct.unpack("<f", cs2.memory.read(Pawn + m_vOldOrigin +0x4, 4, memprocfs.FLAG_NOCACHE))[0]
    pY = struct.unpack("<f", cs2.memory.read(Pawn + m_vOldOrigin, 4, memprocfs.FLAG_NOCACHE))[0]
    pZ = struct.unpack("<f", cs2.memory.read(Pawn + m_vOldOrigin +0x8, 4, memprocfs.FLAG_NOCACHE))[0]
    print(struct.unpack(f'x: {pX} y: {pY} z: {pZ}',"<I", cs2.memory.read(EntityAddress + m_iPawnHealth, 4, memprocfs.FLAG_NOCACHE))[0])


