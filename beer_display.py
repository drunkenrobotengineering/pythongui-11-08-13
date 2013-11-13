#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter
import tkFont
import time
import serial
from lib.arduino_io import arduino

class beer_display(Tkinter.Tk):

    def get_beer_consumed(self):
        # This is for testing.  Eventually this'll use self.arduino, but that only works if it actually has an arduino connected.
        drink_info = self.arduino.read_drink_info_from_serial()
        self.beer_1_consumed = round(drink_info["1"]["c"] * .033814, 2)
        self.beer_2_consumed = round(drink_info["2"]["c"] * .033814, 2)
        return self.beer_1_consumed, self.beer_2_consumed

    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.arduino = arduino()
        self.parent = parent
        # The following two lines are for testing
        # Eventually this'll come from an on-disk file or AWS
        self.beer_1_consumed = 0
        self.beer_2_consumed = 0
        self.initialize()

    def initialize(self):
        self.grid()
        # The current UI kinda sucks, but it has all the initial elements.
        # It'll be made prettier later.
        helv36bold = tkFont.Font(family="Helvetica", size=36, weight="bold")
        helv18 = tkFont.Font(family="Helvetica", size=18)
        helv24 = tkFont.Font(family="Helvetica", size=24)
        helv36 = tkFont.Font(family="Helvetica", size=36)
        wraplength = 600

        nameFont = helv36bold
        descriptionFont = helv24
        abvFont = helv18
        consumedFont = helv18

        # overall layout:
        # beer label 1 (name1)              | beer label 2 (name2)
        # beer description 1 (description1) | beer description 2 (description2)
        # beer ABV 1 (abv1)                 | beer ABV 2 (abv2)
        # amount consumed 1 (consumed1)     | amount consumed 2 (consumed2)
        self.nameVar1 = Tkinter.StringVar()
        self.descriptionVar1 = Tkinter.StringVar()
        self.abvVar1 = Tkinter.StringVar()
        self.consumedVar1 = Tkinter.StringVar()
        self.nameVar2 = Tkinter.StringVar()
        self.descriptionVar2 = Tkinter.StringVar()
        self.abvVar2 = Tkinter.StringVar()
        self.consumedVar2 = Tkinter.StringVar()

        background = "light gray"
        foreground = "black"
        self.configure(background=background)
        nameLabel1 = Tkinter.Label(self,textvariable=self.nameVar1,
                              anchor="w",fg=foreground,bg=background, font=nameFont, wraplength=wraplength)
        descriptionLabel1 = Tkinter.Label(self,textvariable=self.descriptionVar1,
                              anchor="w",fg=foreground,bg=background, font=descriptionFont, wraplength=wraplength)
        abvLabel1 = Tkinter.Label(self,textvariable=self.abvVar1,
                              anchor="w",fg=foreground,bg=background, font=abvFont, wraplength=wraplength)
        consumedLabel1 = Tkinter.Label(self,textvariable=self.consumedVar1,
                              anchor="w",fg=foreground,bg=background, font=consumedFont, wraplength=wraplength)
        nameLabel2 = Tkinter.Label(self,textvariable=self.nameVar2,
                              anchor="w",fg=foreground,bg=background, font=nameFont, wraplength=wraplength)
        descriptionLabel2 = Tkinter.Label(self,textvariable=self.descriptionVar2,
                              anchor="w",fg=foreground,bg=background, font=descriptionFont, wraplength=wraplength)
        abvLabel2 = Tkinter.Label(self,textvariable=self.abvVar2,
                              anchor="w",fg=foreground,bg=background, font=abvFont, wraplength=wraplength)
        consumedLabel2 = Tkinter.Label(self,textvariable=self.consumedVar2,
                              anchor="w",fg=foreground,bg=background, font=consumedFont, wraplength=wraplength)

        nameLabel1.grid(column=0,row=0,columnspan=1)
        descriptionLabel1.grid(column=0,row=1,columnspan=1)
        abvLabel1.grid(column=0,row=2,columnspan=1)
        consumedLabel1.grid(column=0,row=3,columnspan=1)
        nameLabel2.grid(column=1,row=0,columnspan=1)
        descriptionLabel2.grid(column=1,row=1,columnspan=1)
        abvLabel2.grid(column=1,row=2,columnspan=1)
        consumedLabel2.grid(column=1,row=3,columnspan=1)

        self.nameVar1.set("Chocolate Rain")
        self.descriptionVar1.set("A rich and creamy milk stout with notes of chocolate, vanilla, and coffee.  Warning: contains a shit-ton of lactose.")
        self.abvVar1.set("5.0% ABV")
        self.nameVar2.set("SeattAle")
        self.descriptionVar2.set("A crisp and refreshing fruit ale made with hops and raspberries from Seattle and honey from Central Washington State.")
        self.abvVar2.set("4.5% ABV")
        self.update_consumed_values()

        self.grid_columnconfigure(0,weight=2, pad=25)
        self.grid_columnconfigure(1,weight=2, pad=25)
        self.grid_rowconfigure(0,weight=2, pad=10)
        self.grid_rowconfigure(1,weight=2, pad=10)
        self.grid_rowconfigure(2,weight=1, pad=10)
        self.grid_rowconfigure(3,weight=1, pad=10)

        self.resizable(True,False)
        self.update()

    def update_consumed_values(self):
        one, two = self.get_beer_consumed()
        self.consumedVar1.set(str(one) + " oz. drunk")
        self.consumedVar2.set(str(two) + " oz. drunk")

    def update_consumed_values_loop(self):
        self.update_consumed_values()
        self.after(2000, self.update_consumed_values_loop)

if __name__ == "__main__":
    app = beer_display(None)
    app.title('Beer Display')
    app.update_consumed_values_loop()
    app.mainloop()
