
class gapBuffer:
    def __init__(self, size):
        self.size = size
        self.gap_size = 10
        self.buffer = ['_'] * self.size
        self.gap_start = 0
        self.gap_end = self.gap_size

    def grow(self, amount, position):
            # Increasing the size of the gap
            self.buffer[position:position] = ['_'] * amount
            self.size += amount
            self.gap_end += amount
            self.gap_size += amount

    def right(self, position):
        while position > self.gap_start:
            if self.gap_end >= len(self.buffer):
                break
            self.buffer[self.gap_start] = self.buffer[self.gap_end]
            self.buffer[self.gap_end] = '_'

            self.gap_start += 1
            self.gap_end += 1
            print("moving right")

    def left(self, position):
         while position < self.gap_start:
            self.gap_end -= 1
            self.gap_start -= 1  
            self.buffer[self.gap_end] = self.buffer[self.gap_start]
            self.buffer[self.gap_start] = '_'
            print("moving left")

    # way to keep position and gap in sync
    def move_position(self, position):
        if self.gap_size == 0: # Bug fix, stop if from moving on empy buffer
            self.grow(5, self.gap_start)
        if position < self.gap_start:
            self.left(position)
        else:
            self.right(position)

    def insert(self, position, input):
        if position != self.gap_start:
             self.move_position(position)
        for char in input:
            if self.gap_start >= self.gap_end:
                self.grow(5, self.gap_start)
            self.buffer[self.gap_start] = char
            self.gap_start += 1
            self.gap_size -= 1
            self.gap_end = self.gap_start + self.gap_size

            print(self.buffer)

    # simular to move left, but increases the gap size
    def delete(self, position):
        if position != self.gap_start: # Always be positiond at the gap_start
            self.move_position(position)

        if self.gap_start == 0: # Prevent deletion before the start of the buffer
            return None

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






