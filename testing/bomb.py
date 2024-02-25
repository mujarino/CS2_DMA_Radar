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
m_flFlashBangTime = clientdll['C_CSPlayerPawnBase']['data']['m_flFlashBangTime']['value']
m_flFlashDuration = clientdll['C_CSPlayerPawnBase']['data']['m_flFlashDuration']['value']
m_flFlashOverlayAlpha = clientdll['C_CSPlayerPawnBase']['data']['m_flFlashOverlayAlpha']['value']
dwPlantedC4 = offsets['client_dll']['data']['dwPlantedC4']['value']
m_pGameSceneNode = clientdll['C_BaseEntity']['data']['m_pGameSceneNode']['value']
m_vecAbsOrigin = clientdll['CGameSceneNode']['data']['m_vecAbsOrigin']['value']

offset = int(input())

print('[+] offsets parsed')


vmm = memprocfs.Vmm(['-device', 'fpga'])


cs2 = vmm.process('cs2.exe')


client = cs2.module('client.dll')
client_base = client.base
print(f"[+] Client_base {client_base}")


c4_ent = struct.unpack("<Q", cs2.memory.read(client_base + dwPlantedC4, 8, memprocfs.FLAG_NOCACHE))[0]
print(cs2.memory.read(c4_ent + m_pGameSceneNode, 8, memprocfs.FLAG_NOCACHE))
c4_node = struct.unpack("<Q", cs2.memory.read(c4_ent + m_pGameSceneNode, 8, memprocfs.FLAG_NOCACHE))[0]
c4_pos = struct.unpack("<fff", cs2.memory.read(c4_node + m_vecAbsOrigin, 12, memprocfs.FLAG_NOCACHE))[0]
print(c4_pos)