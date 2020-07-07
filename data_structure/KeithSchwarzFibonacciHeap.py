#Java implementation here: https://keithschwarz.com/interesting/code/?dir=fibonacci-heap
#I translated it to Python

class KFib:
    class Node:
        # Renamed member priority to value and changed parameter order to match other implementations
        def __init__(self, key, value):
            self.degree = 0
            self.is_marked = False
            self.next = self.prev = self
            self.parent = self.child = None
            self.value = value
            self.key = key

    min = None
    size = 0

    def __init__(self):
        self.min = None
        self.size = 0

    # method name changed from enqueue to match other implementations
    def insert(self, key, value):
        if key is None:
            return None
        result = self.Node(key, value)
        self.min = KFib.merge_lists(self.min, result)
        self.size += 1
        return result

    @staticmethod
    def merge(one, two):
        result = KFib()
        result.min = KFib.merge_lists(one.min, two.min)
        result.size = one.size + two.size
        one.size = two.size = 0
        one.min = None
        two.min = None
        return result

    # method name changed from dequeue_min to match other implementations
    def extract_min(self):
        if self.min is None:
            return None
        self.size -= 1
        min_elem = self.min
        if self.min.next == self.min:
            self.min = None
        else:
            self.min.prev.next = self.min.next
            self.min.next.prev = self.min.prev
            self.min = self.min.next
        if min_elem.child is not None:
            curr = min_elem.child
            curr.parent = None
            curr = curr.next
            while curr != min_elem.child:
                curr.parent = None
                curr = curr.next
        self.min = KFib.merge_lists(self.min, min_elem.child)
        if self.min is None:
            return min_elem
        tree_table = [None]*self.size
        to_visit = []
        curr = self.min
        while len(to_visit) == 0 or to_visit[0] != curr:
            to_visit.append(curr)
            curr = curr.next
        for curr in to_visit:
            while True:
                if tree_table[curr.degree] is None:
                    tree_table[curr.degree] = curr
                    break
                other = tree_table[curr.degree]
                tree_table[curr.degree] = None
                minimum = other if other.key < curr.key else curr
                maximum = curr if other.key < curr.key else other
                maximum.next.prev = maximum.prev
                maximum.prev.next = maximum.next
                maximum.next = maximum.prev = maximum
                minimum.child = KFib.merge_lists(minimum.child, maximum)
                maximum.parent = minimum
                maximum.is_marked = False
                minimum.degree += 1
                curr = minimum
            if curr.key <= self.min.key:
                self.min = curr
        return min_elem

    def decrease_key(self, node, new_key):
        if new_key > node.key:
            return
        self.decrease_key_unchecked(node, new_key)

    def delete(self, node):
        self.decrease_key_unchecked(node, -1)
        self.extract_min()

    @staticmethod
    def merge_lists(one, two):
        if one is None and two is None:
            return None
        elif one is not None and two is None:
            return one
        elif one is None and two is not None:
            return two
        else:
            one_next = one.next
            one.next = two.next
            one.next.prev = one
            two.next = one_next
            two.next.prev = two
            return one if one.key < two.key else two

    def decrease_key_unchecked(self, node, new_key):
        node.key = new_key
        if node.parent is not None and node.key <= node.parent.key:
            self.cut_node(node)
        if node.key <= self.min.key:
            self.min = node

    def cut_node(self, node):
        node.is_marked = False
        if node.parent is None:
            return
        if node.next != node:
            node.next.prev = node.prev
            node.prev.next = node.next
        if node.parent.child == node:
            if node.next != node:
                node.parent.child = node.next
            else:
                node.parent.child = None
        node.parent.degree -= 1
        node.prev = node.next = node
        self.min = KFib.merge_lists(self.min, node)
        if node.parent.is_marked:
            self.cut_node(node.parent)
        else:
            node.parent.is_marked = True
        node.parent = None
