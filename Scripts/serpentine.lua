-- CleWin Parameters --
-- Length
-- Rows
LENGTH = Length --1000
WIDTH = 10
ROW_SPACING = 3*WIDTH
PAD_SIZE = 150
ROWS = Rows --20
MID_PAD_OFFSET = 50
LAYER_PADS = 3
LAYER_CONTACT = 2
PAD_OFFSET = 5
setlayer(LAYER_CONTACT)
x = 0
y = 0
nodes = {}
for i=1,10*ROWS/2,10 do
    --Node 1
    x = 0; y = y;
    nodes[i] = x
    nodes[i+1] = y
    -- Node 2
    x = LENGTH; y = y;
    nodes[i+2] = x
    nodes[i+3] = y
    -- Node 3
    x = x; y = y + ROW_SPACING;
    nodes[i+4] = x
    nodes[i+5] = y
    -- Node 4
    x = 0; y = y;      
    nodes[i+6] = x
    nodes[i+7] = y
    -- Node 5 -- only if not last ROW
    if i ~= 1+10*(ROWS/2-1) then
        x = 0; y = y + ROW_SPACING;
        nodes[i+8] = x
        nodes[i+9] = y
    else
        break
    end
end
wire(0,WIDTH,nodes)
rectangle(-PAD_SIZE+WIDTH/2-MID_PAD_OFFSET,-PAD_SIZE/2,0+WIDTH/2-MID_PAD_OFFSET,PAD_SIZE/2)
rectangle(-PAD_SIZE+WIDTH/2-MID_PAD_OFFSET,y+PAD_SIZE/2,0+WIDTH/2-MID_PAD_OFFSET,y-PAD_SIZE/2)      
wire(0,WIDTH,{-MID_PAD_OFFSET,0,0,0})
wire(0,WIDTH,{-MID_PAD_OFFSET,y,0,y})


str = string.format("%d×%dum",ROWS,LENGTH)
text(str,{1,0,0,1,10,-PAD_SIZE+WIDTH/2+20})
text("Serpentine",{1,0,0,1,10,y+20})
setlayer(LAYER_PADS)
rectangle(-PAD_SIZE+WIDTH/2+PAD_OFFSET-MID_PAD_OFFSET,-PAD_SIZE/2+PAD_OFFSET,0+WIDTH/2-PAD_OFFSET-MID_PAD_OFFSET,PAD_SIZE/2-PAD_OFFSET)
rectangle(-PAD_SIZE+WIDTH/2+PAD_OFFSET-MID_PAD_OFFSET,y+PAD_SIZE/2-PAD_OFFSET,0+WIDTH/2-PAD_OFFSET-MID_PAD_OFFSET,y-PAD_SIZE/2+PAD_OFFSET)


MID_PAD_LOCATIONS = {}
for i=1,ROWS/10-1 do
    MID_PAD_LOCATIONS[i] = 10*(i-1)+9
end
-- MID_PAD_LOCATIONS = {9,19,29,39,49}


for i=1,#MID_PAD_LOCATIONS,1 do
    setlayer(LAYER_CONTACT)
    y = MID_PAD_LOCATIONS[i]*ROW_SPACING
    rectangle(-PAD_SIZE+WIDTH/2-MID_PAD_OFFSET,y+PAD_SIZE/2+ROW_SPACING/2,0+WIDTH/2-MID_PAD_OFFSET,y-PAD_SIZE/2+ROW_SPACING/2)
    wire(0,WIDTH,{0+WIDTH/2-MID_PAD_OFFSET,y+ROW_SPACING/2,0,y+ROW_SPACING/2})
    -- text(string.format("%d",MID_PAD_LOCATIONS[i]+1),{1,0,0,1,-PAD_SIZE+WIDTH/2-MID_PAD_OFFSET-200,y-50})
    text(string.format("%d",MID_PAD_LOCATIONS[i]+1),{1,0,0,1,-PAD_SIZE+WIDTH/2-MID_PAD_OFFSET,y+PAD_SIZE/2+ROW_SPACING/2+10})
    setlayer(LAYER_PADS)
    rectangle(-PAD_SIZE+WIDTH/2-MID_PAD_OFFSET+PAD_OFFSET,y+PAD_SIZE/2+ROW_SPACING/2-PAD_OFFSET,0+WIDTH/2-MID_PAD_OFFSET-PAD_OFFSET,y-PAD_SIZE/2+ROW_SPACING/2+PAD_OFFSET)
end