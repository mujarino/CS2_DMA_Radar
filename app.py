import memprocfs
import struct
import time
import pygame
import pygame_gui
import json
import math
import numpy as np
import os

dwEntityList = 0x17CE6A0
dwLocalPlayerPawn = 0x16D4F48
m_iHealth = 0x32C
m_vOldOrigin = 0x1224
m_iTeamNum = 0x3BF
m_angEyeAngles = 0x1518
mapNameVal = 0x1CC200

zoom_scale = 2

def world_to_minimap(x, y, pos_x, pos_y, scale, map_image, screen, zoom_scale):
    image_x = int((x - pos_x) * screen.get_width() / (map_image.get_width() * scale * zoom_scale))
    image_y = int((y - pos_y) * screen.get_height() / (map_image.get_height() * scale * zoom_scale))

    return int(image_x), int(image_y)

def getmapdata(mapname):
    with open(f'maps/{mapname}/meta.json', 'r') as f:
        data = json.load(f)
    scale = data['scale']
    x = data['offset']['x']
    y = data['offset']['y']
    print(x,y,scale)
    return scale,x,y

vmm = memprocfs.Vmm(['-device', 'fpga', '-disable-python', '-disable-symbols', '-disable-symbolserver', '-disable-yara', '-disable-yara-builtin', '-debug-pte-quality-threshold', '64'])
cs2 = vmm.process('cs2.exe')
client = cs2.module('client.dll')
client_base = client.base

def readmapfrommem():
    mapNameAddress_dll = cs2.module('matchmaking.dll')
    mapNameAddressbase = mapNameAddress_dll.base
    mapNameAddress = struct.unpack("<Q", cs2.memory.read(mapNameAddressbase + mapNameVal, 8, memprocfs.FLAG_NOCACHE))[0]
    mapName = struct.unpack("<32s", cs2.memory.read(mapNameAddress+0x4, 32, memprocfs.FLAG_NOCACHE))[0].decode()
    return mapName



print(f"[+] Client_base {client_base}")

entList = struct.unpack("<Q", cs2.memory.read(client_base + dwEntityList, 8, memprocfs.FLAG_NOCACHE))[0]
print(f"[+] Entitylist {entList}")

player = struct.unpack("<Q", cs2.memory.read(client_base + dwLocalPlayerPawn, 8, memprocfs.FLAG_NOCACHE))[0]
print(f"[+] Player {player}")

entitys = []
for entityId in range(1,2048):
    EntityENTRY = struct.unpack("<Q", cs2.memory.read((entList + 0x8 * (entityId >> 9) + 0x10), 8, memprocfs.FLAG_NOCACHE))[0]
    try:
        entity = struct.unpack("<Q", cs2.memory.read(EntityENTRY + 120 * (entityId & 0x1FF), 8, memprocfs.FLAG_NOCACHE))[0]
        entityHp = struct.unpack("<I", cs2.memory.read(entity + m_iHealth, 4, memprocfs.FLAG_NOCACHE))[0]
        if int(entityHp) != 0:
            team = struct.unpack("<I", cs2.memory.read(entity + m_iTeamNum, 4, memprocfs.FLAG_NOCACHE))[0]
            if int(team) == 1 or int(team) == 2 or int(team) == 3:
                entitys.append(entityId)
        else:
            pass
    except:
        pass
print(f"[+] Find entitys {entitys}")
print(f"[+]{readmapfrommem()}[+]")
mapname = str(readmapfrommem()).replace('\x00', '')
mapname = mapname.split('\\')[0]
if '\x00' in mapname:
    print("Строка содержит нулевой символ")
else:
    print("Строка не содержит нулевой символ")


scale,x,y = getmapdata(mapname)
if os.path.exists(f'maps/{mapname}'):
    print("test")
else:
    print('test2')
pygame.init()

clock = pygame.time.Clock()
screen_width, screen_height = 600, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Mean Radar")
radar_image = pygame.image.load(f'maps/{mapname}/radar.png')
font = pygame.font.Font(None, 24)

# Создание кнопок и меток
running = True
while running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((0, 0, 0))

    line_length = 10
    line_width = 2

    rotated_map_image, map_rect = pygame.transform.scale(radar_image, screen.get_size()), radar_image.get_rect()
    screen.blit(rotated_map_image, map_rect.topleft)

    for entityId in entitys:
        EntityENTRY = struct.unpack("<Q", cs2.memory.read((entList + 0x8 * (entityId >> 9) + 0x10), 8, memprocfs.FLAG_NOCACHE))[0]
        entity = struct.unpack("<Q", cs2.memory.read(EntityENTRY + 120 * (entityId & 0x1FF), 8, memprocfs.FLAG_NOCACHE))[0]
        pX = struct.unpack("<f", cs2.memory.read(entity + m_vOldOrigin +0x4, 4, memprocfs.FLAG_NOCACHE))[0]
        pY = struct.unpack("<f", cs2.memory.read(entity + m_vOldOrigin, 4, memprocfs.FLAG_NOCACHE))[0]
        Hp = struct.unpack("<I", cs2.memory.read(entity + m_iHealth, 4, memprocfs.FLAG_NOCACHE))[0]
        team = struct.unpack("<I", cs2.memory.read(entity + m_iTeamNum, 4, memprocfs.FLAG_NOCACHE))[0]
        EyeAngles = struct.unpack("<fff", cs2.memory.read(entity +(m_angEyeAngles +0x4) , 12, memprocfs.FLAG_NOCACHE))
        EyeAngles = math.radians(EyeAngles[0])
        transformed_x, transformed_y = world_to_minimap(pX, pY, x, y, scale, radar_image, screen, zoom_scale)
        line_end_x = transformed_x + math.sin(EyeAngles) * line_length
        line_end_y = transformed_y + math.cos(EyeAngles) * line_length
        if Hp > 0 and team == 2:
            pygame.draw.circle(screen, (255, 0, 0), (transformed_x, transformed_y), 5)
            line_color = (255, 0, 0)
            pygame.draw.line(screen, line_color, (transformed_x, transformed_y), (line_end_x, line_end_y), line_width)
        if Hp > 0 and team == 3:
            pygame.draw.circle(screen, (0, 0, 255), (transformed_x, transformed_y), 5)
            line_color = (0, 0, 255)
            pygame.draw.line(screen, line_color, (transformed_x, transformed_y), (line_end_x, line_end_y), line_width)
        text_surface = font.render(f'{Hp}', True, (255, 255, 255))
        screen.blit(text_surface, (transformed_x, transformed_y))
    pygame.display.flip()
pygame.quit()
