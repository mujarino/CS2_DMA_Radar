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
import threading
import random
from pygame.locals import *


with open(f'config.json', 'r') as f:
    settings = json.load(f)

triangle_length = settings['triangle_length']
circle_size = settings['circle_size']
hp_font_size = settings['hp_font_size']
rot_angle = settings['rot_angle']
cross_size = settings['cross_size']
teammate_setting = settings['teammates']
altgirlpic_instead_nomappic = settings['altgirlpic_instead_nomappic']
update_offsets = settings['update_offsets']
maxclients = int(settings['maxclients'])


#######################################

try:
    offsets = get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/offsets.json').json()
    clientdll = get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/client.dll.json').json()
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

print('[+] offsets parsed')

#######################################
zoom_scale = 2

maps_with_split = []

def world_to_minimap(x, y, pos_x, pos_y, scale, map_image, screen, zoom_scale):
    image_x = int((x - pos_x) * screen.get_width() / (map_image.get_width() * scale * zoom_scale))
    image_y = int((y - pos_y) * screen.get_height() / (map_image.get_height() * scale * zoom_scale))

    return int(image_x), int(image_y)

def readmapfrommem():
    mapNameAddress_dll = cs2.module('matchmaking.dll')
    mapNameAddressbase = mapNameAddress_dll.base
    mapNameAddress = struct.unpack("<Q", cs2.memory.read(mapNameAddressbase + mapNameVal, 8, memprocfs.FLAG_NOCACHE))[0]
    mapName = struct.unpack("<32s", cs2.memory.read(mapNameAddress+0x4, 32, memprocfs.FLAG_NOCACHE))[0].decode('utf-8', 'ignore')
    return str(mapName)

def getmapdata(mapname):
    with open(f'maps/{mapname}/meta.json', 'r') as f:
        data = json.load(f)
    scale = data['scale']
    x = data['offset']['x']
    y = data['offset']['y']
    return scale,x,y

vmm = memprocfs.Vmm(['-device', 'fpga', '-disable-python', '-disable-symbols', '-disable-symbolserver', '-disable-yara', '-disable-yara-builtin', '-debug-pte-quality-threshold', '64'])
cs2 = vmm.process('cs2.exe')
client = cs2.module('client.dll')
client_base = client.base
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
            entitys.append(entityId)
            team = struct.unpack("<I", cs2.memory.read(entity + m_iTeamNum, 4, memprocfs.FLAG_NOCACHE))[0]
            print(team)
        else:
            pass
    except:
        pass
print(entitys)

mapname = readmapfrommem()

map_folders = [f for f in os.listdir('maps') if os.path.isdir(os.path.join('maps', f))]

for folder in map_folders:
    if folder in mapname:
        mapname = folder
        break

if mapname == 'empty':
    print(f"[-] You are not connected to map")
    exit()
if os.path.exists(f'maps/{mapname}'):
    pass
else:
    print(f'[-] Please, import this map first ({mapname})')
    exit()
print(f"[+] Found map {mapname}")
if mapname in maps_with_split:
    lowerx,lowery = getlowermapdata(mapname)
    print(lowerx,lowery)
scale,x,y = getmapdata(mapname)


pygame.init()

clock = pygame.time.Clock()

screen_width, screen_height = 600, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Mean Radar")

radar_image = pygame.image.load(f'maps/{mapname}/radar.png')

font = pygame.font.Font(None, 24)

manager = pygame_gui.UIManager((600, 600))

# Создание кнопок и меток
scale_plus_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 50), (30, 30)), text='+', manager=manager)
scale_minus_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((90, 50), (30, 30)), text='-', manager=manager)
scale_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((130, 50), (70, 30)), text='Scale: 1.0', manager=manager)

x_plus_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 90), (30, 30)), text='+', manager=manager)
x_minus_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((90, 90), (30, 30)), text='-', manager=manager)
x_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((130, 90), (70, 30)), text='X: 0.0', manager=manager)

y_plus_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 130), (30, 30)), text='+', manager=manager)
y_minus_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((90, 130), (30, 30)), text='-', manager=manager)
y_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((130, 130), (70, 30)), text='Y: 0.0', manager=manager)

running = True
while running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == scale_plus_button:
                    scale += 0.1
                    scale_label.set_text(f'Scale: {scale:.1f}')
                elif event.ui_element == scale_minus_button:
                    scale -= 0.1
                    scale_label.set_text(f'Scale: {scale:.1f}')
                elif event.ui_element == x_plus_button:
                    x += 50.0
                    x_label.set_text(f'X: {x:.1f}')
                elif event.ui_element == x_minus_button:
                    x -= 50.0
                    x_label.set_text(f'X: {x:.1f}')
                elif event.ui_element == y_plus_button:
                    y += 50.0
                    y_label.set_text(f'Y: {y:.1f}')
                elif event.ui_element == y_minus_button:
                    y -= 50.0
                    y_label.set_text(f'Y: {y:.1f}')

    manager.update(time_delta)

    screen.fill((0, 0, 0))

    rotated_map_image, map_rect = pygame.transform.scale(radar_image, screen.get_size()), radar_image.get_rect()
    screen.blit(rotated_map_image, map_rect.topleft)

    for entityId in entitys:
        EntityENTRY = struct.unpack("<Q", cs2.memory.read((entList + 0x8 * (entityId >> 9) + 0x10), 8, memprocfs.FLAG_NOCACHE))[0]
        entity = struct.unpack("<Q", cs2.memory.read(EntityENTRY + 120 * (entityId & 0x1FF), 8, memprocfs.FLAG_NOCACHE))[0]
        pX = struct.unpack("<f", cs2.memory.read(entity + m_vOldOrigin +0x4, 4, memprocfs.FLAG_NOCACHE))[0]
        pY = struct.unpack("<f", cs2.memory.read(entity + m_vOldOrigin, 4, memprocfs.FLAG_NOCACHE))[0]
        Hp = struct.unpack("<I", cs2.memory.read(entity + m_iHealth, 4, memprocfs.FLAG_NOCACHE))[0]
        team = struct.unpack("<I", cs2.memory.read(entity + m_iTeamNum, 4, memprocfs.FLAG_NOCACHE))[0]
        if Hp > 0 and team == 2:
            transformed_x, transformed_y = world_to_minimap(pX, pY, x, y, scale, radar_image, screen, zoom_scale)
            pygame.draw.circle(screen, (255, 0, 0), (transformed_x, transformed_y), 5)
        if Hp > 0 and team == 3:
            transformed_x, transformed_y = world_to_minimap(pX, pY, x, y, scale, radar_image, screen, zoom_scale)
            pygame.draw.circle(screen, (0, 0, 255), (transformed_x, transformed_y), 5)
        text_surface = font.render(f'{Hp}', True, (255, 255, 255))
        print(f'{transformed_x}, {transformed_y}')
        screen.blit(text_surface, (transformed_x, transformed_y))

    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()
