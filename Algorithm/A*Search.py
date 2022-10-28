class Node:
    """
    This class describes a single node contained within a graph. 
    It has the following instannce level attributes:
    
    ID: An integer id for the node i.e. 1
    heuristic_cost: A float value representing the estimated 
                    cost to the goal node
    """    
    def __init__(self, ID, heuristic_cost):
        self.ID = ID
        self.connected_nodes = []
        self.heuristic_cost = heuristic_cost
        
    def __repr__(self):
        ID = self.ID
        hx = self.heuristic_cost
        if len(self.connected_nodes)==0:
            nodes = 'None'
        else:
            nodes = ','.join(str(cn[1].ID) for cn in self.connected_nodes)
        return 'Node:{}\nh(n):{}\nConnected Nodes:{}'.format(ID, hx, nodes)
        
    def set_connected_nodes(self,connected_nodes):
        """
        Adds edges that lead from this node to other nodes:
        
        Parameters:
        - connected_nodes: A list of tuples consisting of (cost, Node), 
                           where 'cost' is a floating point value 
                           indicating the cost to get from this node 
                           to 'Node' and 'Node' is a Node object
        """
        self.connected_nodes = connected_nodes
    
def build_graph():
    """
    Builds the graph to be parsed by the search algorithms.
    Returns: The starting node, which is the entry point into the graph
    """
    ids = range(13)
    coords = [(0,0), (1,1), (1,0), (1,1), (5,2), (3,1), (3,0), 
              (3,-1), (5,1), (4,1), (4,0), (4,-2), (7,0)]
    
    #https://en.wikipedia.org/wiki/Euclidean_distance
    euclidean_distance = lambda x1y1, x2y2: ((x1y1[0]-x2y2[0])**2 +  (x1y1[1]-x2y2[1])**2)**(0.5)
    
    def build_connected_node_list(from_id, to_ids):
        starting_coords = coords[from_id]
        
        connected_nodes = []
        for to_id in to_ids:
            connected_nodes.append((euclidean_distance(starting_coords, coords[to_id]), all_nodes[to_id]))
            
        return connected_nodes
    
    goal_coords = (7,0)
    all_nodes = [Node(_id, euclidean_distance(coord, goal_coords)) for _id, coord in zip(ids, coords)]
    
    all_nodes[8].set_connected_nodes(build_connected_node_list(8, [12]))
    all_nodes[10].set_connected_nodes(build_connected_node_list(10,[12]))
    all_nodes[5].set_connected_nodes(build_connected_node_list(5, [8]))
    all_nodes[6].set_connected_nodes(build_connected_node_list(6, [9, 10]))
    all_nodes[7].set_connected_nodes(build_connected_node_list(7, [11]))
    all_nodes[1].set_connected_nodes(build_connected_node_list(1, [4,5]))
    all_nodes[2].set_connected_nodes(build_connected_node_list(2, [5,6]))
    all_nodes[3].set_connected_nodes(build_connected_node_list(3, [7]))
    all_nodes[0].set_connected_nodes(build_connected_node_list(0, [1,2,3]))
    
    return all_nodes[0]
    
    
import heapq

def heuristic_cost_f(path_cost, h):
    # g(n) + h(n)
    return path_cost + h

def a_star_search(starting_node, goal_node):
    """
    This function implements the A* search algorithm

    Parameters:
    - starting_node: The entry node into the graph
    - goal_node: The integer ID of the goal node.

    Returns:
    A list containing the visited node ids in order they were visited with starting node
    always being the first node and the goal node always being the last
    """

    visited_nodes_in_order = []
    store_item_to_check_frontier = []
    node = starting_node
    frontier = [(node.heuristic_cost, node.ID, node.connected_nodes)] # the priority queue 
    store_item_to_check_frontier = [node.ID] # to check if the item is in frontier or not
    heapq.heapify(frontier)

    # while the frontier is not empty
    while frontier:
      # poping the shallowest node in the frontier list
      popped_elem = heapq.heappop(frontier)
      visited_nodes_in_order.append(popped_elem[1])

      # if the popped node is the goal node, return the visited_nodes_in_order list
      if popped_elem[1] == goal_node:   
        return visited_nodes_in_order

      # loop through the popped_elem's connected nodes
      for connected_node in popped_elem[2]:
        cNode = connected_node[1] 
        new_path_cost = heuristic_cost_f(connected_node[0], cNode.heuristic_cost) 
        # check if the connected node is in visited_nodes_in_order
        if (cNode.ID not in visited_nodes_in_order) or (cNode.ID not in store_item_to_check_frontier):
          heapq.heappush(frontier, (new_path_cost, cNode.ID, cNode.connected_nodes))
          store_item_to_check_frontier.append(cNode.ID)

    return visited_nodes_in_order
    
    raise NotImplementedError()

goal_node = 12

a_star_search_answer = [0, 2, 6, 10, 12]

assert a_star_search(build_graph(), goal_node)==a_star_search_answer
