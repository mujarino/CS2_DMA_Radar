import memprocfs
import struct
import time

dwEntityList = 0x17CE6A0
dwLocalPlayerPawn = 0x16D4F48
m_iIDEntIndex = 0x1544
m_iHealth = 0x32C
m_angEyeAngles = 0x1518

vmm = memprocfs.Vmm(['-device', 'fpga'])


cs2 = vmm.process('cs2.exe')


client = cs2.module('client.dll')
client_base = client.base
print(f"[+] Client_base {client_base}")

entList = struct.unpack("<Q", cs2.memory.read(client_base + dwEntityList, 8, memprocfs.FLAG_NOCACHE))[0]
print(f"[+] Entitylist {entList}")

player = struct.unpack("<Q", cs2.memory.read(client_base + dwLocalPlayerPawn, 8, memprocfs.FLAG_NOCACHE))[0]
print(f"[+] Player {player}")


while True:
    entityId = struct.unpack("<I", cs2.memory.read(player + m_iIDEntIndex, 4, memprocfs.FLAG_NOCACHE))[0]
    EntityENTRY = struct.unpack("<Q", cs2.memory.read((entList + 0x8 * (entityId >> 9) + 0x10), 8, memprocfs.FLAG_NOCACHE))[0]
    try:
        entity = struct.unpack("<Q", cs2.memory.read(EntityENTRY + 120 * (entityId & 0x1FF), 8, memprocfs.FLAG_NOCACHE))[0]
        entityHp = struct.unpack("<I", cs2.memory.read(entity + m_iHealth, 4, memprocfs.FLAG_NOCACHE))[0]
        EyeAngles = struct.unpack("<Q", cs2.memory.read(entity +(m_angEyeAngles +0x4) , 8, memprocfs.FLAG_NOCACHE))[0]
        print(f"[+] entityId {entityId} | EyeAngles {EyeAngles}")
    except:
        print("вы не смотрите на entity")
    time.sleep(0.1)
