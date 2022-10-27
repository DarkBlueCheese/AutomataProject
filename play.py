import time
import pygame
import numpy as np


# conda create -n myvenv python=3.8.8 anaconda
# conda activate myvenv
# conda deactivate


# donut, toroidal, periodic boundary condition

color_bg = (10, 10, 10)
color_grid = (40, 40, 40)
color_die_next = (170, 170, 170)
color_alive_next = (255, 255, 255)

def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):

        # x좌표 벗어날 때, y좌표 벗어날 때
        
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        color = color_bg if cells[row, col] == 0 else color_alive_next
        
        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = color_die_next

            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = color_alive_next

        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = color_alive_next
        
        # (x_pos, y_pos, x_size, y_size) start from (0,0)
        pygame.draw.rect(screen, color, (col*size, row*size, size-1, size-1))

    return updated_cells

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    cells = np.zeros((60, 80))
    screen.fill(color_grid)
    update(screen, cells, 10)
    
    pygame.display.flip()
    pygame.display.update()

    running = False

    while True:
        for event in pygame.event.get():

            # when press quit, quit
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # when press space, pause
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, 10)
                    pygame.display.update()
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1]//10, pos[0]//10] = 1
                update(screen, cells, 10)
                pygame.display.update()

        screen.fill(color_grid)

        if running:
            cells = update(screen, cells, 10, with_progress=True)
            pygame.display.update()

        time.sleep(0.0001)

if __name__ == '__main__':
    main()