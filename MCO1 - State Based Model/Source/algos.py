from queue import PriorityQueue 

def ucs(graph, start, goal):
    frontier = PriorityQueue() # possible nodes to be traversed in order of their cum. cost (more than one instance of nodes are possible)
    frontier.put((0, start))
    came_from = {start: None} # visited nodes
    cost_so_far = {start: 0} # cumulative cost of each node

    while not frontier.empty():
        # get top of queue and print   
        current_cost, current_node = frontier.get()
        print(f"Expanding {current_node} w/ current cost {round(current_cost, 2)}...")

            
        # if current node is the goal, stop traversal
        if current_node == goal:
            print(f"Goal found: {current_node} with cost {round(current_cost, 2)}")
            break
        
        # compute cumulative cost  of children and enqueue
        for next_node, weight in graph[current_node].items():
            new_cost = cost_so_far[current_node] + weight
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost
                frontier.put((priority, next_node))
                came_from[next_node] = current_node # mark visited
                
        # list all possible nodes to visit (that aren't visited yet) based on queue
        frontier_copy = frontier.queue.copy()
        added = set() # collect added nodes to avoid duplicates
        possible_nodes = [(cost, node) for cost, node in frontier_copy
                          if node not in added and not added.add(node) 
        ]
        
        # print possible nodes to visit (if non-empty) and order alphabetically
        if possible_nodes and current_node != goal: 
            print_nodes = ', '.join(f"{node} ({round(cost, 2)})" for cost, node in sorted(possible_nodes))
            print(f" : Considering: {print_nodes}")
        # TODO: remove this (checks contents of queue, cross-check against possible_nodes)
        #print(frontier.queue)

    # reconstruct path
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    # TODO: return came_from as the visit sequence list (optional but iirc ma'am said to show)
    return path

def gbfs(graph, start, goal, heuristic):
    frontier = PriorityQueue() # possible nodes to be traversed in order of cum.cost (with > 1 node instance possible)
    frontier.put((0, start)) 
    came_from = {start: None} # visited nodes

    while not frontier.empty():
        # get top of queue and print
        current_hn, current_node = frontier.get()
        print(f"Expanding {current_node} w/ current heuristic {round(current_hn, 2)}...")
        
        if current_node == goal:
            print(f"Goal found: {current_node}")
            break

        for next_node in graph[current_node]:
            if next_node not in came_from:
                priority = heuristic(next_node, goal)
                frontier.put((priority, next_node))
                came_from[next_node] = current_node # mark visited
                
        # list all possible nodes to visit (that aren't visited yet) based on queue
        frontier_copy = frontier.queue.copy()
        added = set() # collect added nodes to avoid duplicates
        possible_nodes = [(hn, node) for hn, node in frontier_copy
                          if node not in added and not added.add(node) 
        ]
        
        # print possible nodes to visit (if non-empty) and order alphabetically
        if possible_nodes and current_node != goal: 
            print_nodes = ', '.join(f"{node} ({round(hn, 2)})" for hn, node in sorted(possible_nodes))
            print(f" : Considering: {print_nodes}")
            
        # TODO: remove this (double checks contents of queue, cross-check against possible_nodes)
        #print(frontier.queue)

    # reconstruct path
    path = []
    current_node = goal
    while current_node != start:
        path.append(current_node)
        current_node = came_from[current_node]
    path.append(start)
    path.reverse()
    
    return path

# alternate functions being used for measurement.py
def ucs_noprint(graph, start, goal):
    frontier = PriorityQueue()  # possible nodes to be traversed in order of their cum. cost (more than one instance of nodes are possible)
    frontier.put((0, start))
    came_from = {start: None}  # visited nodes
    cost_so_far = {start: 0}  # cumulative cost of each node

    while not frontier.empty():
        # get top of queue
        current_node = frontier.get()[1]

        # if current node is the goal, stop traversal
        if current_node == goal:
            break

        # compute cumulative cost and enqueue
        for next_node, weight in graph[current_node].items():
            new_cost = cost_so_far[current_node] + weight
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost
                frontier.put((priority, next_node))
                came_from[next_node] = current_node  # mark visited

    # reconstruct path
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    # return the path
    return path

def gbfs_noprint(graph, start, goal, heuristic):
    frontier = PriorityQueue() 
    frontier.put((0, start)) 
    came_from = {start: None} 

    while not frontier.empty():
        current = frontier.get()[1]

        if current == goal:
            break

        for next_node in graph[current]:
            if next_node not in came_from:
                priority = heuristic(next_node, goal)
                frontier.put((priority, next_node))
                came_from[next_node] = current

    # reconstruct path
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    
    return path