-- Layer Definition --
LAYER_SEMICONDUCTOR = 0
LAYER_VIA = 1
LAYER_CONTACT = 2
LAYER_PADS = 3

setlayer(Layer)

if Element == 1 then
    rectangle(0,0,3700,200)
    rectangle(0,700,3700,900)
    rectangle(0,200,200,700)
    rectangle(700,200,900,700)
    rectangle(1400,200,1600,700)
    rectangle(2100,200,2300,700)
    rectangle(2800,200,3000,700)
    rectangle(3500,200,3700,700)
end
if Element == 2 then
    rectangle(205,205,695,695)
end
if Element == 3 then
    rectangle(905,205,1395,695)
end
if Element == 4 then
    rectangle(1605,205,2095,695)
end
if Element == 5 then
    rectangle(2305,205,2695,695)
end
if Element == 6 then
    rectangle(3005,205,3495,695)
end