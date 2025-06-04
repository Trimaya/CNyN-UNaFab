-- Layer Definition --
LAYER_SEMICONDUCTOR = 0
LAYER_VIA = 1
LAYER_CONTACT = 2
LAYER_PADS = 3
COL_SPACING = 60000
for i=0,3,1 do
    setlayer(i)
    str = string.format("Mask %d/3",i)
    text(str,{1,0,0,1,0,0})
end