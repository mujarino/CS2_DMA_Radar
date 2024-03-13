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

print('[+] offsets parsed')


vmm = memprocfs.Vmm(['-device', 'fpga'])


cs2 = vmm.process('cs2.exe')


client = cs2.module('client.dll')
client_base = client.base
print(f"[+] Client_base {client_base}")
def get_weapon_name(weapon_id):
    weapon_names = {
        59: "T knife",
        42: "CT knife",
        1: "deagle",
        2: "elite",
        3: "fiveseven",
        4: "glock",
        64: "revolver",
        32: "p2000",
        36: "p250",
        #61: "usp-s",
        262205: "usp-s",
        30: "tec9",
        63: "cz75a",
        17: "mac10",
        24: "ump45",
        26: "bizon",
        33: "mp7",
        34: "mp9",
        19: "p90",
        13: "galil",
        10: "famas",
        60: "m4a1_silencer",
        16: "m4a4",
        8: "aug",
        39: "sg556",
        7: "ak47",
        11: "g3sg1",
        38: "scar20",
        9: "awp",
        40: "ssg08",
        25: "xm1014",
        29: "sawedoff",
        27: "mag7",
        35: "nova",
        28: "negev",
        14: "m249",
        31: "zeus",
        43: "flashbang",
        44: "hegrenade",
        45: "smokegrenade",
        46: "molotov",
        47: "decoy",
        48: "incgrenade",
        49: "c4"
    }

    return weapon_names.get(weapon_id, "Unknown weapon")


def get_weapon(ptr):
    try:
        b1 = struct.unpack("<Q", cs2.memory.read(ptr + 0x1308, 8, memprocfs.FLAG_NOCACHE))[0]
        b2 = struct.unpack("<I", cs2.memory.read(b1 + 0x1BA + 0x50 + 0x1098, 4, memprocfs.FLAG_NOCACHE))[0]
        weapon_id = get_weapon_name(b2)
    except:
        return None
    return weapon_id

EntityList = struct.unpack("<Q", cs2.memory.read(client_base + dwEntityList, 8, memprocfs.FLAG_NOCACHE))[0]
EntityList = struct.unpack("<Q", cs2.memory.read(EntityList + 0x10, 8, memprocfs.FLAG_NOCACHE))[0]
for i in range(0,64):
    try:
        EntityAddress = struct.unpack("<Q", cs2.memory.read(EntityList + (i + 1) * 0x78, 8, memprocfs.FLAG_NOCACHE))[0]
        EntityPawnListEntry = struct.unpack("<Q", cs2.memory.read(client_base + dwEntityList, 8, memprocfs.FLAG_NOCACHE))[0]
        Pawn = struct.unpack("<Q", cs2.memory.read(EntityAddress + m_hPlayerPawn, 8, memprocfs.FLAG_NOCACHE))[0]
        EntityPawnListEntry = struct.unpack("<Q", cs2.memory.read(EntityPawnListEntry + 0x10 + 8 * ((Pawn & 0x7FFF) >> 9), 8, memprocfs.FLAG_NOCACHE))[0]
        Pawn = struct.unpack("<Q", cs2.memory.read(EntityPawnListEntry + 0x78 * (Pawn & 0x1FF), 8, memprocfs.FLAG_NOCACHE))[0]
        health = struct.unpack("<I", cs2.memory.read(EntityAddress + m_iPawnHealth, 4, memprocfs.FLAG_NOCACHE))[0]
        try:
            print(getweapon(Pawn), 'PAWN')
        except:
            pass
        try:
            print(getweapon(EntityAddress), 'EntityAddress')
        except:
            pass
    except Exception as e:
        print(e)

