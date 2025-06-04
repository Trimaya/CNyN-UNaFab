-- Layer Definition --
LAYER_SEMICONDUCTOR = 0
LAYER_VIA = 1
LAYER_CONTACT = 2
LAYER_PADS = 3

setlayer(Layer)

if Element == 1 then
    rectangle(21,41,81,61)
    rectangle(41,61,61,81)
    rectangle(41,21,61,41)
end
if Element == 2 then
    rectangle(0,0,82,20)
    rectangle(82,0,102,82)
    rectangle(0,20,20,102)
    rectangle(20,82,102,102)
end
if Element == 3 then
    rectangle(21,21,40,40)
    rectangle(21,62,40,81)
    rectangle(62,62,81,81)
    rectangle(62,21,81,40)
end