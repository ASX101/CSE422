import heapq

def manhattan_distance(point1, point2):
    
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

# A* Search Algorithm
def astar_search(maze, start, goal, n, m):
    
    # Priority queue: stores (f_score, g_score, current_position, path)
    # f_score = g_score + h_score
    # g_score = cost from start to current
    # h_score = heuristic (Manhattan distance to goal)
    open_list = []

    # Calculate initial heuristic
    h_score = manhattan_distance(start, goal)

    # Push starting node: (f_score, g_score, position, path_actions)
    heapq.heappush(open_list, (h_score, 0, start, ""))

    # Keep track of visited nodes to avoid revisiting
    visited = set()

    # Direction mappings: (row_change, col_change, action_character)
    directions = [
        (-1, 0, 'U'),  # Up: decrease row
        (1, 0, 'D'),   # Down: increase row
        (0, -1, 'L'),  # Left: decrease column
        (0, 1, 'R')    # Right: increase column
    ]

    while open_list:
        # Pop node with smallest f_score
        f_score, g_score, current, path = heapq.heappop(open_list)

        # Check if we reached the goal
        if current == goal:
            return g_score, path

        # Skip if already visited
        if current in visited:
            continue

        # Mark as visited
        visited.add(current)

        # Explore neighbors
        for dr, dc, action in directions:
            new_row = current[0] + dr
            new_col = current[1] + dc
            neighbor = (new_row, new_col)

            # Check if neighbor is valid
            # 1. Within bounds
            # 2. Not a wall
            # 3. Not visited
            if (0 <= new_row < n and
                0 <= new_col < m and
                maze[new_row][new_col] == '0' and
                neighbor not in visited):

                # Calculate new g_score (cost increases by 1)
                new_g_score = g_score + 1

                # Calculate h_score (heuristic)
                new_h_score = manhattan_distance(neighbor, goal)

                # Calculate f_score
                new_f_score = new_g_score + new_h_score

                # Add to priority queue
                new_path = path + action
                heapq.heappush(open_list, (new_f_score, new_g_score, neighbor, new_path))

    # No path found
    return -1, ""

# Main program
def main():
    # Read input
    n, m = map(int, input().split())  # height and width
    start_row, start_col = map(int, input().split())  # entry point
    goal_row, goal_col = map(int, input().split())  # exit point

    # Read maze
    maze = []
    for i in range(n):
      row = input().strip()
      maze.append(row)

    # Define start and goal as tuples
    start = (start_row, start_col)
    goal = (goal_row, goal_col)

    # Run A* search
    cost, path = astar_search(maze, start, goal, n, m)

    # Print output
    if cost == -1:
        print(-1)
    else:
        print(cost)
        print(path)

# Run the program
if __name__ == "__main__":
    main()
    
    
    