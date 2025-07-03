
class gapBuffer:
    def __init__(self, size):
        self.size = size
        self.gap_size = 5
        self.buffer = ['_'] * self.size
        self.gap_start = 0
        self.gap_end = self.gap_start + self.gap_size
       # print(self.buffer)


    # Grow the gap at position, new array is made and old data is copied over
    def grow(self, growthSize: int, position):
        a = self.buffer[position:self.size]
        self.buffer[position:position+growthSize] = ['_'] * growthSize
        self.buffer[position+growthSize:position+growthSize + self.size - position] = a

        self.size += growthSize
        self.gap_size += growthSize
        self.gap_end = self.gap_start + self.gap_size

    # moves the gap right by changing the character to "", array size is not changed
    def right(self, position):
        while position > self.gap_start:
            self.buffer[self.gap_start] = self.buffer[self.gap_end]
            self.buffer[self.gap_end] = '_' 
            self.gap_start += 1
            self.gap_end   += 1

    def left(self, position):
         while position < self.gap_start:
            self.gap_end   -= 1
            self.gap_start -= 1  
            self.buffer[self.gap_end] = self.buffer[self.gap_start]
            self.buffer[self.gap_start] = '_'

    # way to keep position and gap in sync
    def move_position(self, position):
        if self.gap_size == 0: # Bug fix, stop if from moving on empy buffer
            self.grow(5, self.gap_start)
        if position < self.gap_start:
            self.left(position)
        else:
            self.right(position)


    def insert(self, position, char):
        if self.gap_size == 0:
            self.grow(5, position)
        self.move_position(position)
        self.buffer[self.gap_start] = char
        self.gap_start += 1
        self.gap_size -= 1
        self.gap_end = self.gap_start + self.gap_size


    # simular to move left, but increases the gap size
    def delete(self, position):         
        self.move_position(position)
        self.gap_start -= 1
        deleted = self.buffer[self.gap_start]
        self.buffer[self.gap_start] = '_'  
        self.gap_size += 1
        self.gap_end = self.gap_start + self.gap_size
        return deleted
    


    # Returns the text content, excluding the gap
    def textContent(self):
        text =  self.buffer[:self.gap_start] + self.buffer[self.gap_end:]
        return  "".join(text).rstrip("_")
    
    # Printout that show a the gap more clearly
    def __repr__(self):
        before = "".join(self.buffer[:self.gap_start])
        gap_len = self.gap_end - self.gap_start
        gap     = "_" * gap_len          # or use some other symbol
        after   = "".join(self.buffer[self.gap_end:])
        return f"{before}|{gap}|{after}"






