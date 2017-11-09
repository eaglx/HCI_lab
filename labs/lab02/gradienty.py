#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import division             # Division in Python 2.7
import matplotlib
matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import math

from matplotlib import colors

def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    #rc('text', usetex=True) 
    #rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400         # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)


    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('my-gradients.pdf')

def designates_colors(rgb_start, rgb_stop, color_num, v):
    # Designates indirect colors between the given.
    width = 1 / (color_num - 1)
    v_new = (v % width) * (color_num - 1)
    r = rgb_start[0] + (rgb_stop[0] - rgb_start[0]) * v_new
    g = rgb_start[1] + (rgb_stop[1] - rgb_start[1]) * v_new
    b = rgb_start[2] + (rgb_stop[2] - rgb_start[2]) * v_new
    return r, g, b

def hsv2rgb(h, s, v):   # (hue, sat, val)
    if v == 0:
        return (0, 0, 0)
    h = h / 60
    section = h // 1
    fraction = h - section
    Mid_odd = v * (1 - (s * fraction))
    Mid_even = v * (1 - s + (s * fraction))
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


def gradient_rgb_bw(v):
    return designates_colors([0,0,0], [1,1,1], 2, v)


def gradient_rgb_gbr(v):
    if v <= 0.5:
        return designates_colors([0,1,0], [0,0,1], 3, v)
    else:
        return designates_colors([0,0,1], [1,0,0], 3, v)


def gradient_rgb_gbr_full(v):
    if v <= 0.25:
        return designates_colors([0,1,0], [0,1,1], 5, v)
    elif v <= 0.5:
        return designates_colors([0,1,1], [0,0,1], 5, v)
    elif v <= 0.75:
        return designates_colors([0,0,1], [1,0,1], 5, v)
    else:
        return designates_colors([1,0,1], [1,0,0], 5, v)


def gradient_rgb_wb_custom(v):
    if v < (1/7):
        return designates_colors([1,1,1],[1,0.0784314,0.576471], 8, v)
    elif v < (2 / 7):
        return designates_colors([1,0.0784314,0.576471], [0,0,1], 8, v)
    elif v < (3 / 7):
        return designates_colors([0,0,1], [0,1,1], 8, v)
    elif v < (4/7):
        return designates_colors([0,1,1],[0,1,0], 8, v)
    elif v < (5/7):
        return designates_colors([0,1,0],[1,1,0], 8, v)
    elif v < (6/7):
        return designates_colors([1,1,0],[1,0,0], 8, v)
    else:
        return designates_colors([1,0,0], [0,0,0], 8, v)


def gradient_hsv_bw(v):
    h, s, v = designates_colors([0,0,0], [0,0,1], 2, v)   
    return hsv2rgb(h, s, v)


def gradient_hsv_gbr(v):
    if v <= 0.5:
        h, s, v = designates_colors([120,1,1], [240,1,1], 3, v)   
    else:
        h, s, v = designates_colors([240,1,1], [360,1,1], 3, v)   
    return hsv2rgb(h, s, v)

def gradient_hsv_unknown(v):
    if v <= 0.5:
        h, s, v = designates_colors([120,0.5,1], [60,0.5,1], 3, v)   
    else:
        h, s, v = designates_colors([60,0.5,1], [0,0.5,1], 3, v)   
    return hsv2rgb(h, s, v)


def gradient_hsv_custom(v):
    h, s, v = designates_colors([0,1,1], [360,0,1], 2, v)   
    return hsv2rgb(h, s, v)


if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])
