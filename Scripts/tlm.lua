-- Layer Definition --
LAYER_SEMICONDUCTOR = 0
LAYER_VIA = 1
LAYER_CONTACT = 2
LAYER_PADS = 3

WIRE_WIDTH = 10
PAD_OFFSET = 5
VIA_WIDTH = 6
LENGTH = 400
HEIGHT = Height
PAD_SIZE = 100
SEPARATIONS = {10,20,40,60,80,100}
DISTANCES = {}
sum = 0
for i=1,#SEPARATIONS,1 do
    sum = sum + SEPARATIONS[i] + VIA_WIDTH
    DISTANCES[i] = sum
end

setlayer(LAYER_SEMICONDUCTOR)
rectangle(-20,0,LENGTH-20,HEIGHT)


setlayer(LAYER_VIA)
wire(0,VIA_WIDTH,{0,-5,0,HEIGHT+5})
for i=1,#DISTANCES,1 do
    wire(0,VIA_WIDTH,{DISTANCES[i],-5,DISTANCES[i],HEIGHT+5})
end


setlayer(LAYER_CONTACT)
wire(0,WIRE_WIDTH,{0,-5,0,HEIGHT+70})
for i=1,#DISTANCES,2 do
    wire(0,WIRE_WIDTH,{DISTANCES[i],-70,DISTANCES[i],HEIGHT+10})
end
for i=2,#DISTANCES,2 do
    wire(0,WIRE_WIDTH,{DISTANCES[i],-10,DISTANCES[i],HEIGHT+70})
end

setlayer(LAYER_CONTACT)
left = WIRE_WIDTH/2-PAD_SIZE/2
right = PAD_SIZE/2-WIRE_WIDTH/2
PAD_POSX = {0+left,16+left, 42+right, 88+right, 154+right, 240+right, 346}
PAD_POSY = {70+PAD_SIZE+HEIGHT, -70, 70+PAD_SIZE+HEIGHT, -70, 70+PAD_SIZE+HEIGHT, -70, 70+PAD_SIZE+HEIGHT}
setlayer(LAYER_CONTACT)
for i=1,#PAD_POSX,1 do
    setlayer(LAYER_CONTACT)
    rectangle(PAD_POSX[i]-PAD_SIZE/2,PAD_POSY[i]-PAD_SIZE,PAD_POSX[i]+PAD_SIZE/2,PAD_POSY[i])
    setlayer(LAYER_PADS)
    rectangle(PAD_POSX[i]-PAD_SIZE/2+PAD_OFFSET,PAD_POSY[i]-PAD_SIZE+PAD_OFFSET,PAD_POSX[i]+PAD_SIZE/2-PAD_OFFSET,PAD_POSY[i]-PAD_OFFSET)
end

setlayer(LAYER_CONTACT)
str = string.format("W%dum",Height)
text(str,{1,0,0,1,0,-PAD_SIZE-200})