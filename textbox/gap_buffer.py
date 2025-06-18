
class gapBuffer:
    def __init__(self, size):
        self.size = size
        self.gap_size = 5
        self.buffer = ['']*5
        self.gap_start = 0
        self.gap_end = self.gap_size -1
        print(self.buffer)


    # Grow the gap at position, new array is made and old data is copied over
    def grow(self, growthSize: int, position):
        a = self.buffer[position:self.size]
        self.buffer[position:position+growthSize] = ['' for i in range(growthSize)]
        self.buffer[position+growthSize:position+growthSize+ self.size - position] = a

        self.size += growthSize
        self.gap_end += growthSize

    # moves the gap right by changing the character to "", array size is not changed
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

    # way to keep position and gap in sync
    def move_position(self, position):
        if position < self.gap_start:
            self.left(position)
        else:
            self.right(position)

    def insert(self, position, character):
        if self.gap_end == self.gap_start:
            self.grow(5, position)
        self.move_position(position)
        self.buffer[self.gap_start] = character
        self.gap_start += 1
        self.gap_size -= 1

        print(self.buffer)

    # simular to move left, but increases the gap size
    def delete(self, position):         
        if position != self.gap_start:
            self.move_position(position +1)
            self.gap_start -= 1
            self.buffer[self.gap_start] = ''        

    # Returns the text content, excluding the gap
    def textContent(self):
        return "".join(self.buffer[:self.gap_start]) + "".join(self.buffer[self.gap_end:])

    # Printout that show a the gap more clearly
    def __repr__(self):
        before = "".join(self.buffer[:self.gap_start])
        gap_len = self.gap_end - self.gap_start
        gap     = "_" * gap_len          # or use some other symbol
        after   = "".join(self.buffer[self.gap_end:])
        return f"{before}|{gap}|{after}"






