import pygame 

pygame.init()

WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_model({WIDTH, HEIGHT})
timer = pygame.time.Clock()
fps = 120
font = pygame.front.Front('freesanbold.ttf', 20)

run = True 
while run:
    timer.tick(fps)
    screen.fill('black')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run == False 

    pygame.display.flip()
pygame.quit()
 