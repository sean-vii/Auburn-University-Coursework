import os

def main():
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

                if node1 not in graph:
                    graph[node1] = []
                if node2 not in graph:
                    graph[node2] = []

                graph[node1].append(node2)
                graph[node2].append(node1)
        except ValueError:
            print(f"Unsupported file format. Boo womp.")
            return

    #-| Convert file to custom graph schema ----------------------------------------|
    for node, neighbors in graph.items():
        print(f"{node}: {', '.join(neighbors)}")

if __name__ == "__main__":
    main()
