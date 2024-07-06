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
import pymem

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

offsets = get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/offsets.json').json()
clientdll = get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/client.dll.json').json()

#######################################

maps_with_split = ['de_nuke','de_vertigo']

dwEntityList = offsets['client.dll']['dwEntityList']
mapNameVal = offsets['matchmaking.dll']['dwGameTypes_mapName']
dwLocalPlayerPawn = offsets['client.dll']['dwLocalPlayerPawn']
dwPlantedC4 = offsets['client.dll']['dwPlantedC4']
dwGameRules = offsets['client.dll']['dwGameRules']
dwGlobalVars = offsets['client.dll']['dwGlobalVars']

m_angEyeAngles = clientdll['client.dll']['classes']['C_CSPlayerPawnBase']['fields']['m_angEyeAngles']
m_iTeamNum = clientdll['client.dll']['classes']['C_BaseEntity']['fields']['m_iTeamNum']
m_hPlayerPawn = clientdll['client.dll']['classes']['CCSPlayerController']['fields']['m_hPlayerPawn']
m_vOldOrigin = clientdll['client.dll']['classes']['C_BasePlayerPawn']['fields']['m_vOldOrigin']
m_iIDEntIndex = clientdll['client.dll']['classes']['C_CSPlayerPawnBase']['fields']['m_iIDEntIndex']
m_iHealth = clientdll['client.dll']['classes']['C_BaseEntity']['fields']['m_iHealth']
m_bIsDefusing = clientdll['client.dll']['classes']['C_CSPlayerPawn']['fields']['m_bIsDefusing']
m_iCompTeammateColor = clientdll['client.dll']['classes']['CCSPlayerController']['fields']['m_iCompTeammateColor']
m_flFlashOverlayAlpha = clientdll['client.dll']['classes']['C_CSPlayerPawnBase']['fields']['m_flFlashOverlayAlpha']
m_iszPlayerName = clientdll['client.dll']['classes']['CBasePlayerController']['fields']['m_iszPlayerName']
m_pClippingWeapon = clientdll['client.dll']['classes']['C_CSPlayerPawnBase']['fields']['m_pClippingWeapon']
m_pInGameMoneyServices = clientdll['client.dll']['classes']['CCSPlayerController']['fields']['m_pInGameMoneyServices']
m_iAccount = clientdll['client.dll']['classes']['CCSPlayerController_InGameMoneyServices']['fields']['m_iAccount']
m_pItemServices = clientdll['client.dll']['classes']['C_BasePlayerPawn']['fields']['m_pItemServices']
m_bHasDefuser = clientdll['client.dll']['classes']['CCSPlayer_ItemServices']['fields']['m_bHasDefuser']
m_pGameSceneNode = clientdll['client.dll']['classes']['C_BaseEntity']['fields']['m_pGameSceneNode']
m_vecAbsOrigin = clientdll['client.dll']['classes']['CGameSceneNode']['fields']['m_vecAbsOrigin']
m_hOwnerEntity = clientdll['client.dll']['classes']['C_BaseEntity']['fields']['m_hOwnerEntity']
m_bFreezePeriod = clientdll['client.dll']['classes']['C_CSGameRules']['fields']['m_bFreezePeriod']

print('[+] offsets parsed')

#######################################
zoom_scale = 2
map_folders = [f for f in os.listdir('maps') if os.path.isdir(os.path.join('maps', f))]
global_entity_list = []
playerpawn = 0

def world_to_minimap(x, y, pos_x, pos_y, scale, map_image, screen, zoom_scale):
	image_x = int((x - pos_x) * screen.get_width() / (map_image.get_width() * scale * zoom_scale))
	image_y = int((y - pos_y) * screen.get_height() / (map_image.get_height() * scale * zoom_scale))

	return int(image_x), int(image_y)

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


def readmapfrommem():
	mapNameAddress = pm.read_longlong(client_base + dwGlobalVars)
	mapnameAddresss = pm.read_longlong(mapNameAddress+0x1B8)
	mapname = pm.read_string(mapnameAddresss)
	for folder in map_folders:
		if folder in mapname:
			mapname = folder
			break
	if mapname != 'empty':
		print(f"[+] Found map {mapname}")
	mapname = str(mapname)
	return mapname

def get_only_mapname():
	mapNameAddress = pm.read_longlong(client_base + dwGlobalVars)
	mapnameAddresss = pm.read_longlong(mapNameAddress+0x1B8)
	mapname = pm.read_string(mapnameAddresss)
	return mapname

