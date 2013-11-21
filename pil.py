#!/usr/bin/env python

import os, sys
import Tkinter
from Tkinter import *
import Image, ImageTk
import tkFont

def get_dimensions(image, max_width, max_height):
    original_width = image.size[0]
    original_height = image.size[1]
    max_ratio = (1.0*max_width)/(1.0*max_height)
    original_ratio = (1.0*original_width)/(1.0*original_height)
    if (original_ratio > max_ratio):
        # width is the limiting dimension
        # resize so the width is at the max
        scale_down = (1.0*max_width)/(1.0*original_width)
        return original_width * scale_down, original_height*scale_down
    else:
        # height is the limiting dimension (or it's exactly the right ratio)
        # resize so the height is at the max
        scale_down = (1.0*max_height)/(1.0*original_height)
        return original_width * scale_down, original_height*scale_down

def get_resized_image(image, max_width, max_height, enlarge=True):
    width, height = get_dimensions(image, max_width, max_height)
    print "width = " + str(width)
    print "height = " + str(height)
    if (not enlarge and max_width > image.size[0]):
        return image
    width = int(width)
    height = int(height)
    return image.resize((width, height), Image.ANTIALIAS)

def button_click_exit_mainloop (event):
    event.widget.quit() # this will cause mainloop to unblock.

root = Tkinter.Tk()
root.bind("<Button>", button_click_exit_mainloop)
root.geometry('+%d+%d' % (100,100))
dirlist = os.listdir('.')
old_label_image = None
for f in dirlist:
    print f
    width = 1000
    height = 1000
    try:
        image1 = Image.open(f)
        image1 = get_resized_image(image1, width, height, enlarge=False)
        root.geometry('%dx%d' % (width, height))
        tkpi = ImageTk.PhotoImage(image1)
        label_image = Tkinter.Label(root, image=tkpi)
        label_image.place(x=0,y=0,width=image1.size[0],height=image1.size[1])
        root.title(f)
        if old_label_image is not None:
            old_label_image.destroy()
        old_label_image = label_image
        root.mainloop()
    except Exception, e:
        print e
        pass
