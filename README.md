# CS2 DMA RADAR
Alpha version of my project. Simple using, fast memory reading

![Capture](https://media.discordapp.net/attachments/667075233215414272/1201236851525161091/radarr.gif?ex=65c915ff&is=65b6a0ff&hm=b43eaba24e4afc52969a781ace8393b3b1a65e53b083c916ed212c59a0ad5577&=)
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
- [ ] Logic to draw lower maps for nuke and vertigo.
- [x] SET ANGLE MAP ROTATING
- [x] Draw eye angle
- [x] adjustable sizes of models
- [ ] Automatic parse offsets.
- [x] Automatic map reading.
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
