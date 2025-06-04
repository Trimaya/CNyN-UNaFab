WIDTHS = {20,40,80,120,160,200}
LENGTHS = {10,20,40,60,80,110,150,200}
W = 900
H = 700
x = 0                 
y = 0
for i = 1, #WIDTHS do
    for j = 1, #LENGTHS do
        symbol("MOSFET",{1,0,0,1,x,y})
        parameter("CLength",LENGTHS[j])
        parameter("CWidth",WIDTHS[i])
        x = x + W
    end
    y = y + H
    -- x = -L_INCREMENT/2*i
    x = 0
end