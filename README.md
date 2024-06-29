[![ac status - Undetected](https://img.shields.io/static/v1?label=ac+status&message=Undetected&color=2ea44f)](https://) [![tested-cs2-version. - 14014](https://img.shields.io/static/v1?label=tested+cs2+version&message=14011&color=2ea44f)](https://)


![Capture](https://github.com/meanwhiletothestars/CS2_DMA_Radar/blob/DMA/testing/preview.gif)

I doing this project for myself and make this github page public. U can only give me star or crypto donate to make me happy. This project will be free and up do date as long as i will be motivated to do it - **Hit the star**


![](https://view-counter.tobyhagan.com/?user={meanwhiletothestars}/{CS2_DMA_Radar}) [![GitHub release](https://img.shields.io/github/release/meanwhiletothestars/CS2_DMA_Radar?include_prereleases=&sort=semver&color=blue)](https://github.com/meanwhiletothestars/CS2_DMA_Radar/releases/) [![issues - CS2_DMA_Radar](https://img.shields.io/github/issues/meanwhiletothestars/CS2_DMA_Radar)](https://github.com/meanwhiletothestars/CS2_DMA_Radar/issues)

# Is DMA Undetected?
Detecting probability demands only on your dma firmware


**VAC** - Unreal to detect on any firmware

**EAC/GAMEGUARD/any A-tier AC that startup after windows** - If SOME not default firmware - Unreal to detect
**There is a lot of EAC versions and some can be very good in dma protect**

**Faceit AC** - If good 1:1 firmware - 99% not detect


# Is External Undetected?
**VAC** - 99,99% Unreal to detect on any firmware

**EAC/GAMEGUARD/any A-tier AC that startup after windows** - EAC not detect/other - didn't tested

**Faceit AC** - Dont use it on Faceit pls, insta ban probably


# Requirements FOR DMA:
1. pcileech DMA Card
2. Second x64 pc with windows or linux(did not testing on macOS)

# Install:
1. **Download Release:**
   - Access the latest [Release](https://github.com/meanwhiletothestars/CS2_DMA_Radar/releases) on GitHub to get the project files.

2. **Install Python 3:**
   - Ensure you have [Python3](https://www.python.org/downloads/) installed on your system.

3. **Install Dependencies:**
   - Run `pip install -r requirements.txt` to install the required dependencies.
   - **WARNING**  INSTALL pygame and pygame-gui manually by - **pip install pygame** AND **pip install pygame-gui**

4. **config**
   - teammates: 2: all with colors(only for 5x5 or 2x2). 1: all with blue and red colors(for another game modes). 0: teammates off(visibility only local player and enemies)
   - altgirlpic_instead_nomappic: takes random png picture from data\nomap_pics instead of nomap picture
   - update_offsets: 1 - update automatic with internet. 0: - place client and offsets manually
   - maxclients: max clients. on default it will be 10 players. Dont change if u dont know what u doing
     
6. **Open CS2:**
   - Launch CS2.

7. **Start app.py in any time:**
   - On Linux: Launch after cs2 startup with `sudo python app.py`.
   - On Windows: Execute the appropriate command after cs2 startup to start  `python.exe ./app.py`.
  
# if you want to donate me
**Litecoin**
<img src="https://github.com/meanwhiletothestars/CS2_DMA_Radar/blob/DMA/testing/ltc.jpg" width="210px">

**USDT erc20**
<img src="https://github.com/meanwhiletothestars/CS2_DMA_Radar/blob/DMA/testing/usdt.jpg" width="210px">

**TON**
<img src="https://github.com/meanwhiletothestars/CS2_DMA_Radar/blob/DMA/testing/ton.jpg" width="210px">

# TODO
- [x] pygame radar
   - [x] Logic to draw lower maps for nuke and vertigo.
   - [x] SET ANGLE MAP ROTATING
   - [x] Draw eye angle
   - [x] adjustable sizes of models
   - [x] Automatic parse offsets.
   - [x] Automatic map reading.
   - [x] defuse drawing.
   - [x] Tutorial for add maps.
   - [x] Guns(in external)
- [x] websocket radar(not public for now)
   - [x] alpha version
   - [x] adjustable sizes from gui
   - [x] mobile optimization
   - [x] access from external ip-address
   - [x] same functionality like in pygame version
   - [x] guns
   - [x] hp with progress bar
   - [x] advanced config
   - [ ] is enemy spoted
   - [ ] custom link for any client, so it can be reached from private IP(without port open and static ip)
   - [x] bomb
   - [x] kits
   - [x] money on frezetime
   - [ ] done

# TROUBLESHOOTING
1. download binaries from https://github.com/ufrisk/pcileech
2. start dma test with
```
sudo ./pcileech -device fpga probe
```
(1-8% loss is normal)

3. if test isn't working there is couple of things u can do

   a) try another windows version(downgrade for 21h2 for example)
   
   b) try to buy other dma firmware

4. If u use without A/C and it works, then try with AC and have problems - BUY BETTER FIRMWARE. This radar works on libraries that use 100% of dma cheats and only DECRYPTYNG memory. SO there is no chance to fix AC Problems of it because bypass ac is FIRMWARE TASK

P.S. If cheat works great without any anti-cheat and stop working when u start anti-cheat - then u need to buy better dma firmware. This is not my cheat issue

# How to add your map?
   1. download testing/offset_manipulator.py
   2. make folder in /maps with your mapname
   3. copy meta.json from one of other maps. to work properly it needs 2 files in folder: radar.png and meta.json
   4. run offset finder with python
   5. numbers in console is player position in program. so u need to make it positive(if its negative) with plus and minus, x,y
   6. use buttons to search current offset
   7. enter new numbers in meta.json
   8. if ur map with split, use meta.json from nuke or vertigo and add ur mapname in maps_with_split
   9. you can open issue and send me this data and i will add your map for all

