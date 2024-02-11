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

mapNameAddress_dll = cs2.module('matchmaking.dll')
mapNameAddressbase = mapNameAddress_dll.base

# Read the entire 'matchmaking.dll' into a buffer
buffer = cs2.memory.read(mapNameAddressbase, memprocfs.FLAG_NOCACHE)

# Find 'de_mirage' in the buffer
position = buffer.find(b'de_mirage')

if position != -1:
    # Calculate the address of 'de_mirage'
    address = mapNameAddressbase + position
    print("Found 'de_mirage' at address: ", hex(address))
else:
    print("'de_mirage' not found in 'matchmaking.dll'")
