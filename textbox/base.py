import time
import pygame
from .gap_buffer import gapBuffer
from  linkedList import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()

    textLines = []
    cursorPos = 0
    positionX = 50
    positionY = 50
    pointerX = 0
    pointerY = 0
    headNode = Node(gapBuffer(100))  # Create the head node with an initial gap buffer
    currentNode = headNode
    nodeCount = 1

   # load(textLines)  # Load initial text from file

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            # Handle key events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if( cursorPos > 0 and pointerY < nodeCount):
                        currentNode.data.delete(cursorPos - 1 )  # Delete the character before the cursor
                        cursorPos -= 1
                    else:
                        if pointerY > 0:   # Same logic as if backspace at the start of a line
                            pointerY -= 1
                            cursorPos = len(currentNode.data.textContent())
                elif event.key == pygame.K_RETURN:
                    insert_after_node(currentNode, gapBuffer(100))  # Insert a new node after the current one
                    currentNode = currentNode.next
                    nodeCount += 1           
                    pointerY += 1
                    cursorPos = 0
                elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    currentNode.data.clear()
                    cursorPos = 0
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_DOWN:
                    pointerY += 1
                    if pointerY >= nodeCount: # Creates new line if at the end
                        insert_after_node(currentNode, gapBuffer(100))
                        nodeCount += 1
                    currentNode = currentNode.next if currentNode.next else currentNode
                    cursorPos = min(cursorPos, len(currentNode.data.textContent()))
                elif event.key == pygame.K_UP:
                    print("UP", pointerY, nodeCount)
                    if pointerY > 0:
                        pointerY -= 1
                        currentNode = currentNode.prev
                    cursorPos = min(cursorPos, len(currentNode.data.textContent()))
                elif event.key == pygame.K_LEFT:
                    if cursorPos > 0:
                        cursorPos -= 1
                    elif pointerY > 0: # Jump up if at start
                        pointerY -= 1
                        cursorPos = len(currentNode.data.textContent())
                elif event.key == pygame.K_RIGHT:
                    if cursorPos < len(currentNode.data.textContent()):
                        cursorPos += 1
                    elif pointerY < nodeCount - 1: # Jump down if at end
                        pointerY += 1
                        cursorPos = 0
                else:
                    character = event.unicode       
                    if character:
                        if pointerY >= nodeCount:
                                insert_after_node(currentNode, gapBuffer(100))
                                currentNode = currentNode.next
                                nodeCount += 1
                        currentNode.data.insert(cursorPos, character) 
                        cursorPos += 1

                        # Stop overflowing the line
                        # Get new X value based on the new character
                        tempBuf = currentNode.data
                        line_text = tempBuf.textContent()           
                        pointerX = positionX + font.size(line_text[:cursorPos])[0]

                        if pointerX > 950:  # If the line is too long, move to the next line
                            tempBuf.delete(cursorPos -1)  
                            pointerY += 1
                            if pointerY >= nodeCount:
                                insert_after_node(currentNode, gapBuffer(100))
                                nodeCount += 1
                            currentNode = currentNode.next if currentNode.next else currentNode
                            cursorPos = 0
                            currentNode.data.insert(cursorPos, character) 
                            cursorPos = 1

                    
        screen.fill((30, 30, 30))

        # Highlight the current line
        if pointerY < nodeCount:
            pygame.draw.rect(screen, (50, 50, 50), (positionX - 50, positionY + pointerY * font.get_height(), 1000, font.get_height()), 0)


        # Creating the text cursor/caret pointer
        buffer = currentNode.data
        bufferText = buffer.textContent()  # Get the text content of the current line
        beforeCursorText = bufferText[:cursorPos]  # Text before the cursor position
        pointerX = positionX + font.size(beforeCursorText)[0]  #X position of the cursor based on pixels before it
        pointerHeight = font.get_height()
        if time.time() % 1.2 > 0.6:   #Flicker time    
            pygame.draw.rect(screen, (255,255,255), (pointerX,  positionY + pointerY * font.get_height(), 2, pointerHeight))
        
        # Render the text lines, line by line
        for i, buffer in enumerate(textLines):
            if len(buffer.textContent()) == 0:
                continue
            textOutput = buffer.textContent()  # Get the text content of the current line
            key = font.render(textOutput, True, (255, 255, 255))
            screen.blit(key, (positionX, positionY + i * font.get_height()))

        y = positionY
        node = headNode   # Start with the head node
        row = 0
        while node:
            buf = node.data   # your GapBuffer or whatever you called it
            text = buf.textContent()
            if text:
                surface = font.render(text, True, (255,255,255))
                screen.blit(surface, (positionX, y + row * font.get_height()))
            node = node.next
            row += 1


        # Render line numbers
        for i in range(nodeCount):
            line_number = str(i + 1)
            if(i == (pointerY)): 
                line_number_surface = font.render(line_number, True, (250, 250, 250))
            else:
                line_number_surface = font.render(line_number, True, (100, 100, 100))
                
            if( i < 9):
                screen.blit(line_number_surface, (positionX - 30, positionY + i * font.get_height()))
            else:
                screen.blit(line_number_surface, (positionX - 43, positionY + i * font.get_height()))

        pygame.display.flip()

    pygame.quit()



def load(textLines):
    with open('text.txt') as file:
        for line in file:
            textLines.append(gapBuffer(100))
            line = line.rstrip('\n')
            for char in line:
                textLines[-1].insert(len(textLines[-1].textContent()), char)