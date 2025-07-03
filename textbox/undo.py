from gap_buffer import gapBuffer  # Add this import at the top of your file if gapBuffer is defined elsewhere


class Undo:
    def __init__(self, node):
        self.data = ""
        self.cursorPos = 0
        self.node = node
        self.delkey = False
        self.deleteCount = 0
        self.pointerY = 0

    def append(self, char):
        self.data = self.data + char


# Note:
#   Deleting part is almost dont, one error when deleting right after undoing a delete action
# Think it might have something to do with cursor pos, but not sure.
# Hard to recreate some times
#   Redo is also left


class UndoList:
    def __init__(self, node, nodeList):
        self.nodeList = nodeList
        self.list = [Undo(node)]
        self.size = 1
        self.undocalled = False
        self.headNode = node

    def append(self, char, cursorPos, node, pointerY, delkey):
        print("self.size:" + str(self.size))
        print("calc len: " + str(len(self.list)))
        if not self.list or self.size != len(self.list):
            self.list.append(Undo(node))
            self.size = len(self.list)
        # If spacebar is pressed or user writes to a new line move onto next undo object
        if char == " " or node != self.list[self.size -1].node or self.undocalled or delkey != self.list[self.size -1].delkey:
            self.list.append(Undo(node))
            self.size = len(self.list)
            self.undocalled = False

        undo = self.list[self.size -1]
        undo.append(char)
        undo.cursorPos = cursorPos
        undo.pointerY = pointerY
        undo.delkey = delkey
        if delkey:
            undo.deleteCount += 1



    def undoAction(self):
        if self.list is None or self.size <= 0:
            print("nothing to undo")
            return 0, 0, self.headNode
        undoObject = self.list.pop() 
        self.size -= 1 


        if undoObject.node.data.textContent() == "":
            if undoObject.delkey:
                print("restore node")
                self.nodeList.insert_after(undoObject.node, gapBuffer(10))
                return undoObject.cursorPos, undoObject.pointerY + 1, undoObject.node.next
            else:
                print("node is empty, removing")
                nodePrevious = undoObject.node.prev
                self.nodeList.remove(undoObject.node)   
                return undoObject.cursorPos, undoObject.pointerY, nodePrevious

        elif undoObject.delkey:
            print("undoing delete")
            for length in (range(undoObject.deleteCount)):  
                print(undoObject.data[length])
                undoObject.node.data.insert(undoObject.cursorPos - 1 , undoObject.data[length])
            newPos = (undoObject.cursorPos + length)
            print("pointerY: ", undoObject.pointerY)
        else:
            print("undoing insert")
            for length in range(len(undoObject.data)):
                undoObject.node.data.delete((undoObject.cursorPos - length))
            newPos = (undoObject.cursorPos - len(undoObject.data))
            print("pointerY: ", undoObject.pointerY)

        self.undocalled = True
        return newPos, undoObject.pointerY, undoObject.node
