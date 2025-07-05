from gap_buffer import gapBuffer  # Add this import at the top of your file if gapBuffer is defined elsewhere


class Undo:
    def __init__(self, node, op_type):
        self.node = node
        self.op_type = op_type
        self.data = ""
        self.delkey = False
        self.deleteCount = 0
        self.cursorPos = 0
        self.pointerY = 0



# Note:
#  Things to fix:   -Weird behaviour when undoing twice on a node that has been deleted
#                   - when undoing text and then a node, the cursor position is not correct
#                   - Undoing on empty crashes
#    
#   Redo is also left


class UndoList:
    def __init__(self, node, nodeList):
        self.nodeList = nodeList
        self.list = [Undo(node, "insert_char")]
        self.size = 1
        self.undoCalled = False
        self.headNode = node

    def append(self, char, cursorPos, node, pointerY, delkey, op_type):
        if not self.list or self.size != len(self.list):
            self.list.append(Undo(node, "insert_char"))
            self.size = len(self.list)

        undo = self.list[-1]
        collection = (
            op_type != undo.op_type
            or node is not undo.node
            or self.undoCalled
        )
        
        # If spacebar is pressed or user writes to a new line move onto next undo object
        if collection and undo.data:
            self.list.append(Undo(node, op_type))
            self.size = len(self.list)
            self.undoCalled = False
        
        undo = self.list[-1] 
        undo.data += char
        undo.op_type = op_type
        undo.cursorPos = cursorPos
        undo.pointerY = pointerY
        undo.delkey = delkey
        if delkey:
            undo.deleteCount += 1


    def undoAction(self):
        undoObject = self.list.pop()
        self.size -= 1

        if undoObject.op_type == "delete_line":
                newNode = self.nodeList.insert_after(undoObject.node, gapBuffer(10))
                return undoObject.cursorPos, undoObject.pointerY + 1, newNode
        
        elif undoObject.op_type == "add_line":
                nodePrevious = undoObject.node.prev
                self.nodeList.remove(undoObject.node)
                if nodePrevious:
                    new_current = nodePrevious
                elif self.nodeList.head: 
                    new_current = self.nodeList.head
                else:
                    new_current = self.nodeList.append(gapBuffer(10))
                return undoObject.cursorPos, undoObject.pointerY, new_current
        
        elif undoObject.op_type == "delete_char":
            for i, char in enumerate(undoObject.data):
                undoObject.node.data.insert(undoObject.cursorPos -1 + i, char)
            newPos = undoObject.cursorPos + len(undoObject.data) -1

        elif undoObject.op_type in ("insert_char", "insert_space"):
            # delete each char you previously inserted
            for i in undoObject.data:
                undoObject.node.data.delete(undoObject.cursorPos - 1)
            newPos = undoObject.cursorPos - len(undoObject.data)

        else:
            # safety fallback
            return undoObject.cursorPos, undoObject.pointerY, undoObject.node

        self.undoCalled = True
        return newPos, undoObject.pointerY, undoObject.node