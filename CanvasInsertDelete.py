# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 15:58:57 2021

@author: Main Floor
"""

from tkinter import *
from ToolTip.ToolTip import ToolTip
from Edit_Display.CanvasTextEdit import CanvasTextEdit
from Highlight.Highlight import MouseoverHighlight
from PopupMenu.PopupMenu import PopupMenu

debugging = False

class CanvasInsertDelete:

    Event               = None
    valid_justification = ["nw", "ne"]
    Canvas_Items        = ["arc", "bitmap", "image", "line", "oval", "polygon",
                    "rectangle", "text", "window"]

    def __init__(self, listofwidgets, canvas, root, justification = "nw" ):

        self.config_check(listofwidgets, canvas, root, justification)          # Confirms that the inputs are valid
        self.PopupMenu()                                                       # Initializes the popup menu
        self.emptyCanvas()

    def config_check(self, listofwidgets, canvas, root, justification):
        """" configuration of CanvasInsertDelete """

        if root != None:                                              # Only Test if the listofwidgets has been updated
            if ( (root.__class__.__name__ != Tk.__name__) &                    # Test to find out if the Root is a Window or Frame
                ( root.__class__.__name__ != Frame.__name__) ):
                raise TypeError ("<Root> must be a Window or a Frame")
            else:
                self.Root = root                                               # Valid Root Object

        if canvas != None:
            if (canvas.__class__.__name__ != Canvas.__name__) :                   # Test to find out if the Canvas is a tkinter Canvas Widget
                raise TypeError ("<canvas> must be a Canvas Widget")
            else:
                self.Canvas = canvas

        if listofwidgets != None:
            if len(listofwidgets) > 0:
                for element in listofwidgets:
                    handler = element[0]
                    if self.Canvas.type(handler) not in CanvasInsertDelete.Canvas_Items:
                        raise TypeError("<listofwidgets> must contain Valid Canvas type Widgets")
                    else:
                        self.listofwidgets = listofwidgets
            else:
                self.listofwidgets = []



        if justification != None:
            if type(justification) == str:
                if justification not in CanvasInsertDelete.valid_justification:
                    raise TypeError ("<justification> is invalid, please check your justification settings")
                else:
                    self.justification = justification

        self.Buffer = [0, 10]
        self.BufferFirst = [10, 10]

    def config(self, listofwidgets = None, canvas = None, root = None, justification = None):
        self.config_check(listofwidgets, canvas, root, justification)          # Send the variables to the configuration update
        self.update()                                                          # update any justification if need be

    def emptyCanvas(self):

        if self.listofwidgets == []:


            # self.listofwidgets = [ [Widget, embued properties, Position, Buffer Space],
            #                        [Widget, embued properties, Position, Buffer Space] ]
            Xnext = self.BufferFirst[0]
            Ynext = self.BufferFirst[1]
            widget = self.Canvas.create_text(Xnext, Ynext, text = "Default Text Entry Location", anchor = "nw")
            embuedproperties = self.createNew(widget)
            Position = [Xnext, Ynext]
            Buffer = self.BufferFirst
            self.listofwidgets.insert(0, [widget, embuedproperties, Position, Buffer])
            self.update()

    def insert(self, event):
        ''' Activated when a new widget is inserted into the canvas. Ensures
        the widget is added to the list. Preforms all instantiation operations
        for a adding a widget to a list'''

        # self.listofwidgets = [ [Widget, embued properties, Position, Buffer Space],
        #                        [Widget, embued properties, Position, Buffer Space] ]


        if debugging == True: print("Clicked Widget Position: ", event.x, event.y)

        #find the position of the widget in the list
        index, currentWidget = self.whichWidget(event)
        if (index, currentWidget) != (-1, 0):                                  # Catch for if widget doesn't exist anymore
                                                                               # Why does this actually become a problem?
            position = self.Canvas.bbox(currentWidget)                                  # Actual Position of Anchor Position
            xmin = position[0]
            xmax = position[2]
            ymin = position[1]
            ymax = position[3]
            if self.justification == "nw":                                          # Anchor Position in NW corner
                ymax = ymin + (ymax - ymin)                                         # bbox seems to be out by a pixel or two
                Xnext = xmin + self.Buffer[0]                                       # ymax may be a slight number of pixels incorrect
                if debugging == True: print("Xmin", xmin, "Xnext", Xnext)
                Ynext = ymax + self.Buffer[1]                                       # but still close enough



            if self.justification == "ne":
                ymax = position[1] + (ymax - ymin)                                  # bbox seems to be out by a pixel or two
                Xnext = xmax + self.Buffer[0]
                Ynext = ymax + self.Buffer[1]


            widget = self.Canvas.create_text(Xnext, Ynext, text = "Default Test %s" % (index + 1), anchor = self.justification)
            embuedproperties = self.createNew(widget)
            Position = [Xnext, Ynext]
            Buffer = self.Buffer
            self.listofwidgets.insert(index + 1, [widget, embuedproperties, Position, Buffer ])

            self.update()




        pass

    def whichWidget(self, event):
        ''' Using the Relative XY coordinates of where a Mouse button press
        occured in the canvas, the function determines which widget was pressed.
        However, I am unsure of what happens when or if the canvas has a
        scrollbar. This may require some more future modifications. '''

        #currentWidget = event.widget


        #find the position of the widget in the list
        index = 0
        #Find Position of previous Widget

        for element in self.listofwidgets:
            widget = element[0]

            position = self.Canvas.bbox(widget)                                #bbox surrounds the widget by 1 pixel

            #print("Widget position: ", self.Canvas.bbox(widget))
            #print("Widget Position: ", self.Canvas.coords(widget))

            xmin = position[0]
            xmax = position[2]

            ymin = position[1]
            ymax = position[3]

            if (xmin <= event.x) & (event.x <= xmax):
                if (ymin <= event.y) & (event.y <= ymax):
                    currentWidget = widget
                    return index, currentWidget
                    break

            index = index + 1

        return -1, 0                                                           #no matching widget found

    def remove(self, event):

        if debugging == True: print("Remove activated")

            # self.listofwidgets = [ [Widget, embued properties, Position, Buffer Space],
            #                        [Widget, embued properties, Position, Buffer Space] ]

        index, currentWidget = self.whichWidget(event)
        if (index, currentWidget) != (-1, 0):                                  # Only Remove a Widget that Exists (catch for double remove)
            if len(self.listofwidgets) > 1:
                self.Canvas.delete(currentWidget)
                #self.listofwidgets[index][1][0].tkinter_widget_leave() #forces tooltip to end
                if debugging == True: print("Which Widget")
                self.listofwidgets.pop(index)
                self.update()
            else:
                self.Root.bell()
                messagebox.showwarning("Last Entry", "Don't delete the last text entry")
                self.Canvas.delete(currentWidget)
                #self.listofwidgets[index][1][0].tkinter_widget_leave() #forces tooltip to end
                if debugging == True: print("Which Widget")
                self.listofwidgets.pop(index)
                self.update()
                self.emptyCanvas()

    def update(self):
        ''' When a widget is added or deleted, the canvas needs to be updated.
        The position of each widget is updated after a widget is added or
        removed '''
        # self.listofwidgets = [ [Widget, embued properties, Position, Buffer Space],
        #                        [Widget, embued properties, Position, Buffer Space] ]

        index = 0
        for currentWidgetEntry in self.listofwidgets:
            if debugging == True: print("***********************************")
            if debugging == True: print("Current Widget: ", index)
            currentWidget = currentWidgetEntry[0]                             # handler to the current widget
            self.Canvas.itemconfig(currentWidget, anchor = self.justification)

            if debugging == True: print("Current Position: ", currentWidgetEntry[2])

            if index == 0:                                                     # First Widget Special Case
                X = currentWidgetEntry[3][0]                                   # Return X Buffer Distance
                Y = currentWidgetEntry[3][1]                                   # Return Y Buffer Distance
                #print("Buffer Space: ", X, Y)
                if self.justification == 'ne':                                 # Modify XY if Right Justified ("ne")
                    canvas_width = self.Canvas.winfo_width()                   # Width of Canvas
                    X = canvas_width - self.BufferFirst[0]                     # NE anchor = Width of Canvas - Buffer Distance
                    Y = self.BufferFirst[1]
                else:
                    X = self.BufferFirst[0]
                    Y = self.BufferFirst[1]
                self.Canvas.coords(currentWidget, X, Y)                        # Move the Widget to this position
                self.listofwidgets[index][3] = [X, Y]                          # Rerecord this position (why?)
                if debugging == True: print("New Position: ", currentWidgetEntry[3])

            else:                                                              # Every Other Widget Normal Case
                previousWidgetEntry = self.listofwidgets[index - 1]            # Previous Widget Column Vector
                previousWidget = previousWidgetEntry[0]                        # Previous Widget Handler
                previous_X = self.Canvas.coords(previousWidget)[0]             # Previous Widget Anchor X Position
                previous_Y = self.Canvas.coords(previousWidget)[1]             # Previous Widget Anchor Y Position
                coordinates = self.Canvas.bbox(previousWidget)               # Previous Widget Bounding Box [xmin, ymin, xmax, ymax]
                                                                               # xmin, ymin is top left corner
                                                                               # xmax, ymax is bottom right corner
                height = coordinates[3] - coordinates[1]
                width = coordinates[2] - coordinates[0]

                if debugging == True: print("Width: ", width, "Heigh: ", height)


                previousWidget_refX = previous_X
                previousWidget_refY = previous_Y + height


                Buffer = currentWidgetEntry[3]
                Buffer_X = Buffer[0]
                Buffer_Y = Buffer[1]

                if debugging == True: print("Buff_X: ", Buffer_X, "Buff_Y: ", Buffer_Y)

                new_X = previousWidget_refX + Buffer_X
                new_Y = previousWidget_refY + Buffer_Y

                position = [new_X, new_Y]

                if debugging == True: print("New X: ", new_X, "New Y: ", new_Y)

                self.Canvas.coords(currentWidget, new_X, new_Y)

                self.listofwidgets[index][2] = position

            if debugging == True: print("Update Complete")

            index = index + 1

        pass

    def createNew(self, widget):
        ''' Create a new widget, endow the widget with all of the desired
        properties using this method. '''
        listofproperties = []

        feature = ToolTip(widget, self.Root, self.Canvas,                      # Tooltip Popup upon mouseover
                          text = "Right Click bring up popup menu")
        listofproperties.append(feature)
        feature = CanvasTextEdit(widget, self.Canvas, self.Root)               # Edit Text Entry
        listofproperties.append(feature)
        feature = MouseoverHighlight(widget, self.Root, self.Canvas, 0x03)           # Highlight upon Mouseover
        listofproperties.append(feature)
        feature = PopupMenu(widget, self.Root, self.Canvas, self.Menu, self)   # Popup Menu Upon Right Click
        listofproperties.append(feature)
        feature = self.PopupMenu_feature(widget)                               # Auto-Update Popup Menu Functions
        listofproperties.append(feature)

        #self.Canvas.tag_bind(widget, '<Button-3>', self.insert)
        #self.Canvas.tag_bind(widget, '<Button-1>', self.remove)

        return listofproperties

    def configUpdate(self, justification) :
        self.justification = justification
        self.update()


    def PopupMenu(self, event = None):

        self.Menu = Menu(self.Root, tearoff = 0)
        self.Menu.add_command(label = "Insert Below  " )
        self.Menu.add_command(label = "Remove Current")
        self.SubMenu = Menu(self.Menu)
        self.SubMenu.add_command(label = "LHS Justification", command = (lambda: self.configUpdate(justification = 'nw')))
        self.SubMenu.add_command(label = "RHS Justification", command = (lambda: self.configUpdate(justification = 'ne')))
        self.Menu.add_cascade(label = "Justification", menu = self.SubMenu)


    def PopupMenu_feature(self, Widget):
        self.Canvas.tag_bind(Widget, "<Button-3>", self.PopupMenu_update, add = '+')


    def PopupMenu_update(self, event = None  ):

        if event != None:
            CanvasInsertDelete.Event = event
            if debugging == True: print("Event:" , CanvasInsertDelete.Event.x)

        Event = CanvasInsertDelete.Event

        self.Menu.entryconfig("Insert Below  ", command = (lambda: self.insert(Event) ) )
        self.Menu.entryconfig("Remove Current", command = (lambda: self.remove(Event) ) )


    def returnWidgets(self):
        pass





