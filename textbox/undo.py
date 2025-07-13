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
                1 if op_type == "insert_char" else 
                -1 if op_type == "delete_char" else 0
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

        
    def undoAction(self, undoObject):
        self.redoList.append(undoObject)
        if undoObject.op_type == "Head":
            # If the head is called, return the current position and node
            return 0, 0, self.nodeList.head


        if undoObject.op_type == "delete_line":
                # Adds a new line back to the nodeList
            newNode = self.nodeList.insert_oldNode_after(undoObject.prev, undoObject.node)
            undoObject.pointerY += 1
            undoObject.cursorPos = 0
            return undoObject.cursorPos, undoObject.pointerY, newNode

        elif undoObject.op_type == "add_line":
                # Removes the last created line from the list
                nodePrevious = undoObject.node.prev
                self.nodeList.remove(undoObject.node)
                if nodePrevious:
                    new_current = nodePrevious
                elif self.nodeList.head: 
                    new_current = self.nodeList.head
                return undoObject.cursorPos, undoObject.pointerY, new_current
        
        elif undoObject.op_type == "delete_char":
            # Puts back the deleted characters
            for i, char in enumerate(undoObject.data):
                undoObject.node.data.insert(undoObject.cursorPos -1, char)
            newPos = undoObject.cursorPos + len(undoObject.data) -1
            undoObject.cursorPos = newPos
            undoObject.node.data.move_position(newPos)

        elif undoObject.op_type in ("insert_char", "insert_space"):
            # Deletes the last added character
            data = undoObject.data
            start = undoObject.cursorPos
            for char in data:
                undoObject.node.data.delete(start)
                start -= 1
            newPos = start
            undoObject.cursorPos = newPos
            undoObject.node.data.move_position(newPos)

        else:
            # fallback if nothing triggers
            return undoObject.cursorPos, undoObject.pointerY, undoObject.node
        self.undoCalled = True
        return newPos, undoObject.pointerY, undoObject.node
    

    def redo(self):
        redoObject = self.redoList.pop()
        if redoObject.op_type == "insert_char" or redoObject.op_type == "insert_space":
            for char in reversed(redoObject.data):
                redoObject.node.data.insert(redoObject.cursorPos , char)
            newPos = redoObject.cursorPos + len(redoObject.data)
            redoObject.cursorPos = newPos  
            redoObject.node.data.move_position(newPos)

        elif redoObject.op_type == "delete_char":
            for i in range(len(redoObject.data)):
                char = redoObject.node.data.delete(redoObject.cursorPos)
                print("deleted char redo: ", char)
                redoObject.cursorPos -= 1
            newPos = redoObject.cursorPos
            redoObject.node.data.move_position(newPos)
    
        elif redoObject.op_type == "delete_line":
            redoObject.op_type = "add_line"
        elif redoObject.op_type == "add_line":
            redoObject.op_type = "delete_line"


        # Ändrar något i redo som undo inte gillar och det blir baklänges
        self.list.append(redoObject)
        print("redoObject:", redoObject.data)
        return redoObject.cursorPos, redoObject.pointerY, redoObject.node  

