'''
    Author @ Erik Jones
    This program is the Board of the logic game Hitori. Use GUI.py to visually show the board.
'''

from BFS_isPath import Graph, find_Path, isSafe
from pick import return_board
import setting

class Grid:
    '''Grid holds all the cubes (a matrix) '''
    def __init__(self, rows, cols, width, height, board):
        """
        Parameters
        ----------
        rows : int
            The number of rows within the matrix.
        cols : int
            The number of columns within the matrix.
        width : int
            The width of the Grid. Used for GUI.
        height : int
            The height of the Grid. Used for GUI
        board : int
            The matrix of the Values.
        """
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.selected = None
        self.board = board
    
    # Function that checks the position of the Cube on the board and checks up,left,down, and/or right depending on the location.
    # Returns False if there are 2 marked blocks next to each other.
    def adjacent_marked_check(self):
        for i in range(len(self.cubes)):
            for j in range(len(self.cubes[0])):
                if(self.cubes[i][j].mode == "marked"):
                    if(self.cubes[i][j].type == "top-left"):
                        if(self.cubes[i+1][j].mode == "marked" or self.cubes[i][j+1].mode == "marked"):
                            print("Top left rule break")
                            return False
                    elif(self.cubes[i][j].type == "top-right"):
                        if(self.cubes[i+1][j].mode == "marked" or self.cubes[i][j-1].mode == "marked"):
                            print("Top right rule break")
                            return False
                    elif(self.cubes[i][j].type == "bot-left"):
                        if(self.cubes[i-1][j].mode == "marked" or self.cubes[i][j+1].mode == "marked"):
                            print("Bottom left rule break")
                            return False
                    elif(self.cubes[i][j].type == "bot-right"):
                        if(self.cubes[i-1][j].mode == "marked" or self.cubes[i][j-1].mode == "marked"):
                            print("Bottom right rule break")
                            return False
                    elif(self.cubes[i][j].type == "top"):
                        if(self.cubes[i+1][j].mode == "marked" or self.cubes[i][j-1].mode == "marked" or self.cubes[i][j+1].mode == "marked"):
                            print("Top rule break")
                            return False
                    elif(self.cubes[i][j].type == "bot"):
                        if(self.cubes[i-1][j].mode == "marked" or self.cubes[i][j-1].mode == "marked" or self.cubes[i][j+1].mode == "marked"):
                            print("Bottom rule break")
                            return False
                    elif(self.cubes[i][j].type == "left"):
                        if(self.cubes[i-1][j].mode == "marked" or self.cubes[i+1][j].mode == "marked" or self.cubes[i][j+1].mode == "marked"):
                            print("Left rule break")
                            return False
                    elif(self.cubes[i][j].type == "right"):
                        if(self.cubes[i-1][j].mode == "marked" or self.cubes[i+1][j].mode == "marked" or self.cubes[i][j-1].mode == "marked"):
                            print("Right rule break")
                            return False
                    else:
                        if(self.cubes[i-1][j].mode == "marked" or self.cubes[i+1][j].mode == "marked" or self.cubes[i][j-1].mode == "marked" or self.cubes[i][j+1].mode == "marked"):
                            print("Middle rule")
                            return False
        return True

    
    #Uses BFS to check if there is a path to each of the non marked Cubes. Returns True if all non marked squares can reach each other.  
    def path_check(self):
        non_marked = get_white_pos(self)           # Locations within the board that are non marked
        path_matrix = get_graph_matrix(self)       # A converted matrix of the current board. 3 = path. 0 = blockage. 1 = start point. 2 = end point
        if len(non_marked) != 0:
            start_pos = non_marked.pop(0)
            path_matrix[start_pos[0]][start_pos[1]] = 1
        while(len(non_marked) != 0):
            end_point = non_marked.pop(0)
            path_matrix[end_point[0]][end_point[1]] = 2
            if find_Path(path_matrix): 
                path_matrix[end_point[0]][end_point[1]] = 3
                continue
            else: 
                return False
        return True 
        

    #Returns True if there is no non marked duplicates in the corresponding row and col
    def num_col_row_check(self):
        for i in range(len(self.cubes)):
            for j in range(len(self.cubes[0])):
                num = self.cubes[i][j].value
                if(self.cubes[i][j].mode == "none"):
                    if(check_row_col(self,num,(i,j))):
                        return False        
        return True

    #Goes through entire board (matrix) and sets each Cube's type to where it is on the board.
    #This will help the user understand where they got something wrong on the board. (W.I.P)
    def mark_all_cubes_type(self):
        for i in range(len(self.cubes)):
            for j in range(len(self.cubes[0])):
                if(i == 0):
                    if(j == 0):
                        self.cubes[i][j].type = "top-left"
                    elif(j == len(self.cubes[0])-1):
                        self.cubes[i][j].type = "top-right"
                    else:
                        self.cubes[i][j].type = "top"
                elif(j == 0):
                    if(i == len(self.cubes)-1):
                        self.cubes[i][j].type = "bot-left"
                    else:
                        self.cubes[i][j].type = "left"
                elif(i == len(self.cubes)-1):
                    if(j == len(self.cubes[0])-1):
                        self.cubes[i][j].type = "bot-right"
                    else:
                        self.cubes[i][j].type = "bot"
                elif(j == len(self.cubes[0])-1):
                    self.cubes[i][j].type = "right"
                
    #Returns the position of the mouse when clicked as a tuple.                       
    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / self.rows
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    #Changes the current Cubes mode within the matrix (row,col) to the oppsite. 
    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False
        self.cubes[row][col].selected = True
        if(self.cubes[row][col].mode == "marked"):
            self.cubes[row][col].mode = "none"
        elif(self.cubes[row][col].mode == "none"):
            self.cubes[row][col].mode = "marked"

        self.selected = (row, col)
    
    #Sets every Cubes mode to "None". This will set all squares to white in the GUI.
    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_mode("none")
    
