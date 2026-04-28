import pygame
import random
import sys

R, C = 20, 20  # Creates a 20 x 20 maze
CELL_SIZE = 30
WIDTH, HEIGHT = C * CELL_SIZE + 40, R * CELL_SIZE + 40 # Calculates the total screen width and height
FPS = 60 # Controls how smooth the animation is(Frames Per Second)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
GREEN = (0, 255, 0)
 
# This creates the horizontal walls(Top/Bottom)
north_wall = [[1 for _ in range(C)] for _ in range(R + 1)] #initially every cell has a north wall
east_wall = [[1 for _ in range(C + 1)] for _ in range(R)] # This creates the vertical walls(Left/Right)
visited = [[False for _ in range(C)] for _ in range(R)] # This keeps track of which cells have been visited during maze generation

pygame.init() # Initializes the Pygame library
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Creates a window of the specified width and height
pygame.display.set_caption("Building and Running Maze")
clock = pygame.time.Clock() # Creates a clock object to control the frame rate of the animation

def get_neighbors(i, j): # (i,j) represents a single cell in the maze
    neighbors = [] # Creats an empty list
    if i > 0: neighbors.append((i - 1, j)) # when moving up the row decreases by 1
    if i < R - 1: neighbors.append((i + 1, j)) # when moving down the row increases by 1
    if j > 0: neighbors.append((i, j - 1)) # when moving left the column decreases by 1
    if j < C - 1: neighbors.append((i, j + 1)) # when moving right the column increases by 1
    return neighbors

def remove_wall(i1, j1, i2, j2): # These two walls are assumed to be next to each other
    if i1 == i2: #same row(horizontal neighbors) so the wall to remove is vertical
        east_wall[i1][max(j1, j2)] = 0 #path opens here(from left <=> right)
    elif j1 == j2: #same column(vertical neighbors) so the wall to remove is horizontal
        north_wall[max(i1, i2)][j1] = 0 #path opens here(from up <=> down)

# Path data includes red dot(explored path) and blue dot(backtracked path)
# current pos shows the current position of the player
def draw_maze(path_data=None, current_pos=None):
    screen.fill(WHITE)
    for i in range(R):
        for j in range(C):
            x, y = j * CELL_SIZE + 20, (R - 1 - i) * CELL_SIZE + 20 # drawing starts from the bottom left corner, so we need to flip the y coordinate
            
            if path_data:
                if path_data[i][j] == ".": # Draws a small red dot for the explored path
                    pygame.draw.circle(screen, RED, (x + CELL_SIZE//2, y + CELL_SIZE//2), 5) 
                elif path_data[i][j] == "x": # Draws a small blue dot for the backtracked path
                    pygame.draw.circle(screen, BLUE, (x + CELL_SIZE//2, y + CELL_SIZE//2), 5)
            
            if current_pos == (i, j): # Draws a green square for the current position of the player
                pygame.draw.rect(screen, GREEN, (x+2, y+2, CELL_SIZE-4, CELL_SIZE-4))
     # Draws the walls of the maze
            if east_wall[i][j] == 1: #Draw a line on left side od the cell
                pygame.draw.line(screen, BLACK, (x, y), (x, y + CELL_SIZE), 2)
            if east_wall[i][j+1] == 1: #Draw a line on right side of the cell
                pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
            if north_wall[i+1][j] == 1: #Draw a line on top of the cell
                pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y), 2)
            if north_wall[i][j] == 1: #Draw a line on bottom of the cell
                pygame.draw.line(screen, BLACK, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
    pygame.display.flip() # Displays everything on the screen

# Creates a maze step by step on screen
def generate_maze_dynamic():
    stack = [] # It helps to keep track and go back when stuck(backtracking)
    i, j = random.randint(0, R-1), random.randint(0, C-1) # Chooses a random cell in the grid, maze generation starts
    visited[i][j] = True # Marks the starting cell as visited
    stack.append((i, j)) # Adds the starting cell to the stack
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        i, j = stack[-1] #gets the current cell from the top of the stack
        unvisited = [n for n in get_neighbors(i, j) if not visited[n[0]][n[1]]] # Finds all unvisited neighbors of the current cell
        if unvisited:
            ni, nj = random.choice(unvisited) # Chooses a random unvisited neighbor
            remove_wall(i, j, ni, nj) # Removes the wall between the current cell and the chosen neighbor, creating a path
            visited[ni][nj] = True # Marks the chosen neighbor as visited
            stack.append((ni, nj)) # Adds the chosen neighbor to the stack, making it the new current cell for the next iteration
        else: # no unvisited neighbors, so we need to backtrack
            if random.random() < 0.05:
                ni, nj = random.choice(get_neighbors(i, j))
                remove_wall(i, j, ni, nj)
            stack.pop() # removes current cell from stack, go back to previous cell
        draw_maze(current_pos=(i, j)) # updates screen
        clock.tick(FPS) # controls the speed of the animation

def solve_maze_dynamic(start, end): # find a path from start to end
    stack = [start]
    solve_visited = [[False for _ in range(C)] for _ in range(R)] # Keeps track of visited cells during maze solving
    path_display = [[" " for _ in range(C)] for _ in range(R)]
    solve_visited[start[0]][start[1]] = True
    while stack:
        # Allows safe closing of window
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        i, j = stack[-1] # current position
        path_display[i][j] = "." # Marks current exploration path
        if (i, j) == end: return path_display
        moved = False
        for ni, nj in get_neighbors(i, j): # checks all neighbors
            wall_missing = False
            # checks if there is no wall and the cell is not visited, then we can move there
            if ni == i and nj == j + 1: wall_missing = (east_wall[i][j+1] == 0)
            if ni == i and nj == j - 1: wall_missing = (east_wall[i][j] == 0)
            if ni == i + 1 and nj == j: wall_missing = (north_wall[i+1][j] == 0)
            if ni == i - 1 and nj == j: wall_missing = (north_wall[i][j] == 0)
            if not solve_visited[ni][nj] and wall_missing:
                stack.append((ni, nj))
                solve_visited[ni][nj] = True
                moved = True
                break
        if not moved:
            path_display[i][j] = "x"
            stack.pop() # Go to previous cell
        draw_maze(path_data=path_display, current_pos=(i, j))
        clock.tick(FPS // 2)

generate_maze_dynamic()
start = (random.randint(0, R-1), 0) # Chooses a random starting point on the left edge
end = (random.randint(0, R-1), C-1) # Chooses a random ending point on the right edge
east_wall[start[0]][0] = 0 # Creates an entry wall by removing left wall
east_wall[end[0]][C-1] = 0 # Creates an exit wall by removing right wall
solve_maze_dynamic(start, end) 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()