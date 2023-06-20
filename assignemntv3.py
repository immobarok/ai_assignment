import math
import csv
from collections import defaultdict
import time

COORDINATES_FILE = "Coordinates.csv"
DISTANCE_FILE = "distances.csv"

def distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

coordinates = {}
adjacency_list = defaultdict(list)

with open(COORDINATES_FILE, 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for star_name, x, y, z in reader:
        coordinates[star_name] = (int(x), int(y), int(z))

with open(DISTANCE_FILE, "r") as file:
    reader = csv.reader(file)
    for source, destination, dist in reader:
        adjacency_list[source].append((destination, int(dist)))

SOURCE_STAR = "Sun"
DESTINATION_STAR = "61 Virginis"

# A* Algorithm
def astar_heuristic(star_name):
     
    x1, y1, z1 = coordinates[star_name]
    x2, y2, z2 = coordinates[DESTINATION_STAR]
    return distance(x1, y1, z1, x2, y2, z2)

from heapq import heapify, heappop, heappush

start_time = time.time()

priority_queue = [(0, SOURCE_STAR)]
visited = set()
heapify(priority_queue)
g_scores = defaultdict(lambda: float("inf"))
g_scores[SOURCE_STAR] = 0

while priority_queue:
    _, current_star = heappop(priority_queue)
    if current_star == DESTINATION_STAR:
        print("Reached " + DESTINATION_STAR + " Distance = " + str(g_scores[current_star]))
        break
    if current_star in visited:
        continue
    visited.add(current_star)
    for neighbor_star, neighbor_distance in adjacency_list[current_star]:
        tentative_g_score = g_scores[current_star] + neighbor_distance
        if tentative_g_score < g_scores[neighbor_star]:
            g_scores[neighbor_star] = tentative_g_score
            f_score = tentative_g_score + astar_heuristic(neighbor_star)
            heappush(priority_queue, (f_score, neighbor_star))

a_star_execution_time = time.time() - start_time

# Dijkstra's Algorithm
start_time = time.time()

priority_queue = [(0, SOURCE_STAR)]
visited = set()
heapify(priority_queue)
g_scores = defaultdict(lambda: float("inf"))
g_scores[SOURCE_STAR] = 0

while priority_queue:
    dist, current_star = heappop(priority_queue)
    if current_star == DESTINATION_STAR:
        print("Reached " + DESTINATION_STAR + " Distance = " + str(dist))
        break
    if current_star in visited:
        continue
    visited.add(current_star)
    for neighbor_star, neighbor_distance in adjacency_list[current_star]:
        tentative_g_score = g_scores[current_star] + neighbor_distance
        if tentative_g_score < g_scores[neighbor_star]:
            g_scores[neighbor_star] = tentative_g_score
            heappush(priority_queue, (tentative_g_score, neighbor_star))

dijkstra_execution_time = time.time() - start_time

print("Execution Time (A*):", a_star_execution_time)
print("Execution Time (Dijkstra's):", dijkstra_execution_time)
