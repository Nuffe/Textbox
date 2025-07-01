class Undo:
    def __init__(self, node):
        self.data = ""
        self.cursorPos = 0
        self.node = node
        self.delkey = False
        self.pointerY = 0
    
    def append(self, char):
        self.data = self.data + char


# Note:
#   Only for undoing writing. need to add undo for deleting
#   Redo is also left


class UndoList:
    def __init__(self, node):
        self.list = [Undo(node)]
        self.size = 1
        self.undocalled = False
        self.headNode = node

    def append(self, char, cursorPos, node, pointerY, delkey):
        if not self.list:
            self.size += 1
            self.list.append(Undo(node))
        # If spacebar is pressed or user writes to a new line move onto next undo object
        if char == " " or node != self.list[self.size -1].node or self.undocalled:
            self.size += 1
            self.list.append(Undo(node))
            self.undocalled = False

        undo = self.list[self.size -1]
        undo.append(char)
        undo.cursorPos = cursorPos
        undo.pointerY = pointerY
        undo.delkey = delkey



    def undoDelete(self):
        if len(self.list) <= 0:
            return 0, 0, self.headNode
        undoObject = self.list.pop() 
        self.size -= 1 
        for length in range(len(undoObject.data) +1):
            undoObject.node.data.delete((undoObject.cursorPos -length))

        newPos = (undoObject.cursorPos - len(undoObject.data))

        self.undocalled = True
        return newPos, undoObject.pointerY, undoObject.node

    def undoAdd(self):
        if len(self.list) <= 0:
            return 0, 0, self.headNode
        undoObject = self.list.pop() 
        self.size -= 1 
        for length in range(len(undoObject.data)):
            undoObject.node.data.insert(undoObject.cursorPos - len(undoObject.data) + length, undoObject.data[length])
        newPos = (undoObject.cursorPos)
        
        self.undocalled = True
        return newPos, undoObject.pointerY, undoObject.node

        #Not to self. Might need a counter on how many times press backspace. User might only write back part of the word or more then one word
        # Where to call this function, the other is in write, but backspace part dont have character knowladge 