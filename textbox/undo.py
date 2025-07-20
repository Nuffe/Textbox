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
        print("append undo data: ", undo.data)

#------------------------------------------
# Redo for backspace and enterJump with text
# Undo still sometimes jump to far on back-to-back undos
#--------------------------------------------        

    def undoAction(self, undoObject):
        if undoObject.op_type == "Head":
            # If the head is called, return the current position and node
            return 0, 0, self.nodeList.head

        if undoObject.op_type == "addLine":
            cursorPos, newY, newNode = self.addLine(undoObject)
            if self.undoCalled:
                newY -= 1 #Temp bug fix where it jumped twice on back-to-back undo

        elif undoObject.op_type == "undoLine":
            cursorPos, newY, newNode = self.deleteLine(undoObject)

        elif undoObject.op_type == "addChar":
            cursorPos, newY, newNode = self.addText(undoObject)

        elif undoObject.op_type in ("undoChar", "undoSpace"):
            cursorPos, newY, newNode = self.undoText(undoObject)
        

        #----------------------
        # Remake lineJumpUP and enterJump, so they dont rely on exisitn functons.
        # ---------------------------
        elif undoObject.op_type == "lineJumpUP":
            print("Undo LineJumpUP")
            newPos = undoObject.cursorPos
            for i in undoObject.data:
                undoObject.node.data.delete(len(undoObject.node.data.textContent()))  # Remove the character from the current line
                newPos -= 1
            newNode = self.nodeList.insert_after(undoObject.node, gapBuffer(10))
            newNode.data.insert(0, undoObject.data)
            newY = undoObject.pointerY
            cursorPos = 0

        elif undoObject.op_type == "enterJump":
            print("Undo enterJump")
            newNode = undoObject.node
            self.nodeList.remove(undoObject.node.next)
            newNode.data.insert(len(newNode.data.textContent()), undoObject.data)
            cursorPos = len(newNode.data.textContent()) - len(undoObject.data)
            newY = undoObject.pointerY -1

        else:
            # fallback if nothing triggers
            return undoObject.cursorPos, undoObject.pointerY, undoObject.node
        
        self.redoList.append(undoObject)
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
        elif redoObject.op_type == "lineJumpUP": # Basicly reversed what undo function does
            print("redo lineJumpUP")
            # remove line, add text

            newNode = redoObject.node         
            self.nodeList.remove(redoObject.node.next)
            newNode.data.insert(len(newNode.data.textContent()), redoObject.data)
            cursorPos = len(newNode.data.textContent()) - len(redoObject.data)
            newY = redoObject.pointerY -1
            self.list.append(redoObject)
            return cursorPos, newY, newNode
        elif redoObject.op_type == "enterJump":
            # Look over all the node jumps, some might be superflous
             # remove text, add line, add text
            print("redo enterJump")
            
            newPos = redoObject.cursorPos
            for i in redoObject.data:
                redoObject.node.data.delete(len(redoObject.node.data.textContent()))  # Remove the character from the current line
                newPos -= 1
            newNode = self.nodeList.insert_after(redoObject.node, gapBuffer(10))
            newNode.data.insert(0, redoObject.data)
            newY = redoObject.pointerY
            cursorPos = 0     
            self.list.append(redoObject)
            return cursorPos, newY, newNode

        else:
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
        print("AddLine function")
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
        base = max(undoObject.cursorPos - 1, 0)
        # iterate over data backwards becaus deleted data comes in backwards
        for i, char in enumerate(undoObject.data[::-1]):
            undoObject.node.data.insert(base + i, char)
        newPos = undoObject.cursorPos + len(undoObject.data) - 1
        undoObject.cursorPos = newPos
        undoObject.node.data.move_position(newPos)
        return newPos, undoObject.pointerY, undoObject.node