def getmapdata(mapname):
	with open(f'maps/{mapname}/meta.json', 'r') as f:
		data = json.load(f)
	scale = data['scale']
	x = data['offset']['x']
	y = data['offset']['y']
	return scale,x,y

def getlowermapdata(mapname):
    with open(f'maps/{mapname}/meta.json', 'r') as f:
        data = json.load(f)
    lowerx = data['splits']['offset']['x']
    lowery = data['splits']['offset']['y']
    z = data['splits']['zRange']['z']
    return lowerx,lowery,z


pm = pymem.Pymem("cs2.exe")

client_base = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
print(f"[+] Finded client base")

entList = pm.read_longlong(client_base + dwEntityList)
print(f"[+] Entered entitylist")

mapNameAddressbase = pymem.process.module_from_name(pm.process_handle, "matchmaking.dll").lpBaseOfDll

EntityList = pm.read_longlong(client_base + dwEntityList)
EntityList = pm.read_longlong(EntityList + 0x10)
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
	lowerx,lowery,z = getlowermapdata(mapname)
	print(lowerx,lowery,z)
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
                    scale += 0.05
                    scale_label.set_text(f'Scale: {scale:.2f}')
                elif event.ui_element == scale_minus_button:
                    scale -= 0.05
                    scale_label.set_text(f'Scale: {scale:.2f}')
                elif event.ui_element == x_plus_button:
                    x += 25.0
                    x_label.set_text(f'X: {x:.1f}')
                elif event.ui_element == x_minus_button:
                    x -= 25.0
                    x_label.set_text(f'X: {x:.1f}')
                elif event.ui_element == y_plus_button:
                    y += 25.0
                    y_label.set_text(f'Y: {y:.1f}')
                elif event.ui_element == y_minus_button:
                    y -= 25.0
                    y_label.set_text(f'Y: {y:.1f}')

    manager.update(time_delta)

    screen.fill((0, 0, 0))

    rotated_map_image, map_rect = pygame.transform.scale(radar_image, screen.get_size()), radar_image.get_rect()
    screen.blit(rotated_map_image, map_rect.topleft)
    playerpawn = pm.read_longlong(client_base + dwLocalPlayerPawn)
    playerTeam = pm.read_int(playerpawn + m_iTeamNum)
    EntityPawnListEntry = pm.read_longlong(client_base + dwEntityList)
    for i in range(maxclients):
        try:
            EntityAddress = pm.read_longlong(EntityList + (i + 1) * 0x78)
            Pawn = pm.read_longlong(EntityAddress + m_hPlayerPawn)
            newEntityPawnListEntry = pm.read_longlong(EntityPawnListEntry + 0x10 + 8 * ((Pawn & 0x7FFF) >> 9))
            entity_id = pm.read_longlong(newEntityPawnListEntry + 0x78 * (Pawn & 0x1FF))
            Hp = pm.read_int(entity_id + m_iHealth)
            if Hp!= 0:
                pX = pm.read_float(entity_id + m_vOldOrigin +0x4)
                pY = pm.read_float(entity_id + m_vOldOrigin)
                pZ = pm.read_float(entity_id + m_vOldOrigin +0x8)
                team = pm.read_int(entity_id + m_iTeamNum)
                EyeAngles = pm.read_float(entity_id + (m_angEyeAngles +0x4))
                EyeAngles = math.radians(EyeAngles+rot_angle)
                isdefusing = pm.read_int(entity_id + m_bIsDefusing)
                flash_alpha = int(pm.read_int(entity_id + m_flFlashOverlayAlpha))  
            if Hp > 0 and team == 2:
                transformed_x, transformed_y = world_to_minimap(pX, pY, x, y, scale, radar_image, screen, zoom_scale)
                pygame.draw.circle(screen, (255, 0, 0), (transformed_x, transformed_y), 5)
            if Hp > 0 and team == 3:
                transformed_x, transformed_y = world_to_minimap(pX, pY, x, y, scale, radar_image, screen, zoom_scale)
                pygame.draw.circle(screen, (0, 0, 255), (transformed_x, transformed_y), 5)
            text_surface = font.render(f'{Hp}', True, (255, 255, 255))
            print(f'{transformed_x}, {transformed_y}')
            screen.blit(text_surface, (transformed_x, transformed_y))
        except:
            pass
    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
