import pygame
import sys
from random import choice

RES = WIDTH, HEIGHT = (1202, 902)
TILE = 100
COLS = WIDTH // TILE
ROWS = HEIGHT // TILE
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.grid_cells = [Cell(col, row) for row in range(ROWS) for col in range(COLS)]
        self.current_cell = self.grid_cells[0]
        self.stack = []
    
    def draw(self):
        self.screen.fill(pygame.Color('darkslategray'))
        [cell.draw(self.screen) for cell in self.grid_cells]
        self.current_cell.visited = True
        self.current_cell.draw_current_cell(self.screen)
        next_cell = self.current_cell.check_neighbors(self.grid_cells)
        if next_cell:
            next_cell.visited = True
            self.current_cell = next_cell
    
    def check_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
    def update(self):
        pygame.display.flip()
        self.clock.tick(FPS)
        pygame.display.set_caption('MAZE GENERATOR')
        
    def run(self):
        while True:
            self.check_events()
            self.draw()
            self.update()
            
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
    
    def draw_current_cell(self, screen):
        x = self.x * TILE
        y = self.y * TILE
        pygame.draw.rect(screen, pygame.Color('saddlebrown'), (x + 2, y + 2, TILE - 2, TILE - 2))
        
    def draw(self, screen):
        x = self.x * TILE
        y = self.y * TILE
        
        if self.visited:
            pygame.draw.rect(screen, pygame.Color('black'), (x, y, TILE, TILE))
        
        if self.walls['top']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x, y), (x + TILE, y), 2)
        if self.walls['right']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x + TILE, y), (x + TILE, y + TILE), 2)
        if self.walls['bottom']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x + TILE, y + TILE), (x, y + TILE), 2)
        if self.walls['left']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x, y + TILE), (x, y), 2)
            
    def check_cell(self,x, y, grid_cells):
        find_index = lambda x, y: x + y * COLS
        if x < 0 or x > COLS + 1 or y < 0 or y > ROWS -1 :
            return False
        return grid_cells[find_index(x, y)]
        
    def check_neighbors(self, grid_cells):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1, grid_cells)
        right = self.check_cell(self.x + 1, self.y, grid_cells)
        bottom = self.check_cell(self.x, self.y + 1, grid_cells)
        left = self.check_cell(self.x - 1, self.y, grid_cells)
        
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
            
        return choice(neighbors) if neighbors else False
        
if __name__ == "__main__":
    game = Game()
    game.run()