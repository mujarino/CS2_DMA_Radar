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
mapNameVal = 0x196F31C

vmm = memprocfs.Vmm(['-device', 'fpga'])

cs2 = vmm.process('cs2.exe')

mapNameAddress_dll = cs2.module('client.dll')
mapNameAddressbase = mapNameAddress_dll.base
mapNameAddress = struct.unpack("<32s", cs2.memory.read(mapNameAddressbase + mapNameVal, 32, memprocfs.FLAG_NOCACHE))[0].decode('utf-8', 'ignore')
print(mapNameAddress)
mapName = struct.unpack("<32s", cs2.memory.read(mapNameAddress+0x4, 32, memprocfs.FLAG_NOCACHE))[0].decode('utf-8', 'ignore')
print(mapName)