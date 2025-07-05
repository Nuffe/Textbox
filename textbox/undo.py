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
#  Things to fix:   -Weird behaviour when undoing twice on a node that has been deleted
#                   - when undoing text and then a node, the cursor position is not correct
#                   - Undoing on empty crashes
#    
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
        print("undo called")
        if self.list is None or self.size <= 0:
            print("nothing to undo")
            return 0, 0, self.headNode
        undoObject = self.list.pop()
        self.size -= 1

        if undoObject.node.data.textContent() == "" and undoObject.data == "":
            if undoObject.delkey:
                print("restore node")
                newNode = self.nodeList.insert_after(undoObject.node, gapBuffer(10))
                return undoObject.cursorPos, undoObject.pointerY + 1, newNode
            else:
                print("node is empty, removing")
                nodePrevious = undoObject.node.prev
                self.nodeList.remove(undoObject.node)
                if nodePrevious:
                    new_current = nodePrevious
                elif self.nodeList.head: 
                    new_current = self.nodeList.head
                else:
                    new_current = self.nodeList.append(gapBuffer(10))
                return undoObject.cursorPos, undoObject.pointerY, new_current
        elif undoObject.delkey:
            print("undoing delete")
            for i, char in enumerate(undoObject.data):
                undoObject.node.data.insert(undoObject.cursorPos - 1 + i, char)
            newPos = undoObject.cursorPos + len(undoObject.data) -1
        else:
            print("undoing insert")
            for length in range(len(undoObject.data)):
                undoObject.node.data.delete((undoObject.cursorPos - length))
            newPos = (undoObject.cursorPos - len(undoObject.data))
        self.undocalled = True
        return newPos, undoObject.pointerY, undoObject.node