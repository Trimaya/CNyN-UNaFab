-- CleWin Parameters --
-- Size -- Size of capacitor
-- MIS -- 1=true 0=false
-- Pads -- 1=true 0=false

-- Layer Definition --
LAYER_SEMICONDUCTOR = 0
LAYER_VIA = 1
LAYER_CONTACT = 2
LAYER_PADS = 3
VIA_BORDER = 5
CONTACT_BORDER = 10
WIRE_WIDTH = 20
CONTACTPAD_Y = 400
CONTACTPAD_SIZE = 150
PAD_OFFSET = 5

-- Convert numbers to booleans --
if MIS == 0 then
    MIS = false
else
    MIS = true
end
if Pads == 0 then
    Pads = false
else
    Pads = true
end


setlayer(LAYER_VIA)
rectangle(0,0,Size,-Size)
setlayer(LAYER_CONTACT)
rectangle(0-VIA_BORDER,VIA_BORDER,Size+VIA_BORDER,-Size-VIA_BORDER)
if MIS == true then
    setlayer(LAYER_SEMICONDUCTOR)
    rectangle(0-VIA_BORDER-CONTACT_BORDER,VIA_BORDER+CONTACT_BORDER,Size+VIA_BORDER+CONTACT_BORDER,-Size-VIA_BORDER-CONTACT_BORDER)
end
if Pads == true then
    setlayer(LAYER_CONTACT)
    wire(0,WIRE_WIDTH,{Size/2,-Size/2,Size/2,-CONTACTPAD_Y})
    rectangle(Size/2-CONTACTPAD_SIZE/2,-CONTACTPAD_Y-CONTACTPAD_SIZE,Size/2+CONTACTPAD_SIZE/2,-CONTACTPAD_Y)
    setlayer(LAYER_PADS)
    rectangle(Size/2-CONTACTPAD_SIZE/2+PAD_OFFSET,-CONTACTPAD_Y-CONTACTPAD_SIZE+PAD_OFFSET,Size/2+CONTACTPAD_SIZE/2-PAD_OFFSET,-CONTACTPAD_Y-PAD_OFFSET)
end
setlayer(LAYER_CONTACT)
str = string.format("%d",Size)
text(str,{1,0,0,1,Size/2-CONTACTPAD_SIZE/2-33,25})


