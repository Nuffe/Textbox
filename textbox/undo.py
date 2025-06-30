class Undo:
    def __init__(self, node):
        self.data = ""
        self.cursorPos = 0
        self.node = node
        self.delkey = False
    
    def append(self, char):
        self.data = self.data + char


class UndoList:
    def __init__(self, node):
        self.list = [Undo(node)]
        self.size = 1

    def append(self, char, cursorPos, node):
        print(f"[append] char='{char}', size={self.size}")
        if char == " " or node != self.list[self.size -1].node: # If spacebar is pressed or user writes to a new line move onto next undo object
            print("→ NEW Undo created")
            self.size += 1
            self.list.append(Undo(node))
            if char != " ":
                self.list[self.size].append(char) # Run the function again to add the character for the new Undo

        else:
            print("→ Appending to existing Undo")
            undo = self.list[self.size -1]
            undo.append(char)
            undo.cursorPos = cursorPos

            

    
    def undo(self):
        print("Undo")
        if len(self.list) <= 0:
            return print("Noting to undo")
        undoObject = self.list.pop() 
        self.size -= 1               # Somethin goes wrong here :(
        print("size: " +  str(self.size))
        print("undo data: " + undoObject.data)
        print("cursorPos:" + str(undoObject.cursorPos))
        print(undoObject.node)

        for length in range(len(undoObject.data) +1):
            print(length)
            undoObject.node.data.delete(undoObject.cursorPos -length)
        newPos = (undoObject.cursorPos - len(undoObject.data))
        return newPos


    # need to have a check so node exitsts when undo is called
    # If undo before a undo exists, probebly a problem. Look at later
    # toDo: functions for the interactions with the nodes themself when undo is pressd.
    # UndoList.undo() or something