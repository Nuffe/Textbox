
class TextEditor {
    constructor(root) {
        this.cursorPos = 0;                 // column inside current line
        this.pointerY = 0;                  // line index
        this.list = new LineList();
        this.currentNode = this.list.append(new GapBuffer(10));

        this.root = root;                     
        this.linesEl = root.querySelector(".lines");
        this.cursorEl = root.querySelector(".cursor");
        this.highlightEL = root.querySelector(".highlight-layer")

        this.undolist = new UndoList(this.currentNode, this.list)

        const style = getComputedStyle(this.linesEl);
        this.font = `${style.fontSize} ${style.fontFamily}`;

        // Fontsize for cursor to move correctly
        const lh = parseFloat(style.lineHeight);
        if (Number.isFinite(lh)) {
            this.lineHeight = lh;
        } else {
            this.lineHeight = parseFloat(style.fontSize) * 1.6;
        }
        this.measurer = document.createElement("canvas").getContext("2d");
        this.measurer.font = this.font;

        this.bindEvents();
        this.renderAll();
        this.renderCursor();
    }


    renderAll() {
        this.linesEl.textContent = "";
        for (const node of this.list) {
            node.div = this.makeLineDiv(node);
            this.linesEl.appendChild(node.div);
        }
    }

    makeLineDiv(node) {
        const div = document.createElement("div");
        div.className = "line";
        div.node = node
        div.textContent = node.data.textContent();
        div.onmouseup = (e) => {
            this.onClickFunction(e, node)
        }

        return div;
    }

    renderLine(node) {
        node.div.textContent = node.data.textContent();
    }

    columnToX(node, col) {
        const text = node.data.textContent().slice(0, col);
        return this.measurer.measureText(text).width;
    }


    renderCursor() {
        const rect = this.getCaretRect();
        const linesRect = this.linesEl.getBoundingClientRect();
        const x = rect.x - linesRect.x;
        const y = rect.y  - linesRect.y -4; //-4 to alight caret better
        this.cursorEl.style.transform = `translate(${x}px, ${y}px)`;
        this.cursorEl.style.height = `${this.lineHeight}px`;
        this.restartBlink();
    }

    getCaretRect() {
        const textNode = this.currentNode.div.firstChild;
        if (!textNode) {
            return this.currentNode.div.getBoundingClientRect(); // left edge = caret x
        }
        const range = document.createRange();
        range.setStart(textNode, this.cursorPos);
        range.setEnd(textNode, this.cursorPos);
        const rect = range.getBoundingClientRect();
        return rect
    }

    restartBlink() {
        this.cursorEl.style.animation = "none";
        void this.cursorEl.offsetWidth;
        this.cursorEl.style.animation = "";
    }

    bindEvents() {
        this.root.addEventListener("keydown", (e) => this.onKeyDown(e));

        this.root.onmousedown = (e) => {
            this.clickDrag(e.clientX, e.clientY)
        }
    }

    onKeyDown(e) {
        if (e.ctrlKey || e.metaKey) {
            switch (e.key.toLowerCase()) {
                case "s": e.preventDefault(); return; //TODO, Save
                case "f": e.preventDefault(); return; //TODO, Load
                case "z": e.preventDefault(); return; //TODO, Undo   
                case "y": e.preventDefault(); return; //TODO, Redo
                default: return; // lets Ctrl C for now
            }
        }

        switch (e.key) {
            case "Backspace":
                e.preventDefault();
                this.backspace();
                break;

            case "Enter":
                e.preventDefault();
                this.pressReturn();
                break;

            case "ArrowLeft":
                e.preventDefault();
                this.moveCursor(e.key)
                break;
            case "ArrowRight":
                e.preventDefault();
                this.moveCursor(e.key)
                break;
            case "ArrowUp":
                e.preventDefault();
                this.moveCursor(e.key)
                break;
            case "ArrowDown":
                e.preventDefault();
                this.moveCursor(e.key);
                break;

            default:
                if (e.key.length === 1) {
                    e.preventDefault();
                    this.typeCharacter(e.key);
                }
        }
    }

    typeCharacter(char) {
        this.currentNode.data.insert(this.cursorPos, char);
        this.cursorPos += 1;
        console.log("With of div: ",this.currentNode.div.offsetHeight)
        this.renderLine(this.currentNode);   // repaint one div
        this.renderCursor();                 // reposition the caret
        // TODO(undo): record the insert, mirroring your UndoList
    }

    backspace() {
        console.log("Cursor position: ", this.cursorPos)
        if (this.cursorPos > 0) {
            this.currentNode.data.delete(this.cursorPos);
            this.cursorPos -= 1;
            this.renderLine(this.currentNode);
            this.renderCursor();
            // TODO(undo): record the deleted char returned by delete()
        } else {
            if (this.cursorPos == 0 && this.list.head != this.currentNode ){

                let node = this.currentNode;
                [this.cursorPos, this.pointerY, this.currentNode] = this.undolist.doLineJoin(this.currentNode, this.cursorPos, this.pointerY)
                node.div.remove()

                this.renderLine(this.currentNode);
                this.renderCursor();
            }
           
        }
    }

