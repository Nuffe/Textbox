
class Node {
    constructor(data) {
        this.data = data;   // a GapBuffer
        this.prev = null;
        this.next = null;
        this.div = null;    // set by the renderer, not by the list
    }
}

class LineList {
    constructor() {
        this.head = null;
        this.tail = null;
        this.size = 0;
    }

    append(buffer) {
        const newNode = new Node(buffer);
        if (!this.head) {
            this.head = this.tail = newNode;
        } else {
            newNode.prev = this.tail;
            this.tail.next = newNode;
            this.tail = newNode;
        }
        this.size += 1;
        return newNode;
    }

    insertAfter(node, buffer) {
        const newNode = new Node(buffer);
        if (node === null) {
            // Empty list or insert at head,  fix head and tail
            newNode.next = this.head;
            if (this.head) this.head.prev = newNode;
            this.head = newNode;
            if (this.tail === null) this.tail = newNode;
        } else {
            newNode.prev = node;
            newNode.next = node.next;
            if (node.next) {
                node.next.prev = newNode;
            } else {
                this.tail = newNode; // at tail
            }
            node.next = newNode;
        }
        this.size += 1;
        return newNode;
    }

    // Reinserting a previously existing node saved in undo/redo objects
    insertOldNodeAfter(node, oldNode) {
        if (oldNode === null) throw new Error("Can't insert null");
        oldNode.prev = node;
        oldNode.next = node.next;
        if (node.next) {
            node.next.prev = oldNode;
        } else {
            this.tail = oldNode;
        }
        node.next = oldNode;
        this.size += 1;
        
        return oldNode;
    }

    remove(node) {
        if (node.prev) {
            node.prev.next = node.next;
        } else {
            this.head = node.next; // no prev, we're at head
        }
        // two checks, head and tail can be the same node
        if (node.next) {
            node.next.prev = node.prev;
        } else {
            this.tail = node.prev; // no next -> we're at tail
        }
        node.prev = node.next = null;
        this.size -= 1;
    }

    contains(node) {
        let current = this.head;
        while (current) {
            if (current === node) return true;
            current = current.next;
        }
        return false;
    }

    // alternative to  Python __iter__
    *[Symbol.iterator]() {
        let cur = this.head;
        while (cur) {
            yield cur;
            cur = cur.next;
        }
    }

    //Keeps track of y, where user is and specific rows are
    indexOf(node) {
        let i = 0;
        for (const n of this) {
            if (n === node) return i;
            i += 1;
        }
        return -1;
    }

    clear() {
        this.head = null;
        this.tail = null;
        this.size = 0;
    }
}
