import time
import pygame
from  gap_buffer import gapBuffer
from  linkedList import *
import tkinter as tk
from tkinter import filedialog as fd
from undo import *

class TextEditor:
    def __init__(self):
        pygame.init()
        self.cursorPos = 0
        self.positionX = 50
        self.positionY = 24
        self.pointerX = 0
        self.pointerY = 0
        self.list = LineList()
        self.currentNode = self.list.append(gapBuffer(10))
        self.screen = pygame.display.set_mode((1000, 600))
        self.font = pygame.font.SysFont(["cascadiacoderegular", "cascadiamonoregular", "monospace"], 20)
        self.loadButton = pygame.Rect(20, 0, 50, self.font.get_height())
        self.saveButton = pygame.Rect(100, 0, 50,  self.font.get_height())
        self.running = True
        self.filename = ""
        self.undolist = UndoList(self.currentNode, self.list)

    def main(self):
        pygame.display.set_caption("Project MilkBox")
        icon = pygame.image.load("assets/milk-carton.png")
        pygame.display.set_icon(icon)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Left mouse click
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx,my = event.pos
                    if self.loadButton.collidepoint(mx,my):
                        self.loadDialog()
                    elif self.saveButton.collidepoint(mx,my):
                        self.saveDialog()
                # Handles the key events
                elif event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_BACKSPACE:
                        self.backspace()
                        
                    elif event.key == pygame.K_RETURN:
                        self.pressReturn()
                    elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        self.printout()  # Debugging
                    elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        if self.filename != "":
                            self.save(self.filename)
                    elif event.key == pygame.K_f and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        self.loadDialog()
                    elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        if( self.undolist.size > 0):
                            self.cursorPos, self.pointerY, self.currentNode = self.undolist.undoAction()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_DOWN:
                        self.pressDown()
                    elif event.key == pygame.K_UP:
                        self.pressUp()
                    elif event.key == pygame.K_LEFT:
                        self.pressLeft()
                    elif event.key == pygame.K_RIGHT:
                        self.pressRight()
                    else:
                        self.write(event)
                        
            self.screen.fill((30, 30, 30))
            self.toolBar()
            if self.pointerY < self.list.size:    # Highlight the current line
                pygame.draw.rect(self.screen, (50, 50, 50), (self.positionX - 50, self.positionY + self.pointerY * self.font.get_height(), 1000, self.font.get_height()), 0)
            self.textCursor()
            self.renderText()
            self.lineNumbers()
            pygame.display.flip()
        pygame.quit()


    def backspace(self):
        if( self.cursorPos > 0 and self.pointerY < self.list.size):
            old_cursor = self.cursorPos
            old_lineY   = self.pointerY
            deleted = self.currentNode.data.delete(self.cursorPos)  # Delete the character before the cursor
            self.undolist.append(deleted, old_cursor, self.currentNode, old_lineY, "delete_char")
            
            self.cursorPos -= 1
        elif self.pointerY > 0: # Jumps up a line if at start, and remove node if empty
            targetNode = self.currentNode
            prev_node = self.currentNode.prev
            self.pointerY   -= 1
            self.currentNode = prev_node
            if(targetNode.data.textContent() == ""):
                self.undolist.append("", 0, targetNode, self.pointerY, "delete_line")
                self.list.remove(targetNode)
                self.cursorPos = len(self.currentNode.data.textContent())

    def pressReturn(self):
        old_cursor = self.cursorPos
        old_line   = self.pointerY

        self.currentNode = self.list.insert_after(self.currentNode, gapBuffer(10))
        self.undolist.append("", old_cursor, self.currentNode, old_line, "add_line")
        self.pointerY += 1
        self.cursorPos = 0

    def pressDown(self):
        old_cursor = self.cursorPos
        old_line   = self.pointerY
        self.pointerY += 1
        if self.pointerY >= self.list.size: # Creates new line if at the end
            self.currentNode = self.list.insert_after(self.currentNode, gapBuffer(10))
            self.undolist.append("", old_cursor, self.currentNode, old_line, "add_line")

        else:
            self.currentNode = self.currentNode.next
            self.cursorPos = min(self.cursorPos, len(self.currentNode.data.textContent()))    

    def pressUp(self):
        if self.pointerY > 0:
            self.pointerY -= 1
            self.currentNode = self.currentNode.prev  if self.currentNode.prev else self.currentNode
            self.cursorPos = min(self.cursorPos, len(self.currentNode.data.textContent()))

    def pressLeft(self):
        if self.cursorPos > 0:
            self.cursorPos -= 1
        elif self.pointerY > 0: # Jump up if at start
            self.pointerY -= 1
            self.currentNode = self.currentNode.prev if self.currentNode.prev else self.currentNode
            self.cursorPos = len(self.currentNode.data.textContent())

    def pressRight(self):
        if self.cursorPos < len(self.currentNode.data.textContent()):
            self.cursorPos += 1
        elif self.pointerY < self.list.size - 1: # Jump down if at end
            self.pointerY += 1
            self.currentNode = self.currentNode.next if self.currentNode.next else self.currentNode
            self.cursorPos = 0
            
    def write(self, event):
        character = event.unicode       
        if character:

            if self.pointerY >= self.list.size:
                self.currentNode = self.list.insert_after(self.currentNode, gapBuffer(10))
            self.currentNode.data.insert(self.cursorPos, character)
            old_lineY   = self.pointerY
            self.cursorPos += 1
    
            # Stop overflowing the line
            # Get new X value based on the new character
            tempBuf = self.currentNode.data
            line_text = tempBuf.textContent()           
            self.pointerX = self.positionX + self.font.size(line_text[:self.cursorPos])[0]
            if self.pointerX > 950:  # If the line is too long, move to the next line
                tempBuf.delete(self.cursorPos -1)  
                self.pointerY += 1
                if self.pointerY >= self.list.size:
                    self.currentNode = self.list.insert_after(self.currentNode, gapBuffer(10))
                self.cursorPos = 0
                self.currentNode.data.insert(self.cursorPos, character) 
                self.cursorPos = 1
            new_cursor = self.cursorPos
            self.undolist.append(character, new_cursor, self.currentNode, old_lineY, op_type=("insert_space" if character == " " else "insert_char"))

    def textCursor(self):
        bufferText = self.currentNode.data.textContent()  # Get the text content of the current line
        beforeCursorText = bufferText[:self.cursorPos]  # Text before the cursor position
        self.pointerX = self.positionX + self.font.size(beforeCursorText)[0]  #X position of the cursor based on pixels before it
        pointerHeight = self.font.get_height()
        if time.time() % 1.2 > 0.6:   #Flicker time    
            pygame.draw.rect(self.screen, (255,255,255), (self.pointerX,  self.positionY + self.pointerY * self.font.get_height(), 2, pointerHeight))
            
    # Renders the text from each line
    def renderText(self):
            node = self.list.head   # Start with the head node
            row = 0
            while node:
                buffer = node.data  
                text = buffer.textContent()
                if text:
                    surface = self.font.render(text, True, (255,255,255))
                    self.screen.blit(surface, (self.positionX, self.positionY + row * self.font.get_height()))
                row += 1
                node = node.next

    def lineNumbers(self):
        for i in range(self.list.size):
            line_number = str(i + 1)
            if(i == (self.pointerY)): 
                line_number_surface = self.font.render(line_number, True, (250, 250, 250))
            else:
                line_number_surface = self.font.render(line_number, True, (100, 100, 100))
                
            if( i < 9):
                self.screen.blit(line_number_surface, (self.positionX - 30, self.positionY + i * self.font.get_height()))
            else:
                self.screen.blit(line_number_surface, (self.positionX - 43, self.positionY + i * self.font.get_height()))


    def load(self, filename):
        self.list.clear()  # Clear the existing list
        self.currentNode = self.list.append(gapBuffer(10))
        count = 0
        self.cursorPos = 0
        self.positionX = 50
        self.positionY = 24
        self.pointerX = 0
        self.pointerY = 0
        with open(filename) as file:
            for raw in file:
                line = raw.rstrip("\n")
                if count == 0: # Make it start  from the first line
                    node = self.list.head
                    count += 1
                else:
                    node = self.list.append(gapBuffer(10))
                self.cursorPos = 0
                for char in line:
                    node.data.insert(self.cursorPos, char)
                    self.cursorPos += 1
        self.cursorPos = 0
    
    def save(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            node = self.list.head
            while node:
                buffer = node.data
                text = buffer.textContent()
                file.write(text + "\n")
                node = node.next
        
    def toolBar(self):
        pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, 1000, self.font.get_height()), 0)
        pygame.draw.rect(self.screen, (255,255, 255), self.loadButton)
        pygame.draw.rect(self.screen, (255,255,255), self.saveButton)

        self.screen.blit(self.font.render("Load", True, (25,25,25)),(self.loadButton.x, 0))
        self.screen.blit(self.font.render("Save", True, (0,0,0)),(self.saveButton.x, 0))

    def loadDialog(self):
        app = tk.Tk()
        app.withdraw()
        filetypes = [ ("Text files", "*.txt") ]
        filename = fd.askopenfilename(
            parent= app,
            filetypes= filetypes,
        )
        app.destroy()
        if  filename:
            self.load(filename)
            self.filename = filename

        
    def saveDialog(self):
        app = tk.Tk()
        app.withdraw()
        filetypes = [ ("Text files", "*.txt") ]
        filename = fd.asksaveasfilename(
            parent= app,
            filetypes= filetypes,
        )
        app.destroy()
        if  filename:
            self.save(filename)
    
    def printout(self):
        node = self.list.head
        print("____________________________________________")
        while node:
            print("name: ", node, "data: ", node.data.textContent())
            node = node.next
        print("____________________________________________")