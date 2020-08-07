'''
    Author @ Erik Jones
    Traversing algorithm that explores all of the neighbor nodes at the present depth prior to moving on to the nodes at the next depth level.
    
'''
from collections import defaultdict 
class Graph:
    # Adjacency list.
    def __init__(self): 
        self.graph = defaultdict(list) 
      
    def addEdge(self, u, v): 
        self.graph[u].append(v) 
  
    # BFS function to find path from source to destination.     
    def BFS(self, s, d, num):    
        if s == d: 
            return True
              
        # Mark all the vertices as not visited.  
        visited = ([False]*((num) + 1)) 
        queue = [] 
        queue.append(s) 
        visited[s] = True

        while(queue): 
            # Remove a vertex from queue.
            s = queue.pop(0) 
            
            # Get all adjacent vertices of the dequeued vertex s.  
            for i in self.graph[s]: 
                # Returns True if the current node is the destination.  
                if i == d: 
                    return True

                # Continue to do BFS.    
                if visited[i] == False: 
                    queue.append(i) 
                    visited[i] = True
  
        # Returns False if queue empties, indicating there is no path.
        return False

# Returns True if index is not out of bounds and not a 'blocked' index (0 indicates a blocked path).
def isSafe(i, j, matrix):
    if i >= 0 and i < len(matrix) and j >= 0 and j < len(matrix[0]) and matrix[i][j] != 0:
        return True
    else: 
        return False
  
# Returns True if there is a path between Start and Destination.
def find_Path(board): 
    start, destination = None, None # Start and Destination  
    n = len(board) 
    g = Graph() 
    num = (n * n)
    
    # Create graph with n * n nodes    
    k = 1 # Number of the start vertex. 
    for i in range(n): 
        for j in range(n):
            if (board[i][j] != 0): 
                # Connects all 4 adjacent cell to current cell if not its not a 'blocked' index.  
                if (isSafe(i, j + 1, board)): 
                    g.addEdge(k, k + 1) 
                if (isSafe(i, j - 1, board)): 
                    g.addEdge(k, k - 1) 
                if (isSafe(i + 1, j, board)): 
                    g.addEdge(k, k + n) 
                if (isSafe(i - 1, j, board)): 
                    g.addEdge(k, k - n) 

            # Sets the start index. 
            if (board[i][j] == 1): 
                start = k 
  
            # Destination index.     
            if (board[i][j] == 2): 
                destination = k 
            k += 1
    # Find path Using the BFS algorithm.
    return g.BFS(start, destination,num) 