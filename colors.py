'''
Created on 11-11-2011

@author: luke
'''
def get_color(x):
    p = x * 3.0
    if x <= 1.0 / 3.0:
        return mix_color((0, 0, 255), (0, 255, 0), p)
    elif x <= 2.0 / 3.0:
        return mix_color((0, 255, 0), (255, 0, 0), p)
    else:
        return mix_color((255, 0, 0), (0, 0, 255), p)

def mix_color(c1, c2, p):
    while p > 1.0:
        p -= 1.0   
    red = green = blue = 0 
    if p < 0.5:
        red = c1[0] + c2[0] * p * 2
        green = c1[1] + c2[1] * p * 2
        blue = c1[2] + c2[2] * p * 2
    else:
        red = c1[0] * (1 - 2 * (p - 0.5)) + c2[0]
        green = c1[1] * (1 - 2 * (p - 0.5)) + c2[1]
        blue = c1[2] * (1 - 2 * (p - 0.5)) + c2[2]
    return (int(red), int(green), int(blue))
