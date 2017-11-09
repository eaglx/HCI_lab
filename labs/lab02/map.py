#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import division
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import math

def designates_colors(rgb_start, rgb_stop, v):
    # Designates indirect colors between the given.
    r = rgb_start[0] + (rgb_stop[0] - rgb_start[0]) * v
    g = rgb_start[1] + (rgb_stop[1] - rgb_start[1]) * v
    b = rgb_start[2] + (rgb_stop[2] - rgb_start[2]) * v
    return r, g, b

def hsv2rgb(h, s, v):   # (hue, sat, val)
    if v == 0:
        return (0, 0, 0)
    h = h / 60
    section = h // 1
    fraction = h - section
    Mid_odd = v * (1-(s*fraction))
    Mid_even = v * (1-s+(s*fraction))
    m = v - v*s # m - amount to match value
    if section == 0:
        return v, Mid_even, m
    elif section == 1:
        return Mid_odd, v, m
    elif section == 2:
        return m, v, Mid_even
    elif section == 3:
        return m, Mid_odd, v
    elif section == 4:
        return Mid_even, m, v
    elif section == 5:
        return v, m, Mid_odd
    return (0, 0, 0)

def upload_data(file_name):    
    with open(file_name,'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    
    array = []
    for idx, val in enumerate(data):
        ival = ' '.join(val.split())
        if idx == 0:
            width = int(ival.split(' ')[0])
            height = int(ival.split(' ')[1])
            distance = int(ival.split(' ')[2])
        else:
            temp = []
            for i in range(width):
                temp.append(float(ival.split(' ')[i]))
            array.append(temp)
        
    return (width, height, array)

def data_cast(data, height, width):
    # Cast value to be between 0..1
    minimum = min([min(row) for row in data])
    maximum = max([max(row) for row in data])
    
    for row in range(height):
        for element in range(width):
            data[row][element] = (data[row][element] - minimum) / (maximum - minimum)

def shadow(s, v, first_height, second_height):
    v += (second_height - first_height) * 5.0
    s -= (second_height - first_height) * 15.0
    
    if(v < 0):
        v = 0
    elif(v > 1):
        v = 1.0
    
    if(s < 0):
        s = 0
    elif(s > 1):
        s = 1
        
    return s, v

def color(data, hsv_low, hsv_high, sun_pos):    
    height = len(data)
    width = len(data[0])
    array = np.zeros((height, width, 3))
    
    data_cast(data, height, width)
    
    for i in range(height - 1):
        for j in range(width - 1):
            h, s, v = designates_colors(hsv_low, hsv_high, data[i][j])
            v -= 0.1
            if(j != 0):
                s, v = shadow(s, v, data[i][j - 1], data[i][j])
            array[i][j] = hsv2rgb(h, s, v)

    return array
    

if __name__ == '__main__':
    rc('legend', fontsize=10)
    fig = plt.figure()
    
    width, height, data = upload_data('big.dem')
    plt.imshow(color(data, [120,1,1], [0,1,1], [0.12, 0.0, 1.0]), shape = (width, height, 3), aspect = 'auto')
        
    fig.savefig('my-map.pdf')
