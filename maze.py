import pygame
import sys
import csv
from settings import *
from cell import Cell

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.new_maze()
    
    def new_maze(self):
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
            self.color += 1
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
                    self.new_maze()
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
        while True:
            self.check_events()
            self.draw()
            self.update()
            
        
if __name__ == "__main__":
    game = Game()
    game.run()