

class Undo {
    constructor(opType, node, cursorPos, pointerY, data = "") {
        this.node = node;
        this.prev = node ? node.prev : null;
        this.next = node ? node.next : null;
        this.opType = opType;
        this.data = data;
        this.cursorPos = cursorPos;
        this.pointerY = pointerY;
        this.splitNode = null;
    }
}

class UndoList {
    constructor(node, nodeList) {
        this.nodeList = nodeList;
        this.list = [new Undo("Head", node, 0, 0)];
        this.size = 1;
        this.undoCalled = false;
        this.headNode = node;
        this.redoList = [];
    }

    append(char, cursorPos, node, pointerY, opType) {
        const last = this.list.length ? this.list[this.list.length - 1] : null;
        this.redoList = []; // resetting redo

        const newUndo = (
            this.undoCalled
            || last === null
            || opType !== last.opType
            || node !== last.node
        );

        let cursorMove = false;
        if (!newUndo) {
            const expected = last.cursorPos + (
                opType === "undoChar" ? 1 :
                opType === "addChar" ? -1 : 0
            );
            if (cursorPos !== expected) cursorMove = true;
        }
        if (!newUndo){
            let expected = last.curorPos;
            if(opType === "undoChar"){
                expected = last.cursorPos + 1
            }
            if(opType === "addChar"){
                expected = last.cursorPos -1
            } 
            if (cursorPos !== expected) cursorMove = true;
        }


        if (newUndo || cursorMove) {
            this.list.push(new Undo(opType, node, cursorPos, pointerY, ""));
            this.size = this.list.length;
            this.undoCalled = false;
        }

        // Add the data to the last undo object
        const undo = this.list[this.list.length - 1];
        undo.data += char;
        undo.opType = opType;
        undo.cursorPos = cursorPos;
        undo.pointerY = pointerY;
        console.log("append undo data:", undo.data);
    }
    
    // Redo for backspace and enterJump with text.
    undoAction(undoObject) {
        if (undoObject.opType === "Head") {
            return [0, 0, this.nodeList.head];
        }

        let cursorPos, newY, newNode;

        if (undoObject.opType === "addLine") {
            [cursorPos, newY, newNode] = this.addLine(undoObject);
            if (this.undoCalled) {
                newY -= 1; // temp bug fix: jumped twice on back-to-back undo
            }
        } else if (undoObject.opType === "undoLine") {
            [cursorPos, newY, newNode] = this.deleteLine(undoObject);
        } else if (undoObject.opType === "addChar") {
            [cursorPos, newY, newNode] = this.addText(undoObject);
        } else if (undoObject.opType === "undoChar" || undoObject.opType === "undoSpace") {
            [cursorPos, newY, newNode] = this.undoText(undoObject);
        } else if (undoObject.opType === "enterJump") {
            console.log("enterJump");
            [cursorPos, newY, newNode] = this.undoEnterJump(undoObject);
        } else if (undoObject.opType === "lineJoin") {
            console.log("lineJoin");
            [cursorPos, newY, newNode] = this.undoLineJoin(undoObject);
        } else {
            // fallback if nothing triggers
            return [undoObject.cursorPos, undoObject.pointerY, undoObject.node];
        }

        this.redoList.push(undoObject);
        this.undoCalled = true;
        return [cursorPos, newY, newNode];
    }

    redo() {
        if (!this.redoList.length) return null; // nothing to redo

        const redoObject = this.redoList.pop();
        console.log("redoObject:", redoObject.opType, redoObject.data);

        // Redo character insertion
        if (redoObject.opType === "undoChar" || redoObject.opType === "undoSpace") {
            let i = 0;
            for (const char of redoObject.data) {
                redoObject.node.data.insert(redoObject.cursorPos + i, char);
                i += 1;
            }
            const newPos = redoObject.cursorPos + redoObject.data.length;
            redoObject.cursorPos = newPos;
            redoObject.node.data.movePosition(newPos);

            this.list.push(redoObject);
            return [newPos, redoObject.pointerY, redoObject.node];
        }

        // Redo a character deletion
        if (redoObject.opType === "addChar") {
            // move cursor one right (to the first char to delete)
            redoObject.cursorPos += 1;
            for (const _ of redoObject.data) {
                redoObject.node.data.delete(redoObject.cursorPos);
                redoObject.cursorPos -= 1;
            }
            const newPos = redoObject.cursorPos;
            redoObject.node.data.movePosition(newPos);

            this.list.push(redoObject);
            return [newPos, redoObject.pointerY, redoObject.node];
        }

        // Redo the line undo just added
        if (redoObject.opType === "addLine") {
            let baseY = redoObject.pointerY;
            const nodeToRemove = redoObject.node;
            const prevNode = nodeToRemove.prev;
            this.nodeList.remove(nodeToRemove);
            baseY -= 1;
            const newCurrent = prevNode ? prevNode : this.nodeList.head;
            const cursorPos = newCurrent.data.textContent().length;
            this.list.push(redoObject);
            return [cursorPos, baseY, newCurrent];
        }

        // Redo the line that was just undone
        if (redoObject.opType === "undoLine") {
            const newNode = this.nodeList.insertOldNodeAfter(redoObject.prev, redoObject.node);
            const newY = redoObject.pointerY;
            redoObject.cursorPos = 0;
            this.list.push(redoObject);
            return [redoObject.cursorPos, newY, newNode];
        }

        if (redoObject.opType === "enterJump") {
            return this.doEnterJump(redoObject.node, redoObject.cursorPos,
                                    redoObject.pointerY, false);
        }
        if (redoObject.opType === "lineJoin") {
            return this.doLineJoin(redoObject.node, redoObject.cursorPos,
                                   redoObject.pointerY, false);
        }

        return [redoObject.cursorPos, redoObject.pointerY, redoObject.node];
    }

