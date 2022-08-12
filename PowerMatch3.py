import random
import pygame
import math

# includes the rewards you get from things like 4-in-a-rows.
# to store this data, board carries tuples (color, type)
# types are:
# 0: normal
# 1: bomb
# 2: cross bomb
# (6,3): power crystal

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

gem_anim_time = 5000
gem_anim_timer = 0

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
    gem_anim_timer += clock.get_time()
    gem_anim_timer %= gem_anim_time

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
        # find match 3s
        to_remove = []
        for row in range(boardheight):
            currentstreak = 0
            currentcolor = -1
            for col in range(boardwidth):
                if board[row][col][0] == currentcolor:
                    currentstreak+=1
                else:
                    # end the streak
                    if currentstreak == 3:
                        for i in range(1,currentstreak+1):
                            to_remove.append((row,col-i))
                    elif currentstreak == 4:
                        # TODO: spawn the powergem at the "creating gem"
                        to_remove.append((row,col-1))
                        to_remove.append((row,col-2))
                        to_remove.append((row,col-4))
                        board[row][col-3] = (currentcolor, 1)
                    elif currentstreak >= 5:
                        for i in range(1,currentstreak+1):
                            if i != 3: 
                                to_remove.append((row,col-i))
                        board[row][col-3] = (len(colors), 3)
                    # start a new one
                    currentcolor = board[row][col][0]
                    currentstreak = 1

        
        # for col in range(boardwidth):
        #     currentstreak = 0
        #     currentcolor = -1
        #     for row in range(boardheight):
        #         if board[row][col][0] == currentcolor:
        #             currentstreak+=1
        #         else:
        #             # end the streak
        #             if currentstreak == 3:
        #                 for i in range(1,currentstreak+1):
        #                     to_remove.append((row,col-i))
        #             elif currentstreak == 4:
        #                 # TODO: spawn the powergem at the "creating gem"
        #                 to_remove.append((row,col-1))
        #                 to_remove.append((row,col-2))
        #                 to_remove.append((row,col-4))
        #                 board[row][col-3] = (currentcolor, 1)
        #             elif currentstreak >= 5:
        #                 for i in range(1,currentstreak+1):
        #                     if i != 3: 
        #                         to_remove.append((row,col-i))
        #                 board[row][col-3] = (len(colors), 3)
        #             # start a new one
        #             currentcolor = board[row][col][0]
        #             currentstreak = 1

        for r,c in to_remove:
            board[r][c] = None


    # falling logic
    if game_state == "PreAnimating": 
        for row in range(boardheight-1, -1, -1):
            for col in range(boardwidth):
                if board[row][col] == None:
                    is_falling[row][col] = True
                    if row == 0:
                        board[row][col] = (random.randint(0,len(colors)-1),0)
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
                if board[row][col][0] == len(colors):
                    color = pygame.Color(0,0,0)
                    color.hsva = (360*gem_anim_timer/gem_anim_time,100,100,100)
                elif board[row][col][1] == 0:
                    color = colors[board[row][col][0]]
                elif board[row][col][1] == 1:
                    flux = math.sin(5*(2*math.pi*gem_anim_timer/gem_anim_time))
                    mult = 0.8 + (0.2 * flux)
                    color = pygame.Color(colors[board[row][col][0]])
                    color.hsva = (color.hsva[0], color.hsva[1], color.hsva[2]*mult, color.hsva[3])

                do_fall_anim = is_falling[row][col] and (game_state == "Animating" or game_state == "PreAnimating")
                pygame.draw.ellipse(
                    screen,
                    color,
                    (
                        col*tilesize + padding/2,
                        row*tilesize + padding/2 - (tilesize*(1-(fall_timer/fall_time)) if do_fall_anim else 0),
                        tilesize - padding,
                        tilesize - padding
                    )
                )
    pygame.display.flip()