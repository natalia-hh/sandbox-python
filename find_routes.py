# 
# generate city map, get courier and orders locations
# 

from random import random
import math 

ways = [(-1, 0), (0, 1), (1, 0), (0, -1)] # defines possible directions - only 90° now
cols, rows = 100, 100
courier_location = (84, 17)
orders_location = [(66, 32), (39, 75), (90, 10), (89, 60), (79, 77), (65, 38), (9, 5)]
route = []
route_path = []
route_unpacked = []
city_map_list = []

orders_location = sorted(orders_location, key=lambda tup: math.dist(tup, courier_location)) #sort orders by distance
print('Orders order:',orders_location)

def get_city_map_list (cols,rows):
    global city_map_list
    city_map_list = [[0 if random() < 0.1 else 1 for col in range(cols)] for row in range(rows)]
    locations_to_check = orders_location + [courier_location]
    for x, y in locations_to_check:
        city_map_list[y][x] = 1
        if not possible_ways(x, y):
        # Try to make an adjacent cell accessible if none is, to ensure at least one possible way
            for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < cols and 0 <= ny < rows:
                    city_map_list[ny][nx] = 1  # Make an adjacent cell accessible
                    break
    return city_map_list

def possible_ways(cl_x,cl_y): #returns possible directions for current dot (out of 4 directions)
    check_next = lambda cl_x, cl_y: True if 0 <= cl_y < len(city_map_list) and 0 <= cl_x < len(city_map_list[0]) and city_map_list[cl_y][cl_x]==1 else False 
    ways = [-1,0],[0,1],[1,0],[0,-1]
    possible_ways = [(cl_x + dx, cl_y + dy) for dx, dy in ways if check_next(cl_x + dx, cl_y + dy)]
    return possible_ways

get_city_map_list(cols, rows)

# 
# with visuals
# 

import pygame
from collections import deque

def get_rect(x, y): #to draw dots
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2

def get_next_order(x,y):
    grid_x, grid_y = x,y
    pygame.draw.rect(screen, pygame.Color('red'), get_rect(grid_x, grid_y))
    return (grid_x, grid_y)

def bfs(start, goal, graph):
    queue = deque([start])
    visited = {start: None}
    while queue:
        cur_node = queue.popleft()
        if cur_node == goal:
            break
        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node
    return queue, visited


pygame.init()
clock = pygame.time.Clock()

# BFS settings
TILE = 10
start = courier_location
goal = start
queue = deque([start])
visited = {start: None}

screen = pygame.display.set_mode([len(city_map_list) * TILE, len(city_map_list[0]) * TILE])
grid = city_map_list
graph = {}

for y, row in enumerate(grid):
    for x, col in enumerate(row):
        if col==1:
            graph[(x, y)] = graph.get((x, y), []) + possible_ways(x, y)

route.clear()
route_unpacked.clear()
running = True
while running:
    pygame.event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        Else: None 
    pygame.display.update()
            
    screen.fill(pygame.Color('black'))
    [[pygame.draw.rect(screen, pygame.Color('darkorange'), get_rect(x, y), border_radius=TILE // 5)
      for x, col in enumerate(row) if col==0] for y, row in enumerate(grid)]
    
    # BFS get path to next order
    for orders in orders_location:
        next_order = get_next_order(orders[0],orders[1])
        route_path.clear()
        if next_order and grid[next_order[1]][next_order[0]]:
            if orders_location.index(orders)>0:
                start = tuple((orders_location[orders_location.index(orders)-1]))
            queue, visited = bfs(start, next_order, graph)
            goal = next_order
            print("start:", start)
            print("next goal:", goal)
    # draw path
            path_head, path_segment = goal, goal
            while path_segment and path_segment in visited:
                pygame.draw.rect(screen, pygame.Color('white'), get_rect(*path_segment), TILE, border_radius=TILE // 3)
                path_segment = visited[path_segment]
                if path_segment:
                    print("a",path_segment)
                    route_path.append(path_segment)
            route_path.reverse()
            route_path.append(path_head)
            route_unpacked.append(list(route_path))
            print("route_path:",route_path)
            pygame.draw.rect(screen, pygame.Color('blue'), get_rect(*start), border_radius=TILE // 3)
            pygame.draw.rect(screen, pygame.Color('magenta'), get_rect(*path_head), border_radius=TILE // 3)
        running = False
                    
        pygame.display.flip()
        clock.tick(2)

        # 
# no visuals
# 

from collections import deque

def get_next_order(x,y):
    grid_x, grid_y = x,y
    return (grid_x, grid_y)

def bfs(start, goal, graph):
    queue = deque([start])
    visited = {start: None}
    while queue:
        cur_node = queue.popleft()
        if cur_node == goal:
            break
        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node
    return queue, visited

start = courier_location
goal = start
queue = deque([start])
visited = {start: None}
grid = city_map_list
graph = {}

for y, row in enumerate(grid):
    for x, col in enumerate(row):
        if col==1:
            graph[(x, y)] = graph.get((x, y), []) + possible_ways(x, y)

route.clear()
route_unpacked.clear()
running = True
while running:
    for orders in orders_location:
        next_order = get_next_order(orders[0],orders[1])
        route_path.clear()
        if next_order and grid[next_order[1]][next_order[0]]:
            if orders_location.index(orders)>0:
                start = tuple((orders_location[orders_location.index(orders)-1]))
            queue, visited = bfs(start, next_order, graph)
            goal = next_order
            path_head, path_segment = goal, goal
            while path_segment and path_segment in visited:
                path_segment = visited[path_segment]
                if path_segment:
                    route_path.append(path_segment)
            route_path.reverse()
            route_path.append(path_head)
            route_unpacked.append(list(route_path))
        running = False

route = [item for sublist in route_unpacked for item in sublist]
print('Route:', route)

# # orders's locations
# [(17, 99), [(42, 76), (27, 80), (43, 52), (26, 75)]]
# [(84, 17), [(66, 32), (39, 75), (90, 10), (89, 60), (79, 77), (65, 38), (9, 5)]]
# [(10, 55), [(99, 48), (75, 90), (23, 29), (23, 96), (73, 11), (91, 88), (25, 50), (3, 69)]]
# [(10, 87), [(83, 38), (94, 56), (72, 75), (74, 64), (62, 15), (83, 99), (84, 25), (66, 7), (71, 41), (2, 40)]]
# [(22, 3), [(15, 38), (55, 13), (33, 1), (61, 88), (90, 66), (19, 91), (61, 58), (15, 74)]]
# [(9, 82), [(4, 6), (85, 25)]]
# [(26, 26), [(29, 29), (0, 0), (0, 3)]]

# # temp code to import city_map_list from existing csv file
# import pandas as pd
# df = pd.read_csv('/Users/mia_pro/QA/city_map.csv', names=list(range(0, 100, 1)))
# city_map_list = df.values.tolist()