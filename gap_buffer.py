
class gapBuffer:
    def __init__(self, size):
        self.size = size
        self.gap_size = 5
        self.buffer = ['_' for i in range(size)]
        self.gap_start = 0
        self.gap_end = self.gap_size - self.gap_start -1
        print(self.buffer)


    def grow(self, k: int):
        self.buffer[self.gap_start : self.gap_start] = [''] * k
        self.gap_end += k
        self.gap_size += k


    def right(self, position):
        while position > self.gap_start:
            self.gap_start += 1
            self.gap_end   += 1
            self.buffer[self.gap_start -1] = self.buffer[self.gap_end]
            self.buffer[self.gap_end] = ''

    def left(self, position):
         while position < self.gap_start:
            self.gap_end   -= 1
            self.gap_start -= 1  
            self.buffer[self.gap_end +1] = self.buffer[self.gap_start]
            self.buffer[self.gap_start] = ''

    def move_position(self, position):
        if position < self.gap_start:
            self.left(position)
        else:
            self.right(position)

    def insert(self, position, character):

        if self.gap_end == self.gap_start:
            self.grow(10)
            
        self.move_position(position)
        self.buffer[position] = character
        self.gap_start += 1
        self.gap_size -= 1

        print(self.buffer)

    def __repr__(self):
        before = "".join(self.buffer[:self.gap_start])
        gap_len = self.gap_end - self.gap_start
        gap     = "_" * gap_len          # or use some other symbol
        after   = "".join(self.buffer[self.gap_end:])
        return f"{before}|{gap}|{after}"


buffer = gapBuffer(10)
buffer.insert(0, 'C')
buffer.insert(1, 'a')
buffer.insert(2, 'l')
buffer.insert(3, '*')
buffer.insert(4, 'p')
buffer.insert(5, 'a')
buffer.insert(6, 'u')
buffer.insert(2, 'r')
buffer.insert(2, 'r')
buffer.insert(2, 'r')
print(buffer)


