import random
import pygame

# game constants
boardwidth = 10
boardheight = 10

colors = [(255,255,255), (255,255,0), (255,0,255), (0,255,255), (255,0,0), (0,255,0), (0,0,255)]
# less colors means more chain reactions
# colors = [(255,255,255), (255,255,0), (255,0,255), (0,255,255)]
selectcolor = (128,128,128)

board = [[None for j in range(boardwidth)] for k in range(boardheight)]

# possible gamestates are:
# Idle - awating user input
# Animating - peices are falling, user cannot input
# PreIdle - no longer animating, but still no input
# PreAnimating - animation will happen, but logic for falling has not been performed yet
game_state = "PreIdle"

# how long does it take to fall one block in milliseconds
fall_time = 200
fall_timer = 0
is_falling = [[False for j in range(boardwidth)] for k in range(boardheight)]

# during the animation gamestate, everything is in the position it will eventually be in,
# and anything that is falling is marked in is_falling

prev_selected = None

# pygame initialization/constants
tilesize = 50
padding = 10
size = (boardwidth * tilesize, boardheight * tilesize)

pygame.init()
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()


# mainloop
flag = True
while flag:
    clock.tick(40)

    # update game_state
    # game_state is also updated whenever you take an action
    if game_state == "Idle" or game_state == "PreIdle":
        stable = True
        for row in range(boardheight-1, -1, -1):
            for col in range(boardwidth):
                if board[row][col] == None:
                    stable = False
        
        if stable:
            game_state = "Idle"
        else:
            game_state = "PreAnimating"
            prev_selected = None
            fall_timer = 0

    elif game_state == "Animating" or game_state == "PreAnimating":
        fall_timer += clock.get_time()
        if fall_timer > fall_time:
            stable = True
            for row in range(boardheight-1, -1, -1):
                for col in range(boardwidth):
                    if board[row][col] == None:
                        stable = False
            
            if stable:
                game_state = "PreIdle"
            else:
                game_state = "PreAnimating"
                fall_timer = 0
        else:
            game_state = "Animating"
    
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                flag = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                tilepos = (event.pos[0]//tilesize, event.pos[1]//tilesize)
                if game_state == "Idle":
                    if prev_selected == None:
                        prev_selected = tilepos
                    else:
                        eudist = abs(tilepos[0]-prev_selected[0]) + abs(tilepos[1]-prev_selected[1])
                        if eudist == 1:
                            temp = board[tilepos[1]][tilepos[0]]
                            board[tilepos[1]][tilepos[0]] = board[prev_selected[1]][prev_selected[0]]
                            board[prev_selected[1]][prev_selected[0]] = temp
                            prev_selected = None
                            game_state = "PreIdle"
                        else:
                            prev_selected = tilepos
    
    # match 3 logic
    if game_state == "PreIdle":
        to_remove = []
        for row in range(boardheight):
            for col in range(boardwidth-2):
                if board[row][col] == board[row][col+1] and board[row][col] == board[row][col+2]:
                    to_remove.append((row,col))
                    to_remove.append((row,col+1))
                    to_remove.append((row,col+2))
        for row in range(boardheight-2):
            for col in range(boardwidth):
                if board[row][col] == board[row+1][col] and board[row][col] == board[row+2][col]:
                    to_remove.append((row,col))
                    to_remove.append((row+1,col))
                    to_remove.append((row+2,col))

        for r,c in to_remove:
            board[r][c] = None


    # falling logic
    if game_state == "PreAnimating": 
        for row in range(boardheight-1, -1, -1):
            for col in range(boardwidth):
                if board[row][col] == None:
                    is_falling[row][col] = True
                    if row == 0:
                        board[row][col] = random.randint(0,len(colors)-1)
                    else:
                        board[row][col] = board[row-1][col]
                        board[row-1][col] = None
                else:
                    is_falling[row][col] = False
                

    # draw the screen
    screen.fill((0,0,0))

    if prev_selected is not None:
        pygame.draw.ellipse(
            screen,
            selectcolor,
            (
                prev_selected[0]*tilesize,
                prev_selected[1]*tilesize,
                tilesize,
                tilesize
            )
        )

    for row in range(boardheight):
        for col in range(boardwidth):
            if board[row][col] is not None:
                do_fall_anim = is_falling[row][col] and (game_state == "Animating" or game_state == "PreAnimating")
                pygame.draw.ellipse(
                    screen,
                    colors[board[row][col]],
                    (
                        col*tilesize + padding/2,
                        row*tilesize + padding/2 - (tilesize*(1-(fall_timer/fall_time)) if do_fall_anim else 0),
                        tilesize - padding,
                        tilesize - padding
                    )
                )
    pygame.display.flip()