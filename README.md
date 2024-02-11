# CS2 DMA RADAR
Beta version of my project. Simple using, fast memory reading.

![Capture](https://github.com/meanwhiletothestars/CS2_DMA_Radar/blob/main/testing/preview.gif)
# requirements
1. pcileech DMA Card
2. Second x64 pc with windows or linux(did not testing on macOS)
# install
1. Download release
2. Install python 3
3. Install dependencies with ```pip install -r requirements.txt```
4. Open cs2 and connect to the map
5. Start on match starts with ```sudo python app.py```

# TODO
- [x] pygame radar
   - [x] Logic to draw lower maps for nuke and vertigo.
   - [x] SET ANGLE MAP ROTATING
   - [x] Draw eye angle
   - [x] adjustable sizes of models
   - [ ] Automatic parse offsets.
   - [x] Automatic map reading.
   - [ ] Bomb/kits drawing.
   - [ ] Tutorial for add maps.
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

![](https://view-counter.tobyhagan.com/?user={meanwhiletothestars}/{CS2_DMA_Radar})
