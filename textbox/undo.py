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
        if char == " " or node != self.list[self.size]:
            self.size += 1
            self.list[self.size] = Undo()
        else:
            undo = self.list[self.size]
            undo.append(char)
            undo.cursortPos = cursorPos
            undo.node = node
            

    



    # need to have a check so node exitsts when undo is called
