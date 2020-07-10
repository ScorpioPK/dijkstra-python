import numpy


class MinHeap:
    class Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value

    def __init__(self):
        self._array = [0]
        self._positions = [] #vector that holds the heap positions of nodes
        self._size = 0

    def init_heap(self, node_count):
        self.__init__()
        self._positions = [-1] * (node_count+1)

    def insert(self, key, value):
        new_node = self.Node(key, value)
        self._size += 1
        self._array.append(new_node)
        self._positions[new_node.value] = self._size
        self._move_up(self._size)
        return new_node

    def switch(self, pos1, pos2):
        tmp = self._array[pos1]
        self._array[pos1] = self._array[pos2]
        self._array[pos2] = tmp

        tmp = self._positions[self._array[pos1].value]
        self._positions[self._array[pos1].value] = self._positions[self._array[pos2].value]
        self._positions[self._array[pos2].value] = tmp

    def decrease_key(self, node, new_key):
        node.key = new_key
        self._move_up(self._positions[node.value])

    def extract_min(self):
        if self._size == 0:
            return None
        elif self._size == 1:
            return_node = self._array.pop()
            self._size -= 1
            return return_node
        else:
            return_node = self._array[1]
            self._array[1] = self._array[self._size]
            self._positions[self._array[1].value] = 1
            self._size -= 1
            self._array.pop()
            self._move_down(1)
            return return_node

    def _min_child(self, pos):
        if pos * 2 + 1 > self._size:
            return pos * 2
        else:
            if self._array[pos*2].key < self._array[pos*2+1].key:
                return pos * 2
            else:
                return pos * 2 + 1

    def _move_up(self, pos):
        while pos // 2 > 0:
            if self._array[pos].key < self._array[pos // 2].key:
                self.switch(pos, pos // 2)
            pos = pos // 2

    def _move_down(self, pos):
        while (pos * 2) <= self._size:
            mc = self._min_child(pos)
            if self._array[pos].key > self._array[mc].key:
                self.switch(pos, mc)
            pos = mc
