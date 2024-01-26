import memprocfs
import struct
import time
import leechcorepyc as lc

dwEntityList = 0x17CE6A0
dwLocalPlayerPawn = 0x16D4F48
m_iIDEntIndex = 0x1544
m_iHealth = 0x32C
m_lifeState = 0x330
m_iTeamNum = 0x3BF
m_iszPlayerName = 0x640 # char[128]
m_hPlayerPawn = 0x7EC
m_iPawnArmor = 0x7FC
m_vOldOrigin = 0x1224

vmm = memprocfs.Vmm(['-device', 'fpga'])


cs2 = vmm.process('cs2.exe')


client = cs2.module('client.dll')
client_base = client.base
print(f"[+] Client_base {client_base}")
vmm.close()

device = "FPGA"
leechcore = lc.LeechCore(device)

data = leechcore.read(client_base + dwEntityList, 8)
entList = struct.unpack("<Q", data)[0]
print(f"[+] Entitylist {entList}")

player = struct.unpack("<Q", leechcore.read(client_base + dwLocalPlayerPawn, 8))[0]
print(f"[+] Player {player}")

def getinfo(index):
    EntityENTRY = struct.unpack("<Q", leechcore.read((entList + 0x8 * (index >> 9) + 0x10), 8))[0]
    entity = struct.unpack("<Q", leechcore.read(EntityENTRY + 120 * (index & 0x1FF), 8))[0]

    Hp = struct.unpack("<I", leechcore.read(entity + m_iHealth, 4))[0]
    Armor = struct.unpack("<I", leechcore.read(entity + m_iPawnArmor, 4))[0]
    px = struct.unpack("<f", leechcore.read(entity + m_vOldOrigin +0x4, 4))[0]
    py = struct.unpack("<f", leechcore.read(entity + m_vOldOrigin, 4))[0]
    print(f"[+] ID - {index} | HP - {Hp} | X - {px} | Y - {px}")

def infohandle(index):
    EntityENTRY = struct.unpack("<Q", leechcore.read((entList + 0x8 * (index >> 9) + 0x10), 8))[0]
    entity = struct.unpack("<Q", leechcore.read(EntityENTRY + 120 * (index & 0x1FF), 8))[0]
    while True:
        px = leechcore.read(entity + m_vOldOrigin +0x4, 4)
        print(f"[+] X - {px}")
        time.sleep(0.05)

entitys = []
for entityId in range(1,700):
    EntityENTRY = struct.unpack("<Q", leechcore.read((entList + 0x8 * (entityId >> 9) + 0x10), 8))[0]
    try:
        entity = struct.unpack("<Q", leechcore.read(EntityENTRY + 120 * (entityId & 0x1FF), 8))[0]
        entityHp = struct.unpack("<I", leechcore.read(entity + m_iHealth, 4))[0]
        if int(entityHp) != 0:
            entitys.append(entityId)
        else:
            pass
    except:
        pass

print(entitys)
target = entitys[0]
infohandle(target)
#for index in entitys:
    #getinfo(index)

