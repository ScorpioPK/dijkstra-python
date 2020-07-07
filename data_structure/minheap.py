import numpy


class MinHeap:
    def __init__(self):
        self._array = [0]
        self._positions = [] #vector that holds the heap positions of nodes
        self._node_numbers = [0] #vector that holds the numbers of the nodes on each heap position
        self._size = 0

    def init_heap(self, dist, node_number, node_count):
        self.__init__()
        self._node_numbers = [-1] * (node_count+1)
        self._node_numbers[1] = node_number
        self._positions = [-1] * (node_count+1)
        self._positions[node_number] = 1
        self._array = [-1]
        self._array.append(dist)
        self._size = 1

    def insert(self, dist, node_number):
        self._size += 1
        self._array.append(dist)
        self._node_numbers[self._size] = node_number
        self._positions[node_number] = self._size
        self._move_up(self._size)

    def switch(self, pos1, pos2):
        tmp = self._array[pos1]
        self._array[pos1] = self._array[pos2]
        self._array[pos2] = tmp

        tmp = self._positions[self._node_numbers[pos1]]
        self._positions[self._node_numbers[pos1]] = self._positions[self._node_numbers[pos2]]
        self._positions[self._node_numbers[pos2]] = tmp

        tmp = self._node_numbers[pos1]
        self._node_numbers[pos1] = self._node_numbers[pos2]
        self._node_numbers[pos2] = tmp

    def decrease_key(self, node_number, new_value):
        self._array[self._positions[node_number]] = new_value
        self._move_up(self._positions[node_number])

    def update(self, node_number, new_value):
        old_value = self._array[self._positions[node_number]]
        self._array[self._positions[node_number]] = new_value
        if old_value > new_value:
            self._move_up(self._positions[node_number])
        else:
            self._move_down(self._positions[node_number])

    def pop_min(self):
        if self._size == 0:
            return [-1, -1]
        elif self._size == 1:
            ret_val = self._array[1]
            ret_pos = self._node_numbers[1]
            self._array.pop()
            self._node_numbers.pop()
            self._size -= 1
            return [ret_val, ret_pos]
        else:
            ret_val = self._array[1]
            ret_pos = self._node_numbers[1]
            self._array[1] = self._array[self._size]
            self._node_numbers[1] = self._node_numbers[self._size]
            self._positions[self._node_numbers[self._size]] = 1
            self._size -= 1
            self._array.pop()
            self._node_numbers.pop()
            self._move_down(1)
            return [ret_val, ret_pos]

    # this assumes that the initial positions of elements are node numbers
    def build_heap(self, input_list):
        for i in range(1, len(input_list) + 1):
            self._node_numbers.append(i - 1)
            self._positions.append(i)
        pos = len(input_list) // 2
        self._size = len(input_list)
        self._array = [0]
        self._array.extend(input_list)

        while pos > 0:
            self._move_down(pos)
            pos = pos - 1

    def get_value_for_node(self, pos):
        if self._positions[pos] == -1:
            return -1
        return self._array[self._positions[pos]]

    def get_values_as_list(self):
        return self._array[1:]

    def get_positions_as_list(self):
        return self._positions

    def get_node_numbers_as_list(self):
        return self._node_numbers[1:]

    def _min_child(self, pos):
        if pos * 2 + 1 > self._size:
            return pos * 2
        else:
            if self._array[pos*2] < self._array[pos*2+1]:
                return pos * 2
            else:
                return pos * 2 + 1

    def _move_up(self, pos):
        while pos // 2 > 0:
            if self._array[pos] < self._array[pos // 2]:
                self.switch(pos, pos // 2)
            pos = pos // 2

    def _move_down(self, pos):
        while (pos * 2) <= self._size:
            mc = self._min_child(pos)
            if self._array[pos] > self._array[mc]:
                self.switch(pos, mc)
            pos = mc
