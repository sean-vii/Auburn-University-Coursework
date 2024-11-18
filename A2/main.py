import os
import sys
import time
from collections import deque

# TODO: 
# Because they're so similar, combine bfs and dfs methods, with a new, fourth paremeter to 
# create distinction. This fourth parameter would control whether you use a stack (LIFO) or a 
# queue (FIFO). That's not part of the assignment though so I'm not doing it rn. 

def bfs(graph, start, target):
    visited = set()
    queue = [(start, 0)]  
    parent = {start: None}  

    while queue:
        node, distance = queue.pop(0)  # Dequeue - FIFO
        if node == target:
            path = []
            while node:
                path.append(node)
                node = parent[node]
            return distance, path[::-1] # Reverse the path to get start to target
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited and neighbor not in parent:
                    parent[neighbor] = node
                    queue.append((neighbor, distance + 1))  # Enqueue

    return -1, []  # If no path found

def dfs(graph, start, target):
    visited = set()
    stack = [(start, 0)] 
    parent = {start: None}  

    while stack:
        node, distance = stack.pop()  # Dequeue - LIFO
        if node == target:
            path = []
            while node:
                path.append(node)
                node = parent[node]
            return distance, path[::-1]  # Reverse the path to get start to target
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited and neighbor not in parent:
                    parent[neighbor] = node 
                    stack.append((neighbor, distance + 1))  # Enqueue

    return -1, []  # If no path found

def main():
    #-| Read Command-Line Arguments ------------------------------------------------|
    if len(sys.argv) != 4:
        print("Usage: python3 main.py <src_node> <tgt_node> <alg>")
        return

    src = sys.argv[1].strip()
    tgt = sys.argv[2].strip()
    alg = sys.argv[3].strip().lower()

    #-| Read File ------------------------------------------------------------------|
    file_name = "testcases.txt"

    if not os.path.exists(file_name):
        print(f"Error: {file_name} not found.")
        return

    #-| Convert file to custom graph schema ----------------------------------------|
    graph = {}

    with open(file_name, 'r') as file:
        try:
            for line in file:
                node1, node2 = line.strip().split(',')
                
                # Ensure the nodes exist in the graph
                if node1 not in graph:
                    graph[node1] = []
                if node2 not in graph:
                    graph[node2] = []
                
                # Add edges if not already present
                if node2 not in graph[node1]:
                    graph[node1].append(node2)
                if node1 not in graph[node2]:
                    graph[node2].append(node1)
        except ValueError:
            print(f"Unsupported file format. Boo womp.")
            return

    #-| Validate Nodes and Execute Algorithm --------------------------------------|
    distance = None
    path = []
    elapsed_time_ms = 0

    if alg == "bfs":
        start_time = time.perf_counter() 
        distance, path = bfs(graph, src, tgt)
        elapsed_time_ms = (time.perf_counter() - start_time) * 1000  
    elif alg == "dfs":
        start_time = time.perf_counter() 
        distance, path = dfs(graph, src, tgt)
        elapsed_time_ms = (time.perf_counter() - start_time) * 1000  
    else:
        print("Error: Invalid algorithm choice. Please choose BFS or DFS.")
        return

    #-| Display Result -----------------------------------------------------------|
    if distance != -1:
        print(
            f"\n\033[1m\n\033[92mA path exists between {src} and {tgt} ({alg.upper()}).\033[0m"
            f"\n\033[1mTime taken:\033[0m {elapsed_time_ms:.4f} ms\n"
            f"\033[1mDistance:\033[0m {distance} nodes\n"
            f"\033[1mPath:\033[0m {' → '.join([node.split('_')[-1] for node in path])}\n"
        )
    else:
        print(f"\033[91mNo path exists between {src} and {tgt}.\033[0m")

if __name__ == "__main__":
    main()