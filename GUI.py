'''
    Author @ Erik Jones
    This program visually displays an hitori board. The user has the ability to choose what size board they want and can click to mark a Cube.
    Currently includes a checker to see if the user's input are correct for any size board.
    
    Upcoming Feature(s):
    -   Add more set Boards (currently around only 10 per board size).
    -   The ability to go back and play another random Board.
    -   Complete random board with speed run type high scores.
    Possible upcoming Feature(s):
    -   Solver.
'''
import pygame
import time
from board import Grid
from board import Cube
from pick import return_board
import setting

pygame.font.init()
setting.initialize()

def draw(self, win):
        # Draws Grid Lines
        gap = int(self.width / setting.number)
        for i in range(self.rows+1):
            thick = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draws Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                the_cube = self.cubes[i][j]
                pos = tuple((i,j))
                draw_cubes(the_cube,win,pos)

def draw_cubes(self, win,pos):
        fnt = pygame.font.SysFont("comicsans", 60 - (2 * setting.number))       #Sets the text size comapred to the board size.
        spacing = (self.width / setting.number) - 3
        gap = self.width / setting.number
        x = self.col * gap
        y = self.row * gap

        # If Cube has been clicked, then the square will appear black with a white number.
        # This indicates the cube as "marked".
        if (self.mode == "marked"):
            text = fnt.render(str(self.value), 1, (255,255,255))
            pygame.draw.rect(win, (0,0,0), (x+2,y+2, spacing , spacing))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        # White Cube with black number if not "marked".    
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

# Displays to the pygame output the main menu. Within the main menu the user can pick the board size.
def reddraw_main_menu(picker):
    pygame.display.set_caption("What size board?")
    mouse = pygame.mouse.get_pos()
    picker.fill((127,0,255))        # Fills the background to a purple color.
    check_fnt = pygame.font.SysFont("comicsans",30)
    header_text = check_fnt.render("Choose Board Size",1,(0,0,0))
    picker.blit(header_text, (183,40))
    
    # Checks to see if mouse is on one of the following buttons
    # 5x5 button with text
    if(setting.picked_5):
        pygame.draw.rect(picker, (0 ,201,87), (220,100,100,40))
    elif(220 + 100 > mouse[0] > 220 and 100 + 40 > mouse[1] > 100):
        pygame.draw.rect(picker, (0 ,201,87), (220,100,100,40), 3)
    else:
        pygame.draw.rect(picker, (255 ,215,0), (220,100,100,40))
    check_text = check_fnt.render("5 x 5",1,(0,0,0))
    picker.blit(check_text, (246,110))
    
    # 6x6 button with text.
    if(setting.picked_6):
        pygame.draw.rect(picker, (0 ,201,87), (220,160,100,40))
    elif(220 + 100 > mouse[0] > 220 and 160 + 40 > mouse[1] > 160):
        pygame.draw.rect(picker, (0 ,201,87), (220,160,100,40),3)
    else:
        pygame.draw.rect(picker, (255,215,0), (220,160,100,40))
    check_text = check_fnt.render("6 x 6",1,(0,0,0))
    picker.blit(check_text, (246,170))
    
    # 7x7 button with text.
    if(setting.picked_7):
        pygame.draw.rect(picker, (0 ,201,87), (220,220,100,40))
    elif(220 + 100 > mouse[0] > 220 and 220 + 40 > mouse[1] > 220):
        pygame.draw.rect(picker, (0 ,201,87), (220,220,100,40),3)
    else:
        pygame.draw.rect(picker, (255,215,0), (220,220,100,40))
    check_text = check_fnt.render("7 x 7",1,(0,0,0))
    picker.blit(check_text, (246,230))

    # Continue Button.
    if(420 + 100 > mouse[0] > 420 and 580 + 40 > mouse[1] > 580):
        pygame.draw.rect(picker, (0 ,201,20), (420,580,100,40),3)    
    else:
        pygame.draw.rect(picker, (0 ,201,20), (420,580,100,40))

    
    check_text = check_fnt.render("Continue",1,(0,0,0))
    picker.blit(check_text, (426,590))
    

# Displays to the pygame output the current Hittori Board.
def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))     #Fills the background to white.
    fnt = pygame.font.SysFont("comicsans", 40)
    check_fnt = pygame.font.SysFont("comicsans",30)

    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 160, 560))
    mouse = pygame.mouse.get_pos()
    
    # Checks to see if mouse position is within the "check..." box
    if(260 + 100 > mouse[0] > 260 and 550 + 40 > mouse[1] > 550):
        pygame.draw.rect(win, (0 ,201,87), (260,550,100,40), 3)
    else:
        pygame.draw.rect(win, (255 ,215,0), (260,550,100,40))
    check_text = check_fnt.render("Check...",1,(0,0,0))
    win.blit(check_text, (270,560))

    # Draw Strikes
    text_strikes = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text_strikes, (20, 560))
    
    # Draw grid and board
    draw(board,win)

# Returns Min : sec
def format_time(secs):
    sec = secs%60
    minute = secs//60
    if(sec < 10):
        mat = " " + str(minute) + ":0" + str(sec) 
    else:
        mat = " " + str(minute) + ":" + str(sec)
    return mat    

# Returns True if button was clicked.    
def button(x,y,w,h,pos):
    if(x+w > pos[0] > x and y+h > pos[1] > y):
        return True

# Removes the buttons apperance of being selected for all buttons.                           
def button_selected_toFalse():
    setting.picked_5 = False
    setting.picked_6 = False
    setting.picked_7 = False
    
def main():
    width = 540
    height = 650
    main_menu = pygame.display.set_mode((width,height))
    mode_pick = True
    run = True
    
    while mode_pick:
        reddraw_main_menu(main_menu)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mode_pick = False
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if(button(220,100,100,40,pos)):
                    setting.number = 5
                    button_selected_toFalse()
                    setting.picked_5 = True
                if(button(220,160,100,40,pos)):
                    setting.number = 6
                    button_selected_toFalse()
                    setting.picked_6 = True
                if(button(220,220,100,40,pos)):
                    setting.number = 7
                    button_selected_toFalse()
                    setting.picked_7 = True
                if(button(420,580,100,40,pos)):
                    mode_pick = False             
        pygame.display.update()

    win = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Hitori")
    the_board = return_board(setting.number)        # Sets the board to a random board based on what size board the user chose.
    board = Grid(setting.number, setting.number, 540, 540,the_board)
    board.mark_all_cubes_type()
    start = time.time()
    strikes = 0
    
    while run:
        play_time = round(time.time() - start) 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                #Checks to if a button is clicked below the board
                if(button(260,550,100,40,pos)):
                    if(strikes <= 8):
                        strikes += 1
                    if(board.path_check()):
                        print("All non marked squares can reach each other")
                    else:
                        print("Marked Cubes are blocking off non marked cubes, Wrong")
                    if(board.adjacent_marked_check() and board.num_col_row_check() and board.path_check()):
                        print("win")  
                    else:
                        print("fail")   
            
                #checks to see if game board is clicked
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])   
        redraw_window(win, board, play_time, strikes)
        pygame.display.update()
main()
pygame.display.quit