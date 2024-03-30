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

try:
    offsets = get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/win/offsets.json').json()
    clientdll = get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/win/client.dll.json').json()
except Exception as e:
    print(e)
    try:
        print('[-]Unable to parse offsets. Using from current folder')
        with open(f'client.dll.json', 'r') as a:
            clientdll = json.load(a)
        with open(f'offsets.json', 'r') as b:
            offsets = json.load(b)
    except:
        print('[-] put offsets.json and client.dll.json in main folder')
        exit()


#######################################

maps_with_split = ['de_nuke','de_vertigo']

dwEntityList = offsets['client.dll']['dwEntityList']
mapNameVal = offsets['matchmaking.dll']['dwGameTypes_mapName']
dwLocalPlayerPawn = offsets['client.dll']['dwLocalPlayerPawn']

m_iPawnHealth = clientdll['client.dll']['classes']['CCSPlayerController']['fields']['m_iPawnHealth']
m_iPawnArmor = clientdll['client.dll']['classes']['CCSPlayerController']['fields']['m_iPawnArmor']
m_bPawnIsAlive = clientdll['client.dll']['classes']['CCSPlayerController']['fields']['m_bPawnIsAlive']
m_angEyeAngles = clientdll['client.dll']['classes']['C_CSPlayerPawnBase']['fields']['m_angEyeAngles']
m_iTeamNum = clientdll['client.dll']['classes']['C_BaseEntity']['fields']['m_iTeamNum']
m_hPlayerPawn = clientdll['client.dll']['classes']['CCSPlayerController']['fields']['m_hPlayerPawn']
m_vOldOrigin = clientdll['client.dll']['classes']['C_BasePlayerPawn']['fields']['m_vOldOrigin']
m_iIDEntIndex = clientdll['client.dll']['classes']['C_CSPlayerPawnBase']['fields']['m_iIDEntIndex']
m_iHealth = clientdll['client.dll']['classes']['C_BaseEntity']['fields']['m_iHealth']
m_bIsDefusing = clientdll['client.dll']['classes']['C_CSPlayerPawnBase']['fields']['m_bIsDefusing']
m_bPawnHasDefuser = clientdll['client.dll']['classes']['CCSPlayerController']['fields']['m_bPawnHasDefuser']
m_iCompTeammateColor = clientdll['client.dll']['classes']['CCSPlayerController']['fields']['m_iCompTeammateColor']
m_flFlashOverlayAlpha = clientdll['client.dll']['classes']['C_CSPlayerPawnBase']['fields']['m_flFlashOverlayAlpha']
m_iszPlayerName = clientdll['client.dll']['classes']['CBasePlayerController']['fields']['m_iszPlayerName']
m_pClippingWeapon = clientdll['client.dll']['classes']['C_CSPlayerPawnBase']['fields']['m_pClippingWeapon']
m_iRoundTime = clientdll['client.dll']['classes']['C_CSGameRules']['fields']['m_iRoundTime']

print('[+] offsets parsed')


def read_string_memory(address):
    data = b""
    try:
        while True:
            byte = cs2.memory.read(address, 1)
            if byte == b'\0':
                break
            data += byte
            address += 1
        decoded_data = data.decode('utf-8')
        return decoded_data
    except UnicodeDecodeError:
        return data

def get_weapon(ptr):
    b1 = struct.unpack("<Q", cs2.memory.read(ptr + m_pClippingWeapon, 8, memprocfs.FLAG_NOCACHE))[0]
    base = struct.unpack("<Q", cs2.memory.read(b1 + 0x10, 8, memprocfs.FLAG_NOCACHE))[0]
    data = struct.unpack("<Q", cs2.memory.read(base + 0x20, 8, memprocfs.FLAG_NOCACHE))[0]
    finall = read_string_memory(data)
    return str(finall)[7:]


vmm = memprocfs.Vmm(['-device', 'fpga'])
cs2 = vmm.process('cs2.exe')
client = cs2.module('client.dll')
client_base = client.base
print(f"[+] Finded client base")

for i in range(2):
    EntityAddress = struct.unpack("<Q", cs2.memory.read(EntityList + (i + 1) * 0x78, 8, memprocfs.FLAG_NOCACHE))[0]
    Pawn = struct.unpack("<Q", cs2.memory.read(EntityAddress + m_hPlayerPawn, 8, memprocfs.FLAG_NOCACHE))[0]
    newEntityPawnListEntry = struct.unpack("<Q", cs2.memory.read(EntityPawnListEntry + 0x10 + 8 * ((Pawn & 0x7FFF) >> 9), 8, memprocfs.FLAG_NOCACHE))[0]
    entity_id = struct.unpack("<Q", cs2.memory.read(newEntityPawnListEntry + 0x78 * (Pawn & 0x1FF), 8, memprocfs.FLAG_NOCACHE))[0]
    print(get_weapon(ptr))

vmm.close()