    undoText(undoObject) {
        // Deletes the last added character(s)
        const data = undoObject.data;
        let start = undoObject.cursorPos;
        for (const _ of data) {
            undoObject.node.data.delete(start);
            start -= 1;
        }
        const newPos = start;
        undoObject.cursorPos = newPos;
        undoObject.node.data.movePosition(newPos);
        return [newPos, undoObject.pointerY, undoObject.node];
    }

    addLine(undoObject) {
        console.log("AddLine function");
        const baseY = undoObject.pointerY;
        const newNode = this.nodeList.insertOldNodeAfter(undoObject.prev, undoObject.node);
        const newY = this.undoCalled ? baseY + 1 : baseY;
        return [0, newY, newNode];
    }

    deleteLine(undoObject) {
        // Removes the last created line from the list
        const baseY = undoObject.pointerY;
        const nodePrevious = undoObject.node.prev;
        this.nodeList.remove(undoObject.node);

        const newY = baseY - 1;
        let newCurrent;
        if (nodePrevious) {
            newCurrent = nodePrevious;
        } else if (this.nodeList.head) {
            newCurrent = this.nodeList.head;
        }
        return [undoObject.cursorPos, newY, newCurrent];
    }

    addText(undoObject) {
        const base = Math.max(undoObject.cursorPos - 1, 0);
        // iterate over data backwards because deleted data comes in backwards
        const reversed = [...undoObject.data].reverse();
        reversed.forEach((char, i) => {
            undoObject.node.data.insert(base + i, char);
        });
        const newPos = undoObject.cursorPos + undoObject.data.length - 1;
        undoObject.cursorPos = newPos;
        undoObject.node.data.movePosition(newPos);
        return [newPos, undoObject.pointerY, undoObject.node];
    }

    doEnterJump(node, cursorPos, pointerY, clearRedo = true) {
        console.log("doEnterJump");
        const cmd = new Undo("enterJump", node, cursorPos, pointerY);
        const tail = node.data.textContent().slice(cursorPos);

        for (let i = 0; i < tail.length; i++) {
            node.data.delete(node.data.textContent().length);
        }

        const newNode = this.nodeList.insertAfter(node, new GapBuffer(10));
        newNode.data.insert(0, tail);
        cmd.data = tail;
        cmd.splitNode = newNode;

        this.appendCmd(cmd, clearRedo);
        return [0, pointerY + 1, newNode];
    }

    doLineJoin(node, cursorPos, pointerY, clearRedo = true) {
        console.log("doLineJoin");
        const cmd = new Undo("lineJoin", node, cursorPos, pointerY);
        const prev = node.prev || this.nodeList.head;
        const joined = node.data.textContent();
        prev.data.insert(prev.data.textContent().length, joined);
        this.nodeList.remove(node);
        cmd.data = joined;
        cmd.splitNode = node;
        const newPos = prev.data.textContent().length - joined.length;

        this.appendCmd(cmd, clearRedo);
        return [newPos, pointerY - 1, prev];
    }

    undoEnterJump(cmd) {
        console.log("undoEnterJump");
        const node = cmd.node;
        const moved = cmd.data;
        node.data.insert(node.data.textContent().length, moved);
        this.nodeList.remove(cmd.splitNode);
        return [cmd.cursorPos, cmd.pointerY, node];
    }

    undoLineJoin(cmd) {
        console.log("undoLineJoin");
        const prev = cmd.prev;
        const reNode = this.nodeList.insertOldNodeAfter(prev, cmd.node);
        for (let i = 0; i < cmd.data.length; i++) {
            prev.data.delete(prev.data.textContent().length);
        }
        return [cmd.cursorPos, cmd.pointerY, reNode];
    }

    appendCmd(cmd, clearRedo = true) { // specifically for undo and redo
        if (clearRedo) this.redoList.length = 0;
        this.list.push(cmd);
        this.undoCalled = false;
    }
}
