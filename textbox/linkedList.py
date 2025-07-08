class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class LineList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, buffer):
        new_node = Node(buffer)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
        return new_node

    def insert_after(self, node, buffer):
        if node is None:
            print("Error: The given node is None")
            return
        new_node = Node(buffer)
        new_node.prev = node
        new_node.next = node.next
        if node.next:
            node.next.prev = new_node
        else:
            # we are at the tail and update it
            self.tail      = new_node
        node.next         = new_node
        self.size        += 1
        return new_node
    
    # Custom for inserting and old node, specificly for undo functionality
    def insert_oldNode_after(self, node, old_node):
        if old_node is None:
            print("Error: The given node is None")
            return
        new_node = old_node
        new_node.prev = node
        new_node.next = node.next
        if node.next:
            node.next.prev = new_node
        else:
            self.tail      = new_node
        node.next         = new_node
        self.size        += 1
        return new_node


    def remove(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            # if no prev, then we at head
            self.head = node.next
        # need two "if else" because head and tail can be the same node
        if node.next:
            node.next.prev = node.prev
        else:
            # if no next, we at tail
            self.tail = node.prev
        node.prev = node.next = None
        self.size -= 1

    def contains(self, node):
        current = self.head
        while current:
            if current == node:
                return True
            current = current.next
        return False

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur
            cur = cur.next