        pressReturn() {
            const node = this.currentNode;  // Remembers old main row
            [this.cursorPos, this.pointerY, this.currentNode] = this.undolist.doEnterJump(node, this.cursorPos, this.pointerY); 

            this.currentNode.div = this.makeLineDiv(this.currentNode);  
            node.div.after(this.currentNode.div);                       
            this.renderLine(node);                                     
            this.renderCursor();                                        
        }

    moveCursor(key) {
        switch(key){
            case "ArrowLeft":
                if(this.cursorPos > 0){
                    this.cursorPos -=1;
                    console.log("Cursor pos: ", this.cursorPos);
                } else {
                    if(this.currentNode != this.list.head){
                        this.currentNode = this.currentNode.prev;
                        this.cursorPos = this.currentNode.data.length();
                    }
                }
                this.renderCursor()
                break;
            case "ArrowRight":
                if(this.cursorPos < this.currentNode.data.length()){
                    this.cursorPos +=1;
                    console.log("Cursor pos: ", this.cursorPos);
                    this.renderCursor();
                }   
                break;
            case "ArrowUp":          
                const testCursor = this.getCaretRect() 
                const range = document.caretRangeFromPoint(testCursor.x, testCursor.y -this.lineHeight);

                //Stop if at the top
                if(!range||!range.startContainer.parentElement.node){
                    break;
                }
                //Change node if new div is based on another node
                if(this.currentNode != range.startContainer.parentElement.node){
                    this.currentNode = range.startContainer.parentElement.node;
                }          
                this.pointerY = this.list.indexOf(this.currentNode); //Update pointerY
                this.cursorPos = range.startOffset;
                this.renderCursor();
                break;
            case "ArrowDown": {
                const testCursor = this.getCaretRect()
                const range = document.caretRangeFromPoint(testCursor.x, testCursor.y +this.lineHeight);

                //Stop if at the bottom
                if(!range || !range.startContainer.parentElement.node){
                break;
                }
            
                if(this.currentNode != range.startContainer.parentElement.node){
                    this.currentNode = range.startContainer.parentElement.node;
                }                    
                this.cursorPos = range.startOffset;
                this.pointerY = this.list.indexOf(this.currentNode);
                this.renderCursor();
                break;
            }
        }
    }

    onClickFunction(e, node) {
        this.currentNode = node;
        const nodeLocation = this.list.indexOf(node);
        this.pointerY = nodeLocation;
        const range = document.caretRangeFromPoint(e.clientX, e.clientY);
        this.cursorPos = range.startOffset;
        this.renderCursor();
    }

    clickDrag(startX, startY){
        const caret = document.caretPositionFromPoint(startX, startY);
        const range = document.createRange();
        const startDir = caret.offsetNode;
        range.setStart(startDir, caret.offset);
        const compareRange = document.createRange()
        compareRange.setStart(startDir, caret.offset)
        compareRange.setEnd(startDir, caret.offset)

        this.highlightEL.replaceChildren()
        let divList = []

        this.root.onmousemove = (e) => {
            const caretMoving = document.caretPositionFromPoint(e.clientX , e.clientY);
            if(compareRange.comparePoint(caretMoving.offsetNode, caretMoving.offset) == 1){
                range.setEnd(caretMoving.offsetNode, caretMoving.offset);
                range.setStart(startDir, caret.offset);
            }else if (compareRange.comparePoint(caretMoving.offsetNode, caretMoving.offset) == -1){
                range.setEnd(caret.offsetNode, caret.offset);
                range.setStart(caretMoving.offsetNode, caretMoving.offset);
            }else {
                range.setEnd(caretMoving.offsetNode, caretMoving.offset);
                range.setStart(startDir, caret.offset);
            }

            const linesRect = this.linesEl.getBoundingClientRect();
            const rects = range.getClientRects();

            if(divList.length < rects.length){ 
                for(let i = 0; i < rects.length; i++){
                    if(!divList[i]){
                        divList[i] = (document.createElement("div"))
                    }
                }
            }
            if(divList.length > rects.length){ //Remove unneeded divs
                const listLength = divList.length;
                for(let i = listLength; i > rects.length; i--){
                    const div = divList.pop()
                    div.remove()
                }
            }
            
            for(let i = 0; i < rects.length; i++){
                const div = divList[i]
                const rect = rects[i]
                div.setAttribute("ID", "highlight")
                div.setAttribute("ID", "highlight")
                div.style.left   = (rect.left - linesRect.x) + "px";
                div.style.top    = (rect.top - linesRect.y) + "px";
                div.style.right  = (linesRect.right - rect.right) + "px";
                div.style.bottom = (linesRect.bottom - rect.bottom) + "px";
                this.highlightEL.appendChild(div)   
            }

        }
        this.root.onmouseup =  (e) => {
            this.root.onmousemove = null;
        }
    }


    // TODO(load)
    // TODO(save)

}

window.addEventListener("DOMContentLoaded", () => {
    const editor = new TextEditor(document.querySelector(".editor"));
    document.querySelector(".editor").focus();
    window.editor = editor; 
});


