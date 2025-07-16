from gap_buffer import gapBuffer  # Add this import at the top of your file if gapBuffer is defined elsewhere


class Undo:
    def __init__(self, node, op_type):
        self.node = node
        self.prev = node.prev if node else None
        self.next = node.next if node else None
        self.op_type = op_type
        self.data = ""
        self.cursorPos = 0
        self.pointerY = 0

        

class UndoList:
    def __init__(self, node, nodeList):
        self.nodeList = nodeList
        self.list = [Undo(node, "Head")]
        self.size = 1
        self.undoCalled = False
        self.headNode = node
        self.redoList = []

    def append(self, char, cursorPos, node, pointerY, op_type):
        last = self.list[-1] if self.list else None
        self.redoList = [] # Reseting Redo
        newUndo = ( # Condition to determine if a new undo object should be made
            self.undoCalled 
            or last is None 
            or op_type is not last.op_type 
            or node is not last.node )

        if not newUndo:
            cursorMove = False
            if cursorPos != last.cursorPos + (
                1 if op_type == "undoChar" else 
                -1 if op_type == "addChar" else 0
            ):
                cursorMove = True


        if newUndo or cursorMove: 
            self.list.append(Undo(node, op_type))
            self.size = len(self.list)
            self.undoCalled = False

        # Adds all the data to the last undo object
        undo = self.list[-1]
        undo.data      += char
        undo.op_type   = op_type
        undo.cursorPos = cursorPos
        undo.pointerY  = pointerY

#------------------------------------------
# look over op_type names, you keep confusing yourself
#--------------------------------------------        

    def undoAction(self, undoObject):
        self.redoList.append(undoObject)
        if undoObject.op_type == "Head":
            # If the head is called, return the current position and node
            return 0, 0, self.nodeList.head
        baseY = undoObject.pointerY

        if undoObject.op_type == "addLine":
            cursorPos, newY, newNode = self.addLine(undoObject)

        elif undoObject.op_type == "undoLine":
            cursorPos, newY, newNode = self.deleteLine(undoObject)

        elif undoObject.op_type == "addChar":
            cursorPos, newY, newNode = self.addText(undoObject)

        elif undoObject.op_type in ("undoChar", "undoSpace"):
            cursorPos, newY, newNode = self.undoText(undoObject)
        
        elif undoObject.op_type == "lineJumpUP":
            # Undo the action of pressing back at the beginning of a line when text existed on the line

            # Look over this node swap, parts seam unnesesary 
            prev = undoObject.prev
            node = undoObject.node
            undoObject.node = prev
            self.undoText(undoObject)
            undoObject.node = node
            cursorPos, newY, newNode  = self.addLine(undoObject)
        elif undoObject.op_type == "enterJump":
            prev = undoObject.prev
            self.deleteLine(undoObject)
            undoObject.node = prev
            cursorPos, newY, newNode  = self.addText(undoObject)
            newY -= 1

        else:
            # fallback if nothing triggers
            return undoObject.cursorPos, undoObject.pointerY, undoObject.node
        
        self.undoCalled = True
        return cursorPos, newY, newNode

    def redo(self):
        if not self.redoList:  # nothing to redo
            return None
        redoObject = self.redoList.pop()

        # Redo character insertion 
        if redoObject.op_type in ("undoChar", "undoSpace"):
            i = 0
            for char in redoObject.data:
                redoObject.node.data.insert(redoObject.cursorPos + i, char)
                i += 1
            newPos = redoObject.cursorPos + len(redoObject.data)
            redoObject.cursorPos = newPos
            redoObject.node.data.move_position(newPos)

            self.list.append(redoObject)
            return newPos, redoObject.pointerY, redoObject.node

        # Redo a character deletion
        elif redoObject.op_type == "addChar":
            # move cursor one right (to the first char to delete)
            redoObject.cursorPos += 1
            for i in redoObject.data:
                redoObject.node.data.delete(redoObject.cursorPos)
                redoObject.cursorPos -= 1
            newPos = redoObject.cursorPos
            redoObject.node.data.move_position(newPos)

            self.list.append(redoObject)
            return newPos, redoObject.pointerY, redoObject.node

        # Redo the line undo just added
        elif redoObject.op_type == "addLine":
            baseY = redoObject.pointerY
            node_to_remove = redoObject.node
            prev_node = node_to_remove.prev
            self.nodeList.remove(node_to_remove)
            baseY -= 1
            if prev_node:
                new_current = prev_node
            else:
                new_current = self.nodeList.head

            self.list.append(redoObject)
            return redoObject.cursorPos, baseY, new_current

        # Redo a the line that was just undone
        elif redoObject.op_type in ("undoLine"):
            new_node = self.nodeList.insert_oldNode_after(redoObject.prev, redoObject.node)
            newY = redoObject.pointerY 
            redoObject.cursorPos = 0
            self.list.append(redoObject)
            return redoObject.cursorPos, newY, new_node

        else:
            self.list.append(redoObject)
            return redoObject.cursorPos, redoObject.pointerY, redoObject.node



    def undoText(self, undoObject):
        # Deletes the last added character
        data = undoObject.data
        start = undoObject.cursorPos
        for char in data:
            undoObject.node.data.delete(start)
            start -= 1
        newPos = start
        undoObject.cursorPos = newPos
        undoObject.node.data.move_position(newPos)
        return newPos, undoObject.pointerY, undoObject.node
    
    def addLine(self, undoObject):
        baseY = undoObject.pointerY
        newNode = self.nodeList.insert_oldNode_after(undoObject.prev, undoObject.node)
        if self.undoCalled:
            newY = baseY + 1
        else:
            newY = baseY
        return 0, newY, newNode
    
    def deleteLine(self, undoObject):
        # Removes the last created line from the list
        baseY = undoObject.pointerY
        nodePrevious = undoObject.node.prev
        self.nodeList.remove(undoObject.node)
        
        newY = baseY -1
        if nodePrevious:
            new_current = nodePrevious
        elif self.nodeList.head: 
            new_current = self.nodeList.head
        return undoObject.cursorPos, newY, new_current        
    
    def addText(self, undoObject):
        for i, char in enumerate(undoObject.data):
            undoObject.node.data.insert(undoObject.cursorPos -1, char)
        newPos = undoObject.cursorPos + len(undoObject.data) -1
        undoObject.cursorPos = newPos
        undoObject.node.data.move_position(newPos)
        return newPos, undoObject.pointerY, undoObject.node

