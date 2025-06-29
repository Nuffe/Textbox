class Undo:
    def __init__(self):
        self.data = ""
        self.cursorPos = 0
        self.node = None
        self.delkey = False
    
    def append(self, char):
        self.data = self.data + char


class UndoList:
    def __init__(self):
        self.list = []
        self.size = 0

    def append(self, char, cursorPos, node):

        if char == " " or node != self.list[self.size].node: # If spacebar is pressed or user writes to a new line move onto next undo object
            self.size += 1
            self.list.append(Undo())
            self.list[self.size].append(char) # Run the function again to add the character for the new Undo
        else:
            undo = self.list[self.size -1]
            undo.append(char)
            undo.cursorPos = cursorPos
            undo.node = node
            

    



    # need to have a check so node exitsts when undo is called
    # If undo before a undo exists, probebly a problem. Look at later
    # toDo: functions for the interactions with the nodes themself when undo is pressd.
    # UndoList.undo() or something