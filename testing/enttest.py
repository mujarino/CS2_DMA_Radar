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

c4_ent = struct.unpack("<Q", cs2.memory.read(client_base + dwPlantedC4, 8, memprocfs.FLAG_NOCACHE))[0]
print(f"[+] Entitylist {entList}")

c4_node = struct.unpack("<Q", cs2.memory.read(c4_ent + m_pGameSceneNode, 8, memprocfs.FLAG_NOCACHE))[0]

c4_pos = struct.unpack("<Q", cs2.memory.read(c4_node + m_vecAbsOrigin, 8, memprocfs.FLAG_NOCACHE))[0]

print(c4_pos)



