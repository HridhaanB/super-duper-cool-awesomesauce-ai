import pygame, sys
from pygame.locals import QUIT

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen_width = 672
screen_height = 772
dimensions = (84, 84)
blurred = False

SCREEN = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('super duper cool awesomesauce ai')
SCREEN.fill(BLACK)

mouse = pygame.mouse
clock = pygame.time.Clock()

grid = {(x, y): 0.0 for x in range(dimensions[0]) for y in range(dimensions[1])}

def drawGrid(w, h, d=dimensions):
    size = (int(w / d[0]), int(h / d[1]))
    for x in range(0, w, size[0]):
        for y in range(0, h, size[1]):
            rect = pygame.Rect(x, y, size[0], size[1])
            pygame.draw.rect(SCREEN, WHITE, rect, 1)


def setBox(p, color, d=dimensions, w=screen_width, h=screen_height-100):
    boxx_og, boxy_og = mousePosToGrid(p)
    for x in range(-1, 2):
        for y in range(-1, 2):
            boxx, boxy = (boxx_og+x, boxy_og + y)
            #print(boxx, boxy)
            if (boxx, boxy) not in grid:
                continue
            if color != BLACK:
                if grid[(boxx, boxy)] == 1:
                    continue
                grid[(boxx, boxy)] = 1
                #antiAlias(p)
                colorGrid()
            else:
                #erase
                grid[(boxx, boxy)] = 0
                drawGrid(w, h)

def mousePosToGrid(pos):
    x, y = pos
    size = int(screen_width / dimensions[0]), int((screen_height-100) / dimensions[1])
    return int(x / size[0]), int(y / size[1])

def antiAlias(pos):
    x, y = mousePosToGrid(pos)
    for x_pos in range(x-1, x+1):
        for y_pos in range(y-1, y+1):
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
                grid[x_pos, y_pos] = surrounding_vals

def colorGrid():
    for key, value in grid.items():
        x, y = key
        size = (int(screen_width / dimensions[0]), int((screen_height-100) / dimensions[1]))
        bg_rect = pygame.Rect(x * size[0], y * size[1], size[0], size[1])
        rect = pygame.Rect(x * size[0]+1, y * size[1]+1, size[0]-2, size[1]-2)
        color = (int(value*255), int(value*255), int(value*255))
        pygame.draw.rect(SCREEN, WHITE, bg_rect)
        pygame.draw.rect(SCREEN, color, rect)

def deres(factor, grid):
    new_grid = {}
    averages = {}
    for x in range(dimensions[0]):
        for y in range(dimensions[1]):
            average = 0
            for z in range(factor):
                for a in range(factor):
                    average += grid.get((x+z, y+a), 0)
            average = average/factor**2
            averages[(x, y)] = average
    for x in range(0, dimensions[0], factor):
        for y in range(0, dimensions[0], factor):
            for z in range(factor):
                for a in range(factor):
                    new_grid[(x+z, y+a)] = averages[(x+z, y+a)]
    return new_grid

def runRender():
    global grid
    global blurred
    #print("Hi")
    drawGrid(screen_width, screen_height-100)
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if mouse.get_pressed()[0]:
            mouse_pos = mouse.get_pos()
            setBox(mouse_pos, WHITE)
        if mouse.get_pressed()[2]:
            mouse_pos = mouse.get_pos()
            setBox(mouse_pos, BLACK)
        
        if pygame.key.get_pressed()[pygame.K_SPACE] and not blurred:
            blurred = True
            grid = deres(3, grid)
            colorGrid()

        pygame.display.update()
