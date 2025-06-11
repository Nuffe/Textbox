import time
import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 600))
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

textInput = []
cursorPos = 0
positionX = 50
positionY = 50

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                textInput.pop()
                cursorPos -= 1
            elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                textInput.clear()
                cursorPos = 0
            elif event.key == pygame.K_ESCAPE:
                running = False
            else:
                character = event.unicode       
                if character:
                    textInput.insert(cursorPos, character)
                    cursorPos += 1

    screen.fill((30, 30, 30))

    if time.time() % 1.2 > 0.6:                              #Flicker time
        textBeforePoint = "".join(textInput[:cursorPos])     #Grabs all before cursor position
        pointerX = positionX + font.size(textBeforePoint)[0] #size givs the pixel size of the string and puts caret at the end
        pointerHeight = font.get_height()
        pygame.draw.rect(screen, (255,255,255), (pointerX, positionY, 2, pointerHeight))
    
    if len(textInput) > 0:
        textOutput = "".join(textInput)
        key = font.render(textOutput, True, (255, 255, 255))
        screen.blit(key, (positionX, positionY))

    clock.tick(60)
    pygame.display.flip()

pygame.quit()

