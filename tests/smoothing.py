import math


current_pos = 0
last_pos = 0
speed_ms = 56789

weird_u = 0
weird_o = 1

def dichte(x):
    res = 1/math.sqrt(2*math.pi*weird_o) * math.exp(-0.5 * ( x - weird_u / weird_o)**2)
    print(res)


dichte(speed_ms)