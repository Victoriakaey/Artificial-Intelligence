class Node:
    """
    This class describes a single node contained within a graph. 
    It has the following instannce level attributes:
    
    ID: An integer id for the node i.e. 1
    """    
    def __init__(self, ID):
        self.ID = ID
        self.connected_nodes = []
        
    def __repr__(self):
        ID = self.ID
        if len(self.connected_nodes)==0:
            nodes = 'None'
        else:
            nodes = ','.join(str(cn[1].ID) for cn in self.connected_nodes)
        return '\nNode:{}\nConnected Nodes:{}'.format(ID, nodes)
        
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
    Returns: All nodes with connectivity in the graph
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
    all_nodes = [Node(_id) for _id in ids]
    
    all_nodes[8].set_connected_nodes(build_connected_node_list(8, [12]))
    all_nodes[10].set_connected_nodes(build_connected_node_list(10,[12]))
    all_nodes[5].set_connected_nodes(build_connected_node_list(5, [8]))
    all_nodes[6].set_connected_nodes(build_connected_node_list(6, [9, 10]))
    all_nodes[7].set_connected_nodes(build_connected_node_list(7, [11]))
    all_nodes[1].set_connected_nodes(build_connected_node_list(1, [4,5]))
    all_nodes[2].set_connected_nodes(build_connected_node_list(2, [5,6]))
    all_nodes[3].set_connected_nodes(build_connected_node_list(3, [7]))
    all_nodes[0].set_connected_nodes(build_connected_node_list(0, [1,2,3]))
    
    return all_nodes
 
def BFS(starting_node, goal_node):
    """
    This function implements the breath first search algorithm
    
    Parameters:
    - starting_node: The entry node into the graph
    - goal_node: The integer ID of the goal node.
    
    Returns:
    A list containing the visited nodes in order they were visited with starting node
    always being the first node and the goal node always being the last
    """
    visited_nodes_in_order = []
    # YOUR CODE HERE
    node = starting_node
    frontier = [node] # a FIFO queue with node as the only element
    
    if starting_node == goal_node:
      visited_nodes_in_order.append(node.ID)

    # while the frontier is not empty
    while frontier:
      # poping the shallowest node in the frontier list
      popped_elem = frontier.pop(0)
      # if the popped node is the goal node, return the visited_nodes_in_order list
      if popped_elem.ID == goal_node: 
        visited_nodes_in_order.append(popped_elem)
        return visited_nodes_in_order
      if popped_elem not in visited_nodes_in_order:
        # adding the popped node to the visited_nodes_in_order list
        visited_nodes_in_order.append(popped_elem) 
        # loop through the popped_elem's connected nodes
        for connected_node in popped_elem.connected_nodes:
          cNode = connected_node[1]
          # check if the connected node is in visited_nodes_in_order
          if cNode not in visited_nodes_in_order:
            frontier.append(cNode)
  
    return visited_nodes_in_order
  
    raise NotImplementedError()

def DFS(starting_node, goal_node):
    """
    This function implements the depth first search algorithm
    
    Parameters:
    - starting_node: The entry node into the graph
    - goal_node: The integer ID of the goal node.
    
    Returns:
    A list containing the visited nodes in order they were visited with starting node
    always being the first node and the goal node always being the last
    """
    visited_nodes_in_order = []
    # YOUR CODE HERE
    node = starting_node
    frontier = [node] # a LIFO queue with node as the only element
    
    if starting_node == goal_node:
      visited_nodes_in_order.append(node.ID)

    # while the frontier is not empty
    while frontier:
      # poping the last node in the frontier list
      popped_elem = frontier.pop()
      # adding the popped node to the explored list
      visited_nodes_in_order.append(popped_elem) 
      # loop through the popped_elem's connected nodes
      for connected_node in popped_elem.connected_nodes:
        cNode = connected_node[1]
        # check if the connected node is in explored
        if cNode not in visited_nodes_in_order:
          # if the connected node is the goal node, return the explored list
          if cNode.ID == goal_node:
            visited_nodes_in_order.append(cNode)
            return visited_nodes_in_order
          # else, append the connected node to frontier for the code to move on
          frontier.append(cNode)
   
    return visited_nodes_in_order
  
    raise NotImplementedError()
    
    
goal_node = 12

print(BFS(build_graph()[0], goal_node))

print(DFS(build_graph()[0], goal_node))


'''
Output:

[
Node:0
Connected Nodes:1,2,3, 
Node:1
Connected Nodes:4,5, 
Node:2
Connected Nodes:5,6, 
Node:3
Connected Nodes:7, 
Node:4
Connected Nodes:None, 
Node:5
Connected Nodes:8, 
Node:6
Connected Nodes:9,10, 
Node:7
Connected Nodes:11, 
Node:8
Connected Nodes:12, 
Node:9
Connected Nodes:None, 
Node:10
Connected Nodes:12, 
Node:11
Connected Nodes:None, 
Node:12
Connected Nodes:None]
[
Node:0
Connected Nodes:1,2,3, 
Node:3
Connected Nodes:7, 
Node:7
Connected Nodes:11, 
Node:11
Connected Nodes:None, 
Node:2
Connected Nodes:5,6, 
Node:6
Connected Nodes:9,10, 
Node:10
Connected Nodes:12, 
Node:12
Connected Nodes:None]
'''
  
  
