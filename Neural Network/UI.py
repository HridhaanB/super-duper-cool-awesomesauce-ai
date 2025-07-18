import pygame, sys
from pygame.locals import QUIT

pygame.init()
pygame.font.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen_width = 700
screen_height = 800
dimensions = (28, 28)

SCREEN = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('super duper cool awesomesauce ai')
SCREEN.fill(BLACK)

font = pygame.font.Font('freesansbold.ttf', 32)

mouse = pygame.mouse
clock = pygame.time.Clock()

grid = {(x, y): 0.0 for x in range(dimensions[0]) for y in range(dimensions[1])}


def drawGrid(w, h, d=dimensions):
    size = (int(w / d[0]), int(h / d[1]))
    for x in range(0, w, size[0]):
        for y in range(0, h, size[1]):
            rect = pygame.Rect(x, y, size[0], size[1])
            pygame.draw.rect(SCREEN, WHITE, rect, 1)


def setBox(p, erase, d=dimensions, w=screen_width, h=screen_height-100):
    boxx, boxy = mousePosToGrid(p)
    if not erase:
        if grid.get((boxx, boxy), 1) == 1:
            return None
        grid[(boxx, boxy)] = 1
        antiAlias(p)
        #colorGrid()
    else:
        #erase
        grid[(boxx, boxy)] = 0
        antiAlias((boxx, boxy))
        #colorGrid()
    # drawGrid(w, h)

def mousePosToGrid(pos):
    x, y = pos
    size = int(screen_width / dimensions[0]), int((screen_height-100) / dimensions[1])
    return int(x / size[0]), int(y / size[1])

def antiAlias(pos):
    x, y = mousePosToGrid(pos)
    for i in range(2):
        for x_pos in range(x-1, x+2):
            for y_pos in range(y-1, y+2):
                surrounding_vals = 0.7*grid.get((x_pos, y_pos), 0)
                surrounding_vals += 0.05*grid.get((x_pos+1, y_pos), 0)
                surrounding_vals += 0.05*grid.get((x_pos-1, y_pos), 0)
                surrounding_vals += 0.05*grid.get((x_pos, y_pos+1), 0)
                surrounding_vals += 0.05*grid.get((x_pos, y_pos-1), 0)
                surrounding_vals += 0.0125*grid.get((x_pos+1, y_pos+1), 0)
                surrounding_vals += 0.0125*grid.get((x_pos-1, y_pos+1), 0)
                surrounding_vals += 0.0125*grid.get((x_pos+1, y_pos-1), 0)
                surrounding_vals += 0.0125*grid.get((x_pos-1, y_pos-1), 0)
                if surrounding_vals >= grid.get((x_pos, y_pos), 0):
                    if grid.get((x_pos, y_pos), None) is not None:
                        grid[x_pos, y_pos] = surrounding_vals

def colorGrid():
    for key, value in grid.items():
        x, y = key
        size = (int(screen_width / 28), int((screen_height-100) / 28))
        bg_rect = pygame.Rect(x * size[0], y * size[1], size[0], size[1])
        rect = pygame.Rect(x * size[0]+1, y * size[1]+1, size[0]-2, size[1]-2)
        color = (int(value*255), int(value*255), int(value*255))
        pygame.draw.rect(SCREEN, WHITE, bg_rect)
        pygame.draw.rect(SCREEN, color, rect)

def runRender():
    global grid

    drawGrid(screen_width, screen_height-100)
    while True:

        SCREEN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        text = font.render('Press space to clear and k to send to AI', True, WHITE)

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            grid = {(x, y): 0.0 for x in range(dimensions[0]) for y in range(dimensions[1])}
            text = font.render('Cleared screen', True, WHITE)
        if pygame.key.get_pressed()[pygame.K_k]:
            text = font.render('sent', True, WHITE)

        SCREEN.blit(text, (15, 730))

        if mouse.get_pressed()[0]:
            mouse_pos = mouse.get_pos()
            setBox(mouse_pos, False)
        if mouse.get_pressed()[2]:
            mouse_pos = mouse.get_pos()
            setBox(mouse_pos, True)
        colorGrid()
        pygame.display.update()