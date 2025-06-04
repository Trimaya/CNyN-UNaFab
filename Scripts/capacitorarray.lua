sizes = {100, 150, 200, 250, 300, 350}
x = 0
y = 0
X_SPACING = 200
for i = 1,#sizes,1 do
    symbol("Capacitor",{1,0,0,1,x,y})
    parameter("Size",sizes[i])
    parameter("MIS",1)
    parameter("Pads",1)
    x = x + sizes[i]+ X_SPACING
end
x = x + 200
for i = 1,#sizes,1 do
    -- symbol("Capacitor",{1,0,0,1,x,y})
    -- parameter("Size",sizes[i])
    -- parameter("MIS",1)
    -- parameter("Pads",0)
    x = x + sizes[i]+ X_SPACING
end
y = y + 1000
x = 0
for i = 1,#sizes,1 do
    symbol("Capacitor",{1,0,0,1,x,y})
    parameter("Size",sizes[i])
    parameter("MIS",0)
    parameter("Pads",1)
    x = x + sizes[i]+X_SPACING
end
x = x + 200
for i = 1,#sizes,1 do
    -- symbol("Capacitor",{1,0,0,1,x,y})
    -- parameter("Size",sizes[i])
    -- parameter("MIS",0)
    -- parameter("Pads",0)
    x = x + sizes[i]+X_SPACING
end