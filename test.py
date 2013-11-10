#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# Some code I pulled from a website to learn the basics of tkinter.
# I don't remember which site in particular, but if you google python gui guide you'll probably find it.
# Code is frmo them, I added the comments to familiarize myself with it

import Tkinter

class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        # Initializes tkinter
        self.grid()

        # Make a String object to display in an entry field
        self.entryVariable = Tkinter.StringVar()
        # Make the tkinter entry field with the above object as the displayed text
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        # Set location and behavior of the field
        self.entry.grid(column=0,row=0,sticky='EW')
        # Add an action to the Enter button inside the entry field
        self.entry.bind("<Return>", self.OnPressEnter)
        # Set the value of the displayed text
        self.entryVariable.set(u"Enter text here.")

        # Make a button object
        # Set the text and set the method that gets called when it gets clicked
        button = Tkinter.Button(self,text=u"Click me !",
                                command=self.OnButtonClick)
        # Set the location of the button
        button.grid(column=1,row=0)

        # Make a string object to display in a label
        self.labelVariable = Tkinter.StringVar()
        # Make a label with the above object as the displayed text
        # Set its colors and displayed value
        label = Tkinter.Label(self,textvariable=self.labelVariable,
                              anchor="w",fg="white",bg="blue")
        # Set the label's location and behavior
        label.grid(column=0,row=1,columnspan=2,sticky='EW')
        # Set the label's display value
        self.labelVariable.set(u"Hello !")

        # In the grid, set the value of option "weight" is 1 in column 0
        self.grid_columnconfigure(0,weight=1)
        # Sets resizability of width (true) and height (false)
        self.resizable(True,False)
        # Updates the display to reflect the changes made
        self.update()
        # Update the display to use the current geometry
        # This call seems like it doesn't do anything
        self.geometry(self.geometry())       
        # Set the focus on the entry field
        self.entry.focus_set()
        # Start with the entire thing selected
        self.entry.selection_range(0, Tkinter.END)

    # Gets called when the button gets clicked
    def OnButtonClick(self):
        # Set the value displayed in the label
        self.labelVariable.set( self.entryVariable.get()+" (You clicked the button)" )
        # Set focus back on the entry field
        self.entry.focus_set()
        # Select all the contents of the entry field
        self.entry.selection_range(0, Tkinter.END)

    # Gets called when enter gets pressed from within the entry field
    def OnPressEnter(self,event):
        # Set the value displayed in the label
        self.labelVariable.set( self.entryVariable.get()+" (You pressed ENTER)" )
        # Set focus back on the entry field
        self.entry.focus_set()
        # Select all the contents of the entry field
        self.entry.selection_range(0, Tkinter.END)

if __name__ == "__main__":
    # Initialize an instance of simpleapp with no parent
    app = simpleapp_tk(None)
    # Set the title
    app.title('my application')
    # Run the application
    app.mainloop()
