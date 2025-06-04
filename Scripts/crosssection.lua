-- Layer Definition --
LAYER_SEMICONDUCTOR = 0
LAYER_VIA = 1
LAYER_CONTACT = 2

LENGTH = 1900 -- has to be multiple of 95
WIDTH = 760 -- has to be multiple of 95

setlayer(LAYER_SEMICONDUCTOR)
rectangle(0,0,LENGTH,WIDTH)
for i=1,WIDTH/95-1,1 do
    rectangle(-80,i*95-15,LENGTH+80,i*95)
end
for i=1,LENGTH/95-1,1 do
    rectangle(i*95-15,-80,i*95,WIDTH+80)
end
setlayer(LAYER_VIA)
for i=1,WIDTH/95-1,1 do
    rectangle(-50,i*95-10,LENGTH+50,i*95-5)
end
for i=1,LENGTH/95-1,1 do
    rectangle(i*95-10,-50,i*95-5,WIDTH+50)
end