class Cube:
    '''A Cube is one of the squares within the board. A 5 x 5 board would have 25 Cubes'''

    def __init__(self, value, row, col, width ,height):
        """
        Parameters
        ----------
        value : int
            The value within the Cube. On a 5 x 5 board, the value range is 1-5.
        row : int
            The row number within the matrix.
        col : int
            The col number within the matrix.
        width : int
            The width of the Grid. Used for GUI
        height : int
            The height of the Grid. Used for GUI
        """

        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.mode = "none"
        self.type = "none"
        self.selected = False
    
    def set_mode(self, mode):
        self.mode = mode

# Helper function for num_row_col_check.Returns True if the current position has duplicates in the corresponding row or column that aren't marked.
def check_row_col(self,num,pos):
        for i in range(len(self.cubes[0])):
            if (self.cubes[pos[0]][i].mode == "none" and self.cubes[pos[0]][i].value == num and pos[1] != i):
                return True
        for i in range(len(self.cubes)):
            if (self.cubes[i][pos[1]].mode == "none" and self.cubes[i][pos[1]].value == num and pos[0] != i):
                return True
        return False


#Returns the current board as a matrix with 0's and 3's which is used in BFS_isPath.py. 0 is "marked" which indicates a path blockage.
#3 represents a path that can be traveled on.
def get_graph_matrix(self):
        temp = self.board
        for i in range(len(self.cubes)):
            for j in range(len(self.cubes[0])):
                if(self.cubes[i][j].mode == "marked"):
                    temp[i][j] = 0
                else:
                    temp[i][j] = 3   
        return temp

#Returns a list of tuples of each of the positions on the Grid that is not marked (aka.White squares)
def get_white_pos(self):
        unmarked = []
        for i in range(len(self.cubes)):
            for j in range(len(self.cubes[0])):
                if(self.cubes[i][j].mode == "none"):
                    unmarked.append(tuple((i,j)))                  
        return unmarked