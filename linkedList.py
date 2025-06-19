

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None
    
def traverse(head):
        current = head
        while current:
            print(current.data, end=' ')
            current = current.next
        print("None")

def insert_at_beginning(head, data):
        new_node = Node(data)
        new_node.next = head
        if head:
            head.prev = new_node
        return new_node
    
def insert_after_node(node, data):
    if node is None:
        print("Error: The given node is None")
        return

    new_node = Node(data)
    new_node.prev = node
    new_node.next = node.next

    if node.next:
        node.next.prev = new_node

    node.next = new_node

def insert_at_end(head, data):
    # Insert a new node at the end of the doubly linked list
    new_node = Node(data)
    if head is None:
        return new_node

    current = head
    while current.next:
        current = current.next

    current.next = new_node
    new_node.prev = current
    return head

def delete_at_position(head, position):
    # Delete the node at a given position from the doubly linked list
    if head is None:
        print("Doubly linked list is empty")
        return None

    if position < 0:
        print("Invalid position")
        return head

    if position == 0:
        if head.next:
            head.next.prev = None
        return head.next

    current = head
    count = 0
    while current and count < position:
        current = current.next
        count += 1

    if current is None:
        print("Position out of range")
        return head

    if current.next:
        current.next.prev = current.prev
    if current.prev:
        current.prev.next = current.next

    del current
    return head

def delete_at_end(head):
    # Delete the last node from the end of the doubly linked list
    if head is None:
        print("Doubly linked list is empty")
        return None

    if head.next is None:
        return None

    current = head
    while current.next.next:
        current = current.next

    del_node = current.next
    current.next = None
    del del_node
    return head




