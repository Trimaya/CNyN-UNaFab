-- CleWin Parameters --
-- Length
-- Lines
-- Layer Definition --
LAYER_SEMICONDUCTOR = 0
LAYER_VIA = 1
LAYER_CONTACT = 2
LAYER_PADS = 3
-- Function Definiton --
function subdivide (nodes, n)
    new_nodes = {}
    x0 = nodes[1]
    y0 = nodes[2]
    x1 = nodes[3]
    y1 = nodes[4]
    dx = (x1-x0)/n 
    dy = (y1-y0)/n
    x = 0
    y = 0
    for i=1,2*(n+1),2 do
        new_nodes[i] = x + dx*((i-1)/2)
        new_nodes[i+1] = y + dy*((i-1)/2)
    end
    return new_nodes
end

function draw_line (nodes)
    for i=1,#nodes,4 do
        setlayer(LAYER_CONTACT)
        if(i>#nodes-3) then break else
        wire(0,WIRE_WIDTH,{table.unpack(nodes,i,i+3)})
        end
        setlayer(LAYER_SEMICONDUCTOR)
        if(i>#nodes-5) then break else
        wire(0,WIRE_WIDTH,{table.unpack(nodes,i+2,i+5)})
        setlayer(LAYER_VIA)
        circle(nodes[i+2],nodes[i+3],VIA_WIDTH)
        circle(nodes[i+4],nodes[i+5],VIA_WIDTH)
        setlayer(LAYER_SEMICONDUCTOR)
        end
    end
end

function raise_nodes (nodes,delta_y)
    for i=2,#nodes,2 do
        nodes[i] = nodes[i]+delta_y
    end
    return nodes
end

WIRE_WIDTH = 20
VIA_WIDTH = 10/2
LINK_LENGTH = 50
PAD_OFFSET = 5
CHAIN_LENGTH = Length
N = CHAIN_LENGTH/LINK_LENGTH
LINES = Lines

Y_SPACING = 40
nodes = subdivide({0,0,CHAIN_LENGTH,0},N) -- argument 9 subdivides into a table of length 20

for i=1,LINES,1 do
    draw_line(nodes)
    nodes = raise_nodes(nodes,Y_SPACING)
    if i%2 == 0 then
        if i < LINES then
            wire(0,WIRE_WIDTH,{0,nodes[#nodes],0,nodes[#nodes]-Y_SPACING})
        end
    else
        if i < LINES then
            wire(0,WIRE_WIDTH,{nodes[#nodes-1],nodes[#nodes],nodes[#nodes-1],nodes[#nodes]-Y_SPACING})
        end
    end
end

PAD_SIZE = 150

setlayer(LAYER_CONTACT)
rectangle(-PAD_SIZE+WIRE_WIDTH/2,-PAD_SIZE+WIRE_WIDTH/2,WIRE_WIDTH/2,WIRE_WIDTH/2)
rectangle(-PAD_SIZE+WIRE_WIDTH/2,Y_SPACING*(LINES-1)-WIRE_WIDTH/2+PAD_SIZE,WIRE_WIDTH/2,Y_SPACING*(LINES-1)-WIRE_WIDTH/2)

text("Via Chain",{1,0,0,1,20,Y_SPACING*(LINES-1)+20})
setlayer(LAYER_PADS)
rectangle(-PAD_SIZE+WIRE_WIDTH/2+PAD_OFFSET,-PAD_SIZE+WIRE_WIDTH/2+PAD_OFFSET,WIRE_WIDTH/2-PAD_OFFSET,WIRE_WIDTH/2-PAD_OFFSET)
rectangle(-PAD_SIZE+WIRE_WIDTH/2+PAD_OFFSET,Y_SPACING*(LINES-1)-WIRE_WIDTH/2+PAD_SIZE-PAD_OFFSET,WIRE_WIDTH/2-PAD_OFFSET,Y_SPACING*(LINES-1)-WIRE_WIDTH/2+PAD_OFFSET)