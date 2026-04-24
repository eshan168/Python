class Node:
    def __init__(self,data,next=None):
        self.data = data
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if self.head == None:
            self.head = new_node
            return
        cur = self.head
        while cur.next != None:
            cur = cur.next
        cur.next = new_node

    def pop(self):
        cur = self.head
        while cur.next != None:
            cur = cur.next
        prev = cur.data
        cur.data = None
        return prev
    
    def toList(self):
        cur = self.head
        List = []
        while cur != None:
            List.append(cur.data)
            cur = cur.next
        return List
    
    def print(self):
        cur = self.head
        while cur.next != None:
            print(cur.data)
            cur = cur.next
        print(cur.data)







