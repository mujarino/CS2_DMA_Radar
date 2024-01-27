# CS2 DMA RADAR
Alpha version of my project. Simple using, fast mem reading

# requirements
1. pcileech DMA Card
2. Second x64 pc
# install
1. Download release
2. Install python 3
3. Install dependencies(memprocfs,pygame,pygame_gui)
4. Change map in map.txt
5. Open csgo and connect to the map
6. Start on first round freezetime with /python main.py

# TODO
- [x] Draw eye angle
- [ ] Automatic parse offsets.
- [ ] Automatic map reading.
- [ ] Bomb/kits drawing.
- [ ] Tutorial for add maps.
- [ ] ...
- [ ] websocket optional

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
