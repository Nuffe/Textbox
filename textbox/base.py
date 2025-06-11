import time
import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 600))
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()
textInput = []

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                textInput.pop()
            elif event.key == pygame.K_SPACE:
                textInput.append(' ')
            elif event.key == pygame.K_TAB:
                textInput.append('\t')
            elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                textInput.clear()
            else:
                keyPressed = pygame.key.name(event.key)
                textInput.append(keyPressed)


    # keyboard event handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    
    screen.fill((30, 30, 30))
    
    if time.time() % 1.2 > 0.6:
        cursor = pygame.draw.rect(screen, (50, 255, 255), (50, 50, 3, 20))
    
    if len(textInput) > 0:
        textOutput = ''.join(textInput)
        key = font.render(textOutput, True, (255, 255, 255))
        screen.blit(key, (50, 50))

    clock.tick(60)
    pygame.display.flip()

pygame.quit()

