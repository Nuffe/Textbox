import time
import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 600))
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

textInput = []
textLines = [[]] 
cursorPos = 0
positionX = 50
positionY = 50
pointerX = 0
pointerY = 0

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        # Handle key events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if( cursorPos > 0 and pointerY < len(textLines)):
                    textLines[pointerY].pop()
                    cursorPos -= 1
                else:
                    if pointerY > 0:   # Same logic as if backspace at the start of a line
                        pointerY -= 1
                        cursorPos = len(textLines[pointerY])
            elif event.key == pygame.K_RETURN:
                textLines.append([])                 
                pointerY += 1
                cursorPos = 0
            elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                textLines[pointerY].clear()
                cursorPos = 0
            elif event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_DOWN:
                pointerY += 1
                if pointerY >= len(textLines): # Creates new line if at the end
                    textLines.append([])
                cursorPos = min(cursorPos, len(textLines[pointerY]))
            elif event.key == pygame.K_UP:
                pointerY -= 1
                if pointerY < 0:
                    pointerY = 0
                cursorPos = min(cursorPos, len(textLines[pointerY]))
            elif event.key == pygame.K_LEFT:
                if cursorPos > 0:
                    cursorPos -= 1
                elif pointerY > 0: # Jump up if at start
                    pointerY -= 1
                    cursorPos = len(textLines[pointerY]) 
            elif event.key == pygame.K_RIGHT:
                if cursorPos < len(textLines[pointerY]):
                    cursorPos += 1
                elif pointerY < len(textLines) - 1: # Jump down if at end
                    pointerY += 1
                    cursorPos = 0
            else:
                character = event.unicode       
                if character:
                    textLines[pointerY].insert(cursorPos, character)
                    cursorPos += 1
                    if pointerX > 500:                      
                        pointerY += 1
                        cursorPos = 0
                        if pointerY >= len(textLines):
                            textLines.append([])
                
    screen.fill((30, 30, 30))

    # Creating the text pointer
    textBeforePointLines = "".join(textLines[pointerY][:cursorPos]) #Grabs all before cursor position
    pointerX = positionX + font.size(textBeforePointLines)[0]  #X position of the cursor based on pixels before it
    pointerHeight = font.get_height()
    if time.time() % 1.2 > 0.6:   #Flicker time    
        pygame.draw.rect(screen, (255,255,255), (pointerX,  positionY + pointerY * font.get_height(), 2, pointerHeight))
       
    # Render the text lines
    for i, line in enumerate(textLines):
        if len(line) == 0:
            continue
        textOutput = "".join(line)
        key = font.render(textOutput, True, (255, 255, 255))
        screen.blit(key, (positionX, positionY + i * font.get_height()))

    clock.tick(60)
    pygame.display.flip()

pygame.quit()