if __name__ == "__main__":



    debugging = False
    Root = Tk()

    Root.focus_set()

    Button_ = Button(Root, text = "Test")
    Button_.pack()

    canvas = Canvas(Root, width = 400, height = 400)
    canvas.pack()

    listofwidgets = []

    # self.listofwidgets = [ [Widget, embued properties, Position, Buffer Space],
    #                        [Widget, embued properties, Position, Buffer Space] ]

    #canvasText = canvas.create_text(10, 10, text = "Default Text", anchor = NW)

    #canvasTextEdit    = CanvasTextEdit(canvasText, canvas, Root)
    #canvasTextToolTip = ToolTip(canvasText, Root, canvas, text = "Right click to insert below")
    #if debugging == True: print(canvas.coords(canvasText))
    #canvas.coords(canvasText, 10, 10)
    #if debugging == True: print(canvas.coords(canvasText))
    #listofwidgets.append([canvasText, [canvasTextEdit, canvasTextToolTip], [10, 10], [10, 10]])




    CanvasWidgetManager = CanvasInsertDelete(listofwidgets, canvas, Root)

    def callback(event, number = 5):
        print("Event: ", event)
        print("Number: ", number)
        Button_.unbind(bind_reference)
        print(Button_.winfo_pointerxy())

        print(Root.winfo_rootx() )
        #print(canvasText.winfo_rootx())
        print("Window size: ", canvasText.winfo_screenheight())



    #canvas.tag_bind(canvasText, '<Button-3>', CanvasWidgetManager.insert, add = '+')

    #bind_reference = Button_.bind("<Enter>", lambda event: callback(event, 5))

    Root.mainloop()


