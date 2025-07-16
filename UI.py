import pygame, sys
from pygame.locals import QUIT


pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen_width = 700
screen_height = 700
dimensions = (28, 28)

SCREEN = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('super duper cool awesomesauce ai')
SCREEN.fill((255, 255, 255))

mouse = pygame.mouse
clock = pygame.time.Clock()

grid = {(x, y):False for x in range(dimensions[0]) for y in range(dimensions[1])}

def drawGrid(w, h, d = dimensions):
    size = (int(w/d[0]), int(h/d[1]))
    for x in range(0, w, size[0]):
        for y in range(0, h, size[1]):
            rect = pygame.Rect(x, y, size[0], size[1])
            pygame.draw.rect(SCREEN, (0,0,0), rect, 1)

def setBox(p, color, d=dimensions, w=screen_width, h=screen_height):
    x, y = p
    size = (int(w/d[0]), int(h/d[1]))
    boxx, boxy = ( int(x/size[0]), int(y/size[1]) )
    if color != WHITE:
        if grid[(boxx, boxy)]:
            return None
        grid[( boxx, boxy )] = True
        rect = pygame.Rect(boxx*size[0], boxy*size[1], size[0], size[1])
    else:
        grid[( boxx, boxy )] = False
        rect = pygame.Rect(boxx*size[0]+1, boxy*size[1]+1, size[0] - 2, size[1] - 2)
    pygame.draw.rect(SCREEN, color, rect)
    #drawGrid(w, h)


def runRender():
    drawGrid(screen_width, screen_height)
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if mouse.get_pressed()[0]:
            mouse_pos = mouse.get_pos()
            setBox(mouse_pos, BLACK)
        if mouse.get_pressed()[2]:
            mouse_pos = mouse.get_pos()
            setBox(mouse_pos, WHITE)
        pygame.display.update()