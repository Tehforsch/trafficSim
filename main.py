import pygame
import constants
import traffic
import renderer

# initialize game engine
pygame.init()
# set screen width/height and caption
size = [constants.WIDTH, constants.HEIGHT]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("")
# initialize clock. used later in the loop.
clock = pygame.time.Clock()

def mainloop():
    done = False
    step = 0

    _traffic = traffic.Traffic.getSimpleTraffic2()

    while done == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill((0, 0, 0)) 

        renderer.drawTraffic(screen, _traffic)
        _traffic.handle()

        pygame.display.update()
        clock.tick(50)
    pygame.quit()

mainloop()
