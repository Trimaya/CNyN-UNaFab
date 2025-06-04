-- Layer Definition --
LAYER_SEMICONDUCTOR = 0
LAYER_VIA = 1
LAYER_CONTACT = 2
LAYER_PADS = 3

symbol("AlignMarkPrecise",{1,0,0,1,0,140})
parameter("Layer",LAYER_VIA)
parameter("Element",3)

symbol("AlignMarkPrecise",{1,0,0,1,140,140})
parameter("Layer",LAYER_CONTACT)
parameter("Element",3)


symbol("AlignMarkPrecise",{1,0,0,1,280,140})
parameter("Layer",LAYER_PADS)
parameter("Element",3)


symbol("AlignMarkPrecise",{1,0,0,1,0,0})
parameter("Layer",LAYER_VIA)
parameter("Element",1)


symbol("AlignMarkPrecise",{1,0,0,1,140,0})
parameter("Layer",LAYER_CONTACT)
parameter("Element",1)


symbol("AlignMarkPrecise",{1,0,0,1,280,0})
parameter("Layer",LAYER_PADS)
parameter("Element",1)

for x=0,140*4,140 do
    symbol("AlignMarkPrecise",{1,0,0,1,x,0})
    parameter("Element",2)
    parameter("Layer",LAYER_SEMICONDUCTOR)
end
for x=0,140*4,140 do
    symbol("AlignMarkPrecise",{1,0,0,1,x,140})
    parameter("Element",1)
    parameter("Layer",LAYER_SEMICONDUCTOR)
end