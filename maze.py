import pygame
import sys
from random import choice
import csv

RES = WIDTH, HEIGHT = (1202, 902)
TILE = 50
COLS = WIDTH // TILE
ROWS = HEIGHT // TILE
FPS = 260

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.grid_cells = [Cell(col, row) for row in range(ROWS) for col in range(COLS)]
        self.current_cell = self.grid_cells[0]
        self.stack = []
        self.colors = []
        self.color = 34
        self.loop = True
        self.paused = False
    
    def remove_walls(self):
        dx = self.current_cell.x - self.next_cell.x
        if dx == 1:
            self.current_cell.walls['left'] = False
            self.next_cell.walls['right'] = False
        elif dx == -1:
            self.current_cell.walls['right'] = False
            self.next_cell.walls['left'] = False
            
        dy = self.current_cell.y - self.next_cell.y
        if dy == 1:
            self.current_cell.walls['top'] = False
            self.next_cell.walls['bottom'] = False
        elif dy == -1:
            self.current_cell.walls['bottom'] = False
            self.next_cell.walls['top'] = False
    
    def draw(self):
        self.screen.fill(pygame.Color('plum'))
        [cell.draw(self.screen) for cell in self.grid_cells]
        self.current_cell.visited = True
        self.current_cell.draw_current_cell(self.screen)
        [pygame.draw.rect(self.screen, self.colors[i], (cell.x * TILE + 5, cell.y * TILE + 5, TILE -10, TILE - 10), border_radius = 12) for i, cell in enumerate(self.stack)]
        self.next_cell = self.current_cell.check_neighbors(self.grid_cells)
        if self.next_cell:
            self.next_cell.visited = True
            self.stack.append(self.current_cell)
            self.colors.append((min(self.color, 255), 10, 100))
            self.color += 2
            self.remove_walls()
            self.current_cell = self.next_cell
        elif self.stack:
            self.current_cell = self.stack.pop()
    
    def check_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    self.loop = False
                if event.key == pygame.K_1:
                    self.print_maze()
                if event.key == pygame.K_ESCAPE:
                    self.save_to_csv()
                
    def update(self):
        pygame.display.flip()
        self.clock.tick(FPS)
        pygame.display.set_caption('MAZE GENERATOR')
    
    def create_ascii_grid(self):
        ascii_grid = [['#','##'*COLS]]
        top = ['#']
        mid = ['#']
        bottom = ['#']
        for index, cell in enumerate(self.grid_cells):
            walls = cell.walls
            if walls['right']:
                mid[-1] = mid[-1] + '.#'
            else:
                mid[-1] = mid[-1] + '..'
            if walls['bottom']:
                bottom.append('##')
            else:
                bottom.append('.#')
            
            if (index + 1) % COLS == 0:
                if index == 0:
                    ascii_grid.append(top)
                ascii_grid.append(mid)
                ascii_grid.append(bottom)
                mid, bottom = ['#'], ['#']
        return ascii_grid
        
    def print_maze(self):
        
        ascii_grid = self.create_ascii_grid()
        
        for row in ascii_grid:
            row.append('\n')
            for block in row:
                print(block, end = '')    
            
    def save_to_csv(self, file_name = 'maze'):
        
        ascii_grid = self.create_ascii_grid()
        
        with open(file_name.replace('.csv', '') + '.csv', 'w') as file:
            writer = csv.writer(file)
            for row in ascii_grid:
                row = ''.join(row)
                row = [i for i in row]
                writer.writerow(row)      
        
    def run(self):
        while self.loop:
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
            pygame.draw.line(screen, pygame.Color('magenta3'), (x, y), (x + TILE, y), 2)
        if self.walls['right']:
            pygame.draw.line(screen, pygame.Color('magenta3'), (x + TILE, y), (x + TILE, y + TILE), 2)
        if self.walls['bottom']:
            pygame.draw.line(screen, pygame.Color('magenta3'), (x + TILE, y + TILE), (x, y + TILE), 2)
        if self.walls['left']:
            pygame.draw.line(screen, pygame.Color('magenta3'), (x, y + TILE), (x, y), 2)
            
    def check_cell(self,x, y, grid_cells):
        find_index = lambda x, y: x + y * COLS
        if x < 0 or x > COLS - 1 or y < 0 or y > ROWS -1 :
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
    game.save_to_csv()
    game.print_maze()