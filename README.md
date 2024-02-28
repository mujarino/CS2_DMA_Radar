![](https://view-counter.tobyhagan.com/?user={meanwhiletothestars}/{CS2_DMA_Radar})
Simple using, fast memory reading.

![Capture](https://github.com/meanwhiletothestars/CS2_DMA_Radar/blob/main/testing/preview.gif)
**Hit the star and i'll do web version!**

# requirements
1. pcileech DMA Card
2. Second x64 pc with windows or linux(did not testing on macOS)

# if you want to donate me
**Litecoin**
<img src="https://github.com/meanwhiletothestars/CS2_DMA_Radar/blob/main/testing/ltc.jpg" width="210px">

**USDT erc20**
<img src="https://github.com/meanwhiletothestars/CS2_DMA_Radar/blob/main/testing/usdt.jpg" width="210px">

# Install:
1. **Download Release:**
   - Access the latest release on GitHub to get the project files.

2. **Install Python 3:**
   - Ensure you have [Python3](https://www.python.org/downloads/) installed on your system.

3. **Install Dependencies:**
   - Run `pip install -r requirements.txt` to install the required dependencies.

4. **config**
   - teammates: 2: all with colors(only for 5x5 or 2x2). 1: all with blue and red colors(for another game modes). 0: teammates off(visibility only local player and enemies)
   - altgirlpic_instead_nomappic: takes random png picture from data\nomap_pics instead of nomap picture
     
6. **Open CS2:**
   - Launch CS2.

7. **Start app.py in any time:**
   - On Linux: Launch the match with `sudo python app.py`.
   - On Windows: Execute the appropriate command to start the match `python.exe ./app.py`.

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
   - [ ] ...
- [ ] websocket radar
   - [ ] alpha version
   - [ ] angle map rotating
   - [ ] adjustable sizes from gui
   - [ ] player-angle rotation
   - [ ] mobile optimization
   - [ ] access from external ip-address

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


# How to add your map?
   1. download offsetfinder.py
   2. make folder in /maps with your mapname
   3. copy meta.json from one of other maps. to work properly it needs 2 files in folder: radar.png and meta.json
   4. run offset finder with python
   5. numbers in console is player position in program. so u need to make it positive(if its negative) with plus and minus, x,y
   6. use buttons to search current offset
   7. enter new numbers in meta.json
   8. you can open issue and send me this data and i will add your map for all

