class Undo:
    def __init__(self, node):
        self.data = ""
        self.cursorPos = 0
        self.node = node
        self.delkey = False
        self.pointerY = 0
    
    def append(self, char):
        self.data = self.data + char

# Need fix, move pointer to follow with undo

class UndoList:
    def __init__(self, node):
        self.list = [Undo(node)]
        self.size = 1
        self.undocalled = False
        self.headNode = node

    def append(self, char, cursorPos, node, pointerY):
        print(f"[append] char='{char}', size={self.size}")

        if not self.list:
            self.size += 1
            self.list.append(Undo(node))

        if char == " " or node != self.list[self.size -1].node or self.undocalled: # If spacebar is pressed or user writes to a new line move onto next undo object
            print("→ NEW Undo created")
            self.size += 1
            self.list.append(Undo(node))
            self.undocalled = False
            print("list size: " + str(self.size) + " calc size = " + str(len(self.list)))
          
        print("→ Appending to existing Undo")
        undo = self.list[self.size -1]
        undo.append(char)
        undo.cursorPos = cursorPos
        undo.pointerY = pointerY

    def undo(self):
        if len(self.list) <= 0:
            print("Noting to undo")
            return 0, 0, self.headNode
        undoObject = self.list.pop() 
        self.size -= 1               # Somethin goes wrong here :(
        print("size: " +  str(self.size))
        print("undo data: " + undoObject.data)
        print("cursorPos:" + str(undoObject.cursorPos))

        for length in range(len(undoObject.data) +1):
            undoObject.node.data.delete((undoObject.cursorPos -length))
        newPos = (undoObject.cursorPos - len(undoObject.data))
        self.undocalled = True
        print("undo pointerY: " + str(undoObject.pointerY))
        return newPos, undoObject.pointerY, undoObject.node
