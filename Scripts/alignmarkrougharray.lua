-- Layer Definition --
LAYER_SEMICONDUCTOR = 0
LAYER_VIA = 1
LAYER_CONTACT = 2
LAYER_PADS = 3

symbol("AlignMarkRough",{1,0,0,1,0,0})
parameter("Element",1)
parameter("Layer",LAYER_SEMICONDUCTOR)

symbol("AlignMarkRough",{1,0,0,1,0,0})
parameter("Element",2)
parameter("Layer",LAYER_VIA)

symbol("AlignMarkRough",{1,0,0,1,0,0})
parameter("Element",3)
parameter("Layer",LAYER_CONTACT)

symbol("AlignMarkRough",{1,0,0,1,0,0})
parameter("Element",4)
parameter("Layer",LAYER_PADS)