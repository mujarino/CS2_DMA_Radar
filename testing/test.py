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


def readmapfrommem():
    mapNameAddress_dll = cs2.module('matchmaking.dll')
    mapNameAddressbase = mapNameAddress_dll.base
    mapNameAddress = struct.unpack("<Q", cs2.memory.read(mapNameAddressbase + mapNameVal, 8, memprocfs.FLAG_NOCACHE))[0]
    mapName = struct.unpack("<32s", cs2.memory.read(mapNameAddress+0x4, 32, memprocfs.FLAG_NOCACHE))[0].decode('utf-8', 'ignore')
    return str(mapName)

vmm = memprocfs.Vmm(['-device', 'fpga'])
cs2 = vmm.process('cs2.exe')
print(readmapfrommem())
vmm.close()