import pymem
import struct
import time
import json
import math
import pygame
import pygame_gui
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
update_offsets = str(settings['update_offsets'])
maxclients = int(settings['maxclients'])

mapname = 'de_mirage'
#######################################

if update_offsets == '1':
    try:
        offsets = get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/offsets.json').json()
        clientdll = get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/client_dll.json').json()
    except Exception as e:
        print(e)
        try:
            print('[-] ' + Fore.RED + 'Unable to parse offsets. Using from current folder' + Style.RESET_ALL)
            with open(f'client.dll.json', 'r') as a:
                clientdll = json.load(a)
            with open(f'offsets.json', 'r') as b:
                offsets = json.load(b)
        except:
            print('[-] ' + Fore.RED + 'Put offsets.json and client.dll.json in main folder' + Style.RESET_ALL)
            exit()
else:
    print('parsing from folder')
    with open('offsets.json', 'r') as file:
        offsets = json.load(file)
    with open('client.dll.json', 'r') as file:
        clientdll = json.load(file)


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




def get_weapon(ptr):
    try:
        b1 = pm.read_longlong(ptr + m_pClippingWeapon)
        base = pm.read_longlong(b1 + 0x10)
        data = pm.read_longlong(base + 0x20)
        finall = pm.read_string(data)
        return str(finall)[7:]
    except:
        return 'None'


def world_to_minimap(x, y, pos_x, pos_y, scale, map_image, screen, zoom_scale, rotation_angle):
    try:
        image_x = int((x - pos_x) * screen.get_width() / (map_image.get_width() * scale * zoom_scale))
        image_y = int((y - pos_y) * screen.get_height() / (map_image.get_height() * scale * zoom_scale))
        center_x, center_y = screen_height // 2, screen_width // 2
        image_x, image_y = rotate_point((center_x, center_y), (image_x, image_y), rotation_angle)
        return image_x * 0.85, image_y * 0.95
    except:
        return 0,0

def rotate_point(center, point, angle):
    angle_rad = math.radians(angle)
    temp_point = point[0] - center[0], center[1] - point[1]
    temp_point = (temp_point[0]*math.cos(angle_rad)-temp_point[1]*math.sin(angle_rad), temp_point[0]*math.sin(angle_rad)+temp_point[1]*math.cos(angle_rad))
    temp_point = temp_point[0] + center[0], center[1] - temp_point[1]
    return temp_point

def toggle_state():
    global teammate_setting
    teammate_setting = (teammate_setting + 1) % 3

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

def checkissplit(mapname):
    for name in maps_with_split:
        if name in mapname:
            return True


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


def rotate_image(image, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect().center)
    return rotated_image, new_rect

pm = pymem.Pymem("cs2.exe")

client_base = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
print(f"[+] Finded client base")

entList = pm.read_longlong(client_base + dwEntityList)
print(f"[+] Entered entitylist")

mapNameAddressbase = pymem.process.module_from_name(pm.process_handle, "matchmaking.dll").lpBaseOfDll

EntityList = pm.read_longlong(client_base + dwEntityList)
EntityList = pm.read_longlong(EntityList + 0x10)


pygame.init()
manager = pygame_gui.UIManager((800, 800))
clock = pygame.time.Clock()
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("CS2 Radar")
font = pygame.font.Font(None, hp_font_size)
fontt = pygame.font.Font(None, 24)

rot_plus_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, screen_height-60), (120, 30)), text='ANGLE+90', manager=manager)
teammates_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((170, screen_height-60), (120, 30)), text='TEAMMATES', manager=manager) 


running = True
while running:
    mapname = 'de_mirage'
    if 'empty' in mapname:
        if altgirlpic_instead_nomappic == 1:
            png_files = [f for f in os.listdir('data/nomap_pics') if f.endswith('.png')]
            if png_files:
                random_file = random.choice(png_files)
            image = pygame.image.load(f'data/nomap_pics/{random_file}')
        else:
            image = pygame.image.load(f'maps/empty/1.png')
        image = pygame.transform.scale(image, (screen_width, screen_height))
        screen.blit(image, (0, 0))
        pygame.display.flip()
        time.sleep(8)
        continue
    if os.path.exists(f'maps/{mapname}'):
        pass
    else:
        print(f'[-] Please, import this map first ({mapname})')
        continue
    if mapname in maps_with_split:
        lowerx,lowery,lowerz = getlowermapdata(mapname)
    scale,x,y = getmapdata(mapname)
    map_image = pygame.image.load(f'maps/{mapname}/radar.png')
    while not 'empty' in 'de_mirage':
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == rot_plus_button:
                        rot_angle += 90
                    if event.ui_element == teammates_button:
                        toggle_state()
            elif event.type == VIDEORESIZE:
                screen_width, screen_height = event.size
                
        manager.update(time_delta)

        screen.fill((0, 0, 0))

        triangle_color = (255, 255, 255)

        rotated_map_image, map_rect = rotate_image(pygame.transform.scale(map_image, screen.get_size()), rot_angle)
        new_width = int(screen_width * 0.85)
        new_height = int(screen_height * 0.95)
        rotated_map_image = pygame.transform.scale(rotated_map_image, (new_width, new_height))
        screen.blit(rotated_map_image, (0, 0))
        manager.draw_ui(screen) 
        wepname = []
        try:
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
                    if Hp != 0:
                        pX = pm.read_float(entity_id + m_vOldOrigin +0x4)
                        pY = pm.read_float(entity_id + m_vOldOrigin)
                        pZ = pm.read_float(entity_id + m_vOldOrigin +0x8)
                        team = pm.read_int(entity_id + m_iTeamNum)
                        EyeAngles = pm.read_float(entity_id + (m_angEyeAngles +0x4))
                        EyeAngles = math.radians(EyeAngles+rot_angle)
                        isdefusing = pm.read_int(entity_id + m_bIsDefusing)
                        flash_alpha = int(pm.read_int(entity_id + m_flFlashOverlayAlpha))
                        if checkissplit(mapname):
                            if pZ<lowerz:
                                transformed_x, transformed_y = world_to_minimap(pX, pY, lowerx, lowery, scale, map_image, screen, zoom_scale, rot_angle)
                            else:
                                transformed_x, transformed_y = world_to_minimap(pX, pY, x, y, scale, map_image, screen, zoom_scale, rot_angle)
                        else:
                            transformed_x, transformed_y = world_to_minimap(pX, pY, x, y, scale, map_image, screen, zoom_scale, rot_angle)
                        triangle_top_x = transformed_x + math.sin(EyeAngles) * triangle_length
                        triangle_top_y = transformed_y + math.cos(EyeAngles) * triangle_length
                        triangle_left_x = transformed_x + math.sin(EyeAngles + math.pi / 3) * triangle_length / 2
                        triangle_left_y = transformed_y + math.cos(EyeAngles + math.pi / 3) * triangle_length / 2
                        triangle_right_x = transformed_x + math.sin(EyeAngles - math.pi / 3) * triangle_length / 2
                        triangle_right_y = transformed_y + math.cos(EyeAngles - math.pi / 3) * triangle_length / 2
                        if teammate_setting == 2:
                            if team == playerTeam:
                                color = pm.read_int(EntityAddress + m_iCompTeammateColor)
                                if color == 0:
                                    pygame.draw.polygon(screen, triangle_color, [(triangle_top_x, triangle_top_y), (triangle_left_x, triangle_left_y), (triangle_right_x, triangle_right_y)])
                                    pygame.draw.circle(screen, (0, 0, 255), (transformed_x, transformed_y), circle_size)
                                elif color == 1:
                                    pygame.draw.polygon(screen, triangle_color, [(triangle_top_x, triangle_top_y), (triangle_left_x, triangle_left_y), (triangle_right_x, triangle_right_y)])
                                    pygame.draw.circle(screen, (0, 255, 0), (transformed_x, transformed_y), circle_size)
                                elif color == 2:
                                    pygame.draw.polygon(screen, triangle_color, [(triangle_top_x, triangle_top_y), (triangle_left_x, triangle_left_y), (triangle_right_x, triangle_right_y)])
                                    pygame.draw.circle(screen, (255, 255, 0), (transformed_x, transformed_y), circle_size)
                                elif  color == 3:
                                    pygame.draw.polygon(screen, triangle_color, [(triangle_top_x, triangle_top_y), (triangle_left_x, triangle_left_y), (triangle_right_x, triangle_right_y)])
                                    pygame.draw.circle(screen, (255, 106, 2), (transformed_x, transformed_y), circle_size)
                                elif color == 4:
                                    pygame.draw.polygon(screen, triangle_color, [(triangle_top_x, triangle_top_y), (triangle_left_x, triangle_left_y), (triangle_right_x, triangle_right_y)])
                                    pygame.draw.circle(screen, (167, 107, 243), (transformed_x, transformed_y), circle_size)
                                if Hp>30:
                                    text_surface = font.render(f'  {Hp}', True, (0, 255, 0))
                                    text_surface.set_alpha(255)
                                elif Hp<=30:  
                                    text_surface = font.render(f'  {Hp}', True, (255, 0, 0))
                                    text_surface.set_alpha(255)
                                if flash_alpha == 255:
                                    pygame.draw.circle(screen, (255, 255, 255, flash_alpha), (transformed_x, transformed_y), circle_size)
                            elif team != playerTeam: 
                                pygame.draw.polygon(screen, triangle_color, [(triangle_top_x, triangle_top_y), (triangle_left_x, triangle_left_y), (triangle_right_x, triangle_right_y)])
                                pygame.draw.circle(screen, (255, 0, 0), (transformed_x, transformed_y), circle_size)
                                if Hp>30:
                                    text_surface = font.render(f'  {Hp}', True, (0, 255, 0))
                                    text_surface.set_alpha(255)
                                elif Hp<=30:
                                    text_surface = font.render(f'  {Hp}', True, (255, 0, 0))
                                    text_surface.set_alpha(255)
                                if flash_alpha == 255:
                                    pygame.draw.circle(screen, (255, 255, 255, flash_alpha), (transformed_x, transformed_y), circle_size)
                                name = pm.read_string(EntityAddress + m_iszPlayerName)
                                weapon = get_weapon(entity_id)
                                wepname.append((name, weapon))
                        elif teammate_setting == 1:
                            if team == playerTeam:
                                pygame.draw.polygon(screen, triangle_color, [(triangle_top_x, triangle_top_y), (triangle_left_x, triangle_left_y), (triangle_right_x, triangle_right_y)])
                                pygame.draw.circle(screen, (0, 0, 255), (transformed_x, transformed_y), circle_size)
                                if Hp>30:
                                    text_surface = font.render(f'  {Hp}', True, (0, 255, 0))
                                    text_surface.set_alpha(255)
                                elif Hp<=30:  
                                    text_surface = font.render(f'  {Hp}', True, (255, 0, 0))
                                    text_surface.set_alpha(255)
                                if flash_alpha == 255:
                                    pygame.draw.circle(screen, (255, 255, 255, flash_alpha), (transformed_x, transformed_y), circle_size)
                            elif team != playerTeam:
                                pygame.draw.polygon(screen, triangle_color, [(triangle_top_x, triangle_top_y), (triangle_left_x, triangle_left_y), (triangle_right_x, triangle_right_y)])
                                pygame.draw.circle(screen, (255, 0, 0), (transformed_x, transformed_y), circle_size)
                                if Hp>30:
                                    text_surface = font.render(f'  {Hp}', True, (0, 255, 0))
                                    text_surface.set_alpha(255)
                                if Hp<=30:  
                                    text_surface = font.render(f'  {Hp}', True, (255, 0, 0))
                                    text_surface.set_alpha(255)
                                if flash_alpha == 255:
                                    pygame.draw.circle(screen, (255, 255, 255, flash_alpha), (transformed_x, transformed_y), circle_size)
                                name = pm.read_string(EntityAddress + m_iszPlayerName)
                                weapon = get_weapon(entity_id)
                                wepname.append((name, weapon))
                        elif teammate_setting == 0:
                            if entity_id == playerpawn:
                                pygame.draw.polygon(screen, triangle_color, [(triangle_top_x, triangle_top_y), (triangle_left_x, triangle_left_y), (triangle_right_x, triangle_right_y)])
                                pygame.draw.circle(screen, (75, 0, 130), (transformed_x, transformed_y), circle_size)
                                text_surface = font.render(f'  {Hp}', True, (0, 255, 0) if Hp > 30 else (255, 0, 0))
                                screen.blit(text_surface, (transformed_x, transformed_y))
                            elif team == playerTeam:
                                text_surface = font.render(f'  {Hp}', True, (0, 255, 0) if Hp > 30 else (255, 0, 0))
                                text_surface.set_alpha(0)
                                screen.blit(text_surface, (transformed_x, transformed_y))
                            elif team != playerTeam:
                                pygame.draw.polygon(screen, triangle_color, [(triangle_top_x, triangle_top_y), (triangle_left_x, triangle_left_y), (triangle_right_x, triangle_right_y)])
                                pygame.draw.circle(screen, (255, 0, 0), (transformed_x, transformed_y), circle_size)
                                text_surface = font.render(f'  {Hp}', True, (0, 255, 0) if Hp > 30 else (255, 0, 0))
                                screen.blit(text_surface, (transformed_x, transformed_y))
                                name = pm.read_string(EntityAddress + m_iszPlayerName)
                                weapon = get_weapon(entity_id)
                                wepname.append((name, weapon))
                        if isdefusing == 1:
                            hasdefuser = pm.read_bool(EntityAddress + m_bPawnHasDefuser)
                            if hasdefuser:
                                pygame.draw.line(screen, (255, 0, 0), (transformed_x - cross_size, transformed_y - cross_size), (transformed_x + cross_size, transformed_y + cross_size), 2)
                                pygame.draw.line(screen, (255, 0, 0), (transformed_x + cross_size, transformed_y - cross_size), (transformed_x - cross_size, transformed_y + cross_size), 2)
                            else:
                                pygame.draw.line(screen, (0, 255, 0), (transformed_x - cross_size, transformed_y - cross_size), (transformed_x + cross_size, transformed_y + cross_size), 2)
                                pygame.draw.line(screen, (0, 255, 0), (transformed_x + cross_size, transformed_y - cross_size), (transformed_x - cross_size, transformed_y + cross_size), 2)
                    screen.blit(text_surface, (transformed_x, transformed_y))
                except:
                    continue
        except Exception as e:
            print(e)
        screenx = screen_width-200
        screeny = 60
        for name, weapon in wepname:
            stringg = f'{name} | {weapon}'
            text_surfacee = fontt.render(f'{stringg}', True, (255, 255, 255))
            screen.blit(text_surfacee, (screenx, screeny))
            screeny = screeny + 15
        pygame.display.flip()
        
pygame.quit()