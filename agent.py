#!/usr/bin/python

import os,sys
from copy import deepcopy

board = [[99, -8, 8, 6, 6, 8, -8, 99], 
         [-8, -24, -4, -3, -3, -4, -24, -8], 
         [8, -4, 7, 4, 4, 7, -4, 8], 
         [6, -3, 4, 0, 0, 4, -3, 6], 
         [6, -3, 4, 0, 0, 4, -3, 6], 
         [8, -4, 7, 4, 4, 7, -4, 8], 
         [-8, -24, -4, -3, -3, -4, -24, -8], 
         [99, -8, 8, 6, 6, 8, -8, 99]]
coord_name_map = {'root':'root','pass':'pass',(0,0):'a1',(1,0):'a2',(2,0):'a3',(3,0):'a4',(4,0):'a5',(5,0):'a6',(6,0):'a7',(7,0):'a8',
(0,1):'b1',(1,1):'b2',(2,1):'b3',(3,1):'b4',(4,1):'b5',(5,1):'b6',(6,1):'b7',(7,1):'b8',
(0,2):'c1',(1,2):'c2',(2,2):'c3',(3,2):'c4',(4,2):'c5',(5,2):'c6',(6,2):'c7',(7,2):'c8',
(0,3):'d1',(1,3):'d2',(2,3):'d3',(3,3):'d4',(4,3):'d5',(5,3):'d6',(6,3):'d7',(7,3):'d8',
(0,4):'e1',(1,4):'e2',(2,4):'e3',(3,4):'e4',(4,4):'e5',(5,4):'e6',(6,4):'e7',(7,4):'e8',
(0,5):'f1',(1,5):'f2',(2,5):'f3',(3,5):'f4',(4,5):'f5',(5,5):'f6',(6,5):'f7',(7,5):'f8',
(0,6):'g1',(1,6):'g2',(2,6):'g3',(3,6):'g4',(4,6):'g5',(5,6):'g6',(6,6):'g7',(7,6):'g8',
(0,7):'h1',(1,7):'h2',(2,7):'h3',(3,7):'h4',(4,7):'h5',(5,7):'h6',(6,7):'h7',(7,7):'h8'
}

input_file = open("input.txt","r")
line_list = input_file.readlines()

algo_type = int(line_list[0].strip('\n'))

my_player = line_list[1].strip('\n')

if my_player == 'X':
    opponent = 'O'
else:
    opponent = 'X'

cuttingoff_depth = int(line_list[2].strip('\n'))

input_file.close()
alpha= -2147483647 
beta = 2147483647
passes = 0
current_scene = [] 
position_score_dict = {}    
possible_score= []
possible_solutions = []
position_flips_dict = {}
position_moves_dict = {}
child_parent_dict = {}
move_board_dict = {}
printable_mm_output = [] 
final_print = []
node_value_dict = {} 
printable_ab_output = [] 
parent_child_dict = {}
traversal_till_now = [] 

for i in range(3,11):
    split_string = list(line_list[i].strip('\n'))
    current_scene.append(split_string)

def get_positions(player):
    my_row = []
    my_indices = []
    row_num = 0
    for row in current_scene:
        if player in row:
            my_count = row.count(player)
            search_from = 0
            for coins in range(0,my_count):
                my_index = row.index(player, search_from) 
                my_indices.append(my_index)            
                search_from = my_index+1
                row_index_tuple = (row_num, my_index)
                my_row.append(row_index_tuple)
        row_num = row_num+1 

    return my_row 

def get_playerscore(current_scene,player):
    player_positions = get_positions(player)
    player_score = 0
    for pos in player_positions:
        player_score = player_score+board[pos[0]][pos[1]]

    return player_score


def get_current_scores(current_scene, player):
    player_positions = get_positions(my_player)

    if player == 'O':
        other_player = 'X'
    else:
        other_player = 'O'

    other_player_pos = get_positions(other_player)

    player_score = 0
    for pos in player_positions:
        player_score = player_score+board[pos[0]][pos[1]] 

    for o_pos in other_player_pos:
        other_player_score = other_player_score+board[pos[0]][pos[1]]  

    score = player_score - other_player_score
    return score 

def check_east(position,flips):
            local_flips = []
            if position[1]+1 >7:
                return []

            elif current_scene[position[0]][position[1]+1] == '*':
                return [] 

            elif current_scene[position[0]][position[1]+1] == my_player:
                return [] 

            elif current_scene[position[0]][position[1]+1] == opponent:
                local_flips.append((position[0],position[1]+1))
                for diag in range(2,8):
                    if position[1]+diag > 7:
                        break

                    if current_scene[position[0]][position[1]+diag] == opponent:
                        local_flips.append((position[0],position[1]+diag))
                        continue

                    elif current_scene[position[0]][position[1]+diag] == my_player:
                        flips = local_flips
                        return flips

                    else:
                        break
                return [] 
            else:
                return []


def check_west(position,flips):
            local_flips = []
            if position[1]-1 <0:
                return []

            elif current_scene[position[0]][position[1]-1] == '*':
                return [] 

            elif current_scene[position[0]][position[1]-1] == my_player:
                return [] 

            elif current_scene[position[0]][position[1]-1] == opponent:
                local_flips.append((position[0],position[1]-1))
                for diag in range(2,8):
                    if position[1]-diag < 0:
                        break

                    if current_scene[position[0]][position[1]-diag] == opponent:
                        local_flips.append((position[0],position[1]-diag))
                        continue

                    elif current_scene[position[0]][position[1]-diag] == my_player:
                        flips = local_flips
                        return flips 

                    else:
                        break
                return [] 
            else:
                return []

def check_north(position,flips):
            local_flips=[] 
            if position[0]-1 < 0:
                return []

            elif current_scene[position[0]-1][position[1]] == '*':
                return [] 

            elif current_scene[position[0]-1][position[1]] == my_player:
                return [] 

            elif current_scene[position[0]-1][position[1]] == opponent:
                local_flips.append((position[0]-1,position[1]))
                for diag in range(2,8):
                    if position[0]-diag < 0 :
                        break
   
                    if current_scene[position[0]-diag][position[1]] == opponent:
                        local_flips.append((position[0]-diag,position[1])) 
                        continue

                    elif current_scene[position[0]-diag][position[1]] == my_player:
                        flips = local_flips
                        return flips

                    else:
                        break
                return [] 
            else:
                return []

def check_south(position,flips):
            local_flips=[] 
            if position[0]+1 > 7:
                return []

            elif current_scene[position[0]+1][position[1]] == '*':
                return [] 

            elif current_scene[position[0]+1][position[1]] == my_player:
                return [] 

            elif current_scene[position[0]+1][position[1]] == opponent:
                local_flips.append((position[0]+1,position[1]))
                for diag in range(2,8):
                    if position[0]+diag > 7 :
                        break

                    if current_scene[position[0]+diag][position[1]] == opponent:
                        local_flips.append((position[0]+diag,position[1]))
                        continue

                    elif current_scene[position[0]+diag][position[1]] == my_player:
                       flips = local_flips
                       return flips 

                    else:
                        break
                return [] 
            else:
                return []

def check_SE(position,flips):
            local_flips=[] 
            if position[0]+1 > 7 or position[1]+1 > 7:
                return []

            elif current_scene[position[0]+1][position[1]+1] == '*':
                return [] 

            elif current_scene[position[0]+1][position[1]+1] == my_player:
                return [] 

            elif current_scene[position[0]+1][position[1]+1] == opponent:
                local_flips.append((position[0]+1,position[1]+1))
                for diag in range(2,8):
                    if position[0]+diag > 7 or position[1]+diag > 7:
                        break

                    if current_scene[position[0]+diag][position[1]+diag] == opponent:
                        local_flips.append((position[0]+diag,position[1]+diag))
                        continue

                    elif current_scene[position[0]+diag][position[1]+diag] == my_player:
                        flips = local_flips
                        return flips

                    else:
                        break
                return [] 
            else:
                return []

def check_SW(position,flips):
            local_flips=[] 
            if position[0]+1 > 7 or position[1]-1 < 0:
                return []

            elif current_scene[position[0]+1][position[1]-1] == '*':
                return [] 

            elif current_scene[position[0]+1][position[1]-1] == my_player:
                return [] 

            elif current_scene[position[0]+1][position[1]-1] == opponent:
                local_flips.append((position[0]+1,position[1]-1))
                for diag in range(2,8):
                    if position[0]+diag > 7 or position[1]-diag < 0:
                        break

                    if current_scene[position[0]+diag][position[1]-diag] == opponent:
                        local_flips.append((position[0]+diag,position[1]-diag))
                        continue

                    elif current_scene[position[0]+diag][position[1]-diag] == my_player:
                        flips = local_flips
                        return flips

                    else:
                        break
                return [] 
            else:
                return []

def check_NE(position,flips):
            local_flips=[] 

            if position[0]-1 < 0 or position[1]+1 >7:
                return []

            elif current_scene[position[0]-1][position[1]+1] == '*':
                return [] 

            elif current_scene[position[0]-1][position[1]+1] == my_player:
                return [] 

            elif current_scene[position[0]-1][position[1]+1] == opponent:
                local_flips.append((position[0]-1,position[1]+1))
                for diag in range(2,8):
                    if position[0]-diag < 0 or position[1]+diag > 7:
                        break

                    if current_scene[position[0]-diag][position[1]+diag] == opponent:
                        local_flips.append((position[0]-diag,position[1]+diag))
                        continue

                    elif current_scene[position[0]-diag][position[1]+diag] == my_player:
                        flips = local_flips
                        return flips

                    else:
                        break
                return [] 
            else:
                return []

def check_NW(position,flips):
            local_flips = []
            if position[0]-1 < 0 or position[1]-1 < 0:
                return []

            elif current_scene[position[0]-1][position[1]-1] == '*':
                return [] 

            elif current_scene[position[0]-1][position[1]-1] == my_player:
                return [] 

            elif current_scene[position[0]-1][position[1]-1] == opponent:
                local_flips.append((position[0]-1,position[1]-1))

                for diag in range(2,8):
                    if position[0]-diag < 0 or position[1]-diag < 1:
                        break

                    if current_scene[position[0]-diag][position[1]-diag] == opponent:
                        local_flips.append((position[0]-diag,position[1]-diag)) 
                        continue

                    elif current_scene[position[0]-diag][position[1]-diag] == my_player:
                        flips = local_flips
                        return flips

                    else:
                        break

                return [] 
            else:
                return []

        
def calculate_score(possible_move, player):

    flips = []
    if possible_move == (0,0): 
        flips.extend(check_east(possible_move,flips))
        flips.extend(check_SE(possible_move,flips))
        flips.extend(check_south(possible_move,flips)) 


    elif possible_move == (0,7): 
        flips.extend(check_west(possible_move,flips))
        flips.extend(check_SW(possible_move,flips))
        flips.extend(check_south(possible_move,flips)) 


    elif possible_move == (7,7): 
        flips.extend(check_west(possible_move,flips))
        flips.extend(check_NW(possible_move,flips))
        flips.extend(check_north(possible_move,flips))


    elif possible_move == (7,0): 
        flips.extend(check_east(possible_move,flips))
        flips.extend(check_NE(possible_move,flips))
        flips.extend(check_north(possible_move,flips))


    elif possible_move[0] == 0:
        flips.extend(check_west(possible_move,flips))
        flips.extend(check_east(possible_move,flips))
        flips.extend(check_south(possible_move,flips))
        flips.extend(check_SW(possible_move,flips))
        flips.extend(check_SE(possible_move,flips))

    elif possible_move[0] == 7:
        flips.extend(check_west(possible_move,flips))
        flips.extend(check_east(possible_move,flips))
        flips.extend(check_north(possible_move,flips))
        flips.extend(check_NW(possible_move,flips))
        flips.extend(check_NE(possible_move,flips))

    elif possible_move[1] == 0:
        flips.extend(check_north(possible_move,flips))
        flips.extend(check_east(possible_move,flips))
        flips.extend(check_south(possible_move,flips))
        flips.extend(check_NE(possible_move,flips))
        flips.extend(check_SE(possible_move,flips))

    elif possible_move[1] == 7:
        flips.extend(check_north(possible_move,flips))
        flips.extend(check_west(possible_move,flips))
        flips.extend(check_south(possible_move,flips))
        flips.extend(check_NW(possible_move,flips))
        flips.extend(check_SW(possible_move,flips))

    else:
       flips.extend(check_north(possible_move,flips))
       flips.extend(check_west(possible_move,flips))
       flips.extend(check_south(possible_move,flips))
       flips.extend(check_east(possible_move,flips))
       flips.extend(check_NW(possible_move,flips))
       flips.extend(check_SW(possible_move,flips)) 
       flips.extend(check_NE(possible_move,flips))
       flips.extend(check_SE(possible_move,flips)) 
    if flips != []:
        flips.append((possible_move[0],possible_move[1]))
        position_flips_dict[possible_move] = flips

    opponent_reduced_score = 0
    final_score =0
    score_from_flips = 0
    
    player_scores = get_playerscore(current_scene,my_player)

    position_flips_dict[possible_move] = flips
    for flip in flips:
        score_from_flips = score_from_flips+board[flip[0]][flip[1]]

    opp_positions = get_positions(opponent)
    for o_pos in opp_positions:
        if o_pos in flips:
            continue

        else:
            opponent_reduced_score = opponent_reduced_score+board[o_pos[0]][o_pos[1]] 

    final_score_for_position = score_from_flips+player_scores-opponent_reduced_score
    position_score_dict[possible_move] = final_score_for_position

def valid_move_north(current_scene,position):
    possible_move = ()
    if position[0]-1 < 0:
        return

    elif current_scene[position[0]-1][position[1]] == opponent: 
        for diag in range(2,8):
                    if position[0]-diag < 0 :
                        break

                    if current_scene[position[0]-diag][position[1]] == opponent:
                        continue

                    elif current_scene[position[0]-diag][position[1]] == '*':
                        possible_move = (position[0]-diag,position[1])
                        break 

                    else:
                        break
        if possible_move != ():
            possible_score.append(calculate_score(possible_move,my_player))

def valid_move_NW(current_scene, position):
    possible_move = ()
    if position[0]-1 < 0 or position[1]-1 < 0:
        return

    elif current_scene[position[0]-1][position[1]-1] == opponent: 
        for diag in range(2,8):
                    if position[0]-diag < 0 :
                        break

                    if current_scene[position[0]-diag][position[1]-diag] == opponent:
                        continue

                    elif current_scene[position[0]-diag][position[1]-diag] == '*':
                        possible_move = (position[0]-diag,position[1]-diag)
                        break 

                    else:
                        break    
        if possible_move != ():
            possible_score.append(calculate_score(possible_move,my_player))

def valid_move_NE(current_scene, position):
    possible_move = ()
    if position[0]-1 < 0 or position[1]+1 > 7:
        return

    elif current_scene[position[0]-1][position[1]+1] == opponent: 
        for diag in range(2,8):
                    if position[0]-diag < 0 or position[1]+diag > 7:
                        break

                    if current_scene[position[0]-diag][position[1]+diag] == opponent:
                        continue

                    elif current_scene[position[0]-diag][position[1]+diag] == '*':
                        possible_move = (position[0]-diag,position[1]+diag)  
                        break

                    else:
                        break
        if possible_move != ():
            possible_score.append(calculate_score(possible_move,my_player))
 
def valid_move_west(current_scene, position):
    possible_move = ()
    if position[1]-1 < 0:
        return

    elif current_scene[position[0]][position[1]-1] == opponent: 
        for diag in range(2,8):
                    if position[1]-diag < 0:
                        break

                    if current_scene[position[0]][position[1]-diag] == opponent:
                        continue

                    elif current_scene[position[0]][position[1]-diag] == '*':
                        possible_move = (position[0],position[1]-diag)
                        break  

                    else:
                        break
        if possible_move != ():
            possible_score.append(calculate_score(possible_move,my_player))

def valid_move_east(current_scene, position):
    possible_move = ()
    if position[1]+1 > 7:
        return 

    elif current_scene[position[0]][position[1]+1] == opponent: 
        for diag in range(2,8):
                    if position[1]+diag > 7:
                        break

                    if current_scene[position[0]][position[1]+diag] == opponent:
                        continue

                    elif current_scene[position[0]][position[1]+diag] == '*':
                        possible_move = (position[0],position[1]+diag)    
                        break

                    else:
                        break  
        if possible_move != ():
            possible_score.append(calculate_score(possible_move,my_player))

def valid_move_SW(current_scene, position):
    possible_move = ()
    if position[0]+1 > 7 or position[1]-1 < 0:
        return

    elif current_scene[position[0]+1][position[1]-1] == opponent: 
        for diag in range(2,8):
                    if position[0]+diag > 7 or position[1]-diag < 0:
                        break

                    if current_scene[position[0]+diag][position[1]-diag] == opponent:
                        continue

                    elif current_scene[position[0]+diag][position[1]-diag] == '*':
                        possible_move = (position[0]+diag,position[1]-diag)  
                        break 

                    else:
                        break
        if possible_move != ():
            possible_score.append(calculate_score(possible_move,my_player))
 
def valid_move_SE(current_scene, position):
    possible_move = ()
    if position[0]+1 > 7 or position[1]+1 > 7:
        return

    elif current_scene[position[0]+1][position[1]+1] == opponent: 
        for diag in range(2,8):
                    if position[0]+diag > 7 or position[1]+diag > 7:
                        break

                    if current_scene[position[0]+diag][position[1]+diag] == opponent:
                        continue

                    elif current_scene[position[0]+diag][position[1]+diag] == '*':
                        possible_move = (position[0]+diag,position[1]+diag)   
                        break 

                    else:
                        break  
        if possible_move != ():
            possible_score.append(calculate_score(possible_move,my_player))

def valid_move_south(current_scene, position): 
    possible_move = ()
    if position[0]+1 > 7:
        return

    elif current_scene[position[0]+1][position[1]] == opponent: 
        for diag in range(2,8):
                    if position[0]+diag > 7 :
                        break

                    if current_scene[position[0]+diag][position[1]] == opponent:
                        continue

                    elif current_scene[position[0]+diag][position[1]] == '*':
                        possible_move = (position[0]+diag,position[1])
                        break

                    else:
                        break 
        if possible_move != ():
            possible_score.append(calculate_score(possible_move,my_player))


def greedy():
    positions = []
    positions = get_positions(my_player) 
    
    for position in positions:
        if position[0] != 0 and position[1] != 0 and position[0] != 7 and position[1] != 7:
        
            valid_move_north(current_scene,position)
            valid_move_NW(current_scene, position) 
            valid_move_NE(current_scene, position)
            valid_move_west(current_scene, position)
            valid_move_east(current_scene, position)
            valid_move_SW(current_scene, position)
            valid_move_south(current_scene, position)
            valid_move_SE(current_scene,position)

        if position[0] == 0 and position[1] == 0:
            valid_move_east(current_scene, position)
            valid_move_south(current_scene, position)
            valid_move_SE(current_scene,position) 

        if position[0] == 0 and position[1] == 7:
            valid_move_west(current_scene, position)
            valid_move_SW(current_scene, position)
            valid_move_south(current_scene, position)


        if position[0] == 7 and position[1] == 0:
            valid_move_north(current_scene,position)
            valid_move_NE(current_scene, position) 
            valid_move_east(current_scene, position)

 
        if position[0] == 7 and position[1] == 7:
            valid_move_west(current_scene, position)
            valid_move_north(current_scene,position)
            valid_move_NW(current_scene, position)
 

        if position[0] == 0:
            valid_move_east(current_scene, position)
            valid_move_SE(current_scene,position) 
            valid_move_west(current_scene, position)
            valid_move_SW(current_scene, position)
            valid_move_south(current_scene, position)
            
        if position[0] == 7:
            valid_move_north(current_scene,position)
            valid_move_NE(current_scene, position) 
            valid_move_east(current_scene, position)
            valid_move_west(current_scene, position)
            valid_move_NW(current_scene, position)
            

        if position[1] == 0:
            valid_move_north(current_scene,position)
            valid_move_NE(current_scene, position) 
            valid_move_east(current_scene, position)
            valid_move_SE(current_scene,position) 
            valid_move_south(current_scene, position)


        if position[1] == 7: 
            valid_move_north(current_scene,position)
            valid_move_south(current_scene, position)
            valid_move_west(current_scene, position)
            valid_move_SW(current_scene, position)
            valid_move_NW(current_scene, position)
            
def print_output_into_file(next_move):
    output_file = open("output.txt","w") 
    for row in next_move:
        output_file.write("".join(row)+'\n')

    output_file.close()


def check_end_game():
    no_space = 0
    for row in current_scene:
        if '*' not in row:
            no_space = no_space+1
        
    if no_space == 8:
        print_output_into_file(current_scene)
    exit(0)



def mm_move_north(current_scene,position,list_of_valid_moves,other_player):
    possible_move = ()
    if position[0]-1 < 0:
        return

    elif current_scene[position[0]-1][position[1]] == other_player:
        for diag in range(2,8):
                    if position[0]-diag < 0 :
                        break

                    if current_scene[position[0]-diag][position[1]] == other_player:
                        continue

                    elif current_scene[position[0]-diag][position[1]] == '*':
                        possible_move = (position[0]-diag,position[1])
                        break

                    else:
                        break
        if possible_move != ():
            list_of_valid_moves.append(possible_move)
            return list_of_valid_moves 


def mm_move_NW(current_scene, position,list_of_valid_moves,other_player):
 
    possible_move = ()
    if position[0]-1 < 0 or position[1]-1 < 0:
        return

    elif current_scene[position[0]-1][position[1]-1] == other_player:
        for diag in range(2,8):
                    if position[0]-diag < 0 :
                        break

                    if current_scene[position[0]-diag][position[1]-diag] == other_player:
                        continue

                    elif current_scene[position[0]-diag][position[1]-diag] == '*':
                        possible_move = (position[0]-diag,position[1]-diag)
                        break

                    else:
                        break
        if possible_move != ():
            list_of_valid_moves.append(possible_move)
            return list_of_valid_moves 
            

def mm_move_NE(current_scene, position,list_of_valid_moves,other_player):

    possible_move = ()
    if position[0]-1 < 0 or position[1]+1 > 7:
        return

    elif current_scene[position[0]-1][position[1]+1] == other_player:
        for diag in range(2,8):
                    if position[0]-diag < 0 or position[1]+diag > 7:
                        break

                    if current_scene[position[0]-diag][position[1]+diag] == other_player:
                        continue

                    elif current_scene[position[0]-diag][position[1]+diag] == '*':
                        possible_move = (position[0]-diag,position[1]+diag)
                        break

                    else:
                        break
        if possible_move != ():
            list_of_valid_moves.append(possible_move)
            return list_of_valid_moves 
            

def mm_move_west(current_scene, position,list_of_valid_moves,other_player):
    possible_move = ()
    if position[1]-1 < 0:
        return

    elif current_scene[position[0]][position[1]-1] == other_player:
        for diag in range(2,8):
                    if position[1]-diag < 0:
                        break

                    if current_scene[position[0]][position[1]-diag] == other_player:
                        continue

                    elif current_scene[position[0]][position[1]-diag] == '*':
                        possible_move = (position[0],position[1]-diag)
                        break

                    else:
                        break
        if possible_move != ():
            list_of_valid_moves.append(possible_move)
            return list_of_valid_moves 
            

def mm_move_east(current_scene, position,list_of_valid_moves,other_player):
    possible_move = ()
    if position[1]+1 > 7:
        return

    elif current_scene[position[0]][position[1]+1] == other_player:
        for diag in range(2,8):
                    if position[1]+diag > 7:
                        break

                    if current_scene[position[0]][position[1]+diag] == other_player:
                        continue

                    elif current_scene[position[0]][position[1]+diag] == '*':
                        possible_move = (position[0],position[1]+diag)
                        break

                    else:
                        break
        if possible_move != ():
            list_of_valid_moves.append(possible_move)
            return list_of_valid_moves 
            

def mm_move_SW(current_scene, position,list_of_valid_moves,other_player):
    possible_move = ()
    if position[0]+1 > 7 or position[1]-1 < 0:
        return

    elif current_scene[position[0]+1][position[1]-1] == other_player:
        for diag in range(2,8):
                    if position[0]+diag > 7 or position[1]-diag < 0:
                        break

                    if current_scene[position[0]+diag][position[1]-diag] == other_player:
                        continue

                    elif current_scene[position[0]+diag][position[1]-diag] == '*':
                        possible_move = (position[0]+diag,position[1]-diag)
                        break

                    else:
                        break
        if possible_move != ():
            list_of_valid_moves.append(possible_move)
            return list_of_valid_moves 

def mm_move_SE(current_scene, position,list_of_valid_moves,other_player):
    possible_move = ()
    if position[0]+1 > 7 or position[1]+1 > 7:
        return

    elif current_scene[position[0]+1][position[1]+1] == other_player:
        for diag in range(2,8):
                    if position[0]+diag > 7 or position[1]+diag > 7:
                        break

                    if current_scene[position[0]+diag][position[1]+diag] == other_player:
                        continue

                    elif current_scene[position[0]+diag][position[1]+diag] == '*':
                        possible_move = (position[0]+diag,position[1]+diag)
                        break

                    else:
                        break
        if possible_move != ():
            list_of_valid_moves.append(possible_move)
            return list_of_valid_moves 

def mm_move_south(current_scene, position,list_of_valid_moves,other_player):
    possible_move = ()
    if position[0]+1 > 7:
        return

    elif current_scene[position[0]+1][position[1]] == other_player:
        for diag in range(2,8):
                    if position[0]+diag > 7 :
                        break

                    if current_scene[position[0]+diag][position[1]] == other_player:
                        continue

                    elif current_scene[position[0]+diag][position[1]] == '*':
                        possible_move = (position[0]+diag,position[1])
                        break

                    else:
                        break
        if possible_move != ():
            list_of_valid_moves.append(possible_move)
            return list_of_valid_moves 


        
def check_all_directions(current_scene,position,player):

        list_of_valid_moves = []
        if player == 'X':
            other_player = 'O'
        else:
            other_player = 'X'

        if position[0] != 0 and position[1] != 0 and position[0] != 7 and position[1] != 7:

            mm_move_north(current_scene,position,list_of_valid_moves,other_player)
            mm_move_NW(current_scene, position,list_of_valid_moves,other_player)
            mm_move_NE(current_scene, position,list_of_valid_moves,other_player)
            mm_move_west(current_scene, position,list_of_valid_moves,other_player)
            mm_move_east(current_scene, position,list_of_valid_moves,other_player)
            mm_move_SW(current_scene, position,list_of_valid_moves,other_player)
            mm_move_south(current_scene, position,list_of_valid_moves,other_player)
            mm_move_SE(current_scene,position,list_of_valid_moves,other_player)

        if position[0] == 0 and position[1] == 0:
            mm_move_east(current_scene, position,list_of_valid_moves,other_player)
            mm_move_south(current_scene, position,list_of_valid_moves,other_player)
            mm_move_SE(current_scene,position,list_of_valid_moves,other_player)

        if position[0] == 0 and position[1] == 7:
            mm_move_west(current_scene, position,list_of_valid_moves,other_player)
            mm_move_SW(current_scene, position,list_of_valid_moves,other_player)
            mm_move_south(current_scene, position,list_of_valid_moves,other_player)


        if position[0] == 7 and position[1] == 0:
            mm_move_north(current_scene,position,list_of_valid_moves,other_player)
            mm_move_NE(current_scene, position,list_of_valid_moves,other_player)
            mm_move_east(current_scene, position,list_of_valid_moves,other_player)


        if position[0] == 7 and position[1] == 7:
            mm_move_west(current_scene, position,list_of_valid_moves,other_player)
            mm_move_north(current_scene,position,list_of_valid_moves,other_player)
            mm_move_NW(current_scene, position,list_of_valid_moves,other_player)


        if position[0] == 0:
            mm_move_east(current_scene, position,list_of_valid_moves,other_player)
            mm_move_SE(current_scene,position,list_of_valid_moves,other_player)
            mm_move_west(current_scene, position,list_of_valid_moves,other_player)
            mm_move_SW(current_scene, position,list_of_valid_moves,other_player)
            mm_move_south(current_scene, position,list_of_valid_moves,other_player)

        if position[0] == 7:
            mm_move_north(current_scene,position,list_of_valid_moves,other_player)
            mm_move_NE(current_scene, position,list_of_valid_moves,other_player)
            mm_move_east(current_scene, position,list_of_valid_moves,other_player)
            mm_move_west(current_scene, position,list_of_valid_moves,other_player)
            mm_move_NW(current_scene, position,list_of_valid_moves,other_player)


        if position[1] == 0:
            mm_move_north(current_scene,position,list_of_valid_moves,other_player)
            mm_move_NE(current_scene, position,list_of_valid_moves,other_player)
            mm_move_east(current_scene, position,list_of_valid_moves,other_player)
            mm_move_SE(current_scene,position,list_of_valid_moves,other_player)
            mm_move_south(current_scene, position,list_of_valid_moves,other_player)


        if position[1] == 7:
            mm_move_north(current_scene,position,list_of_valid_moves,other_player)
            mm_move_south(current_scene, position,list_of_valid_moves,other_player)
            mm_move_west(current_scene, position,list_of_valid_moves,other_player)
            mm_move_SW(current_scene, position,list_of_valid_moves,other_player)
            mm_move_NW(current_scene, position,list_of_valid_moves,other_player) 
  
        list_of_valid_moves.sort()
        list_of_valid_moves = list(set(list_of_valid_moves))
        return list_of_valid_moves

def mm_get_positions(player,scene):
    my_row = []
    my_indices = []
    row_num = 0
    for row in scene:
        if player in row:
            my_count = row.count(player)
            search_from = 0
            for coins in range(0,my_count):
                my_index = row.index(player, search_from) 
                my_indices.append(my_index)            
                search_from = my_index+1
                row_index_tuple = (row_num, my_index)
                my_row.append(row_index_tuple)
        row_num = row_num+1 

    return my_row 

def mm_get_playerscore(player, current_board):
    player_positions = mm_get_positions(player, current_board)
    player_score = 0
    for pos in player_positions:
        player_score = player_score+board[pos[0]][pos[1]]

    return player_score 

def get_children(player,scene):
     
    positions = []
    legal_moves= []
    positions = mm_get_positions(player,scene) 
    positions.sort() 
    for position in positions:
        legal_moves.extend(check_all_directions(scene,position,player)) 
        position_moves_dict[position] = legal_moves 

    return legal_moves

def get_all_flips(position,parent_board,player):
   local_flips = []
   flips = []

   if player == 'X':
      other_player = 'O'
   else:
      other_player = 'X'

   if position[1]-1 < 0:
       pass

   elif parent_board[position[0]][position[1]-1] == other_player:
      local_flips.append((position[0],position[1]-1))
      for diag in range(2,8):
          if position[1]-diag < 0:
              break

          if parent_board[position[0]][position[1]-diag] == other_player:
              local_flips.append((position[0],position[1]-diag))
              continue

          elif parent_board[position[0]][position[1]-diag] == player:
              flips.extend(local_flips)

          else:
              break
         
   local_flips = []
   if position[1]+1 >7 :
       pass 

   elif parent_board[position[0]][position[1]+1] == other_player:
      local_flips.append((position[0],position[1]+1))
      for diag in range(2,8):
          if position[1]+diag > 7:
              break

          if parent_board[position[0]][position[1]+diag] == other_player:
              local_flips.append((position[0],position[1]+diag))
              continue

          elif parent_board[position[0]][position[1]+diag] == player:
              flips.extend(local_flips)

          else:
              break

   local_flips = []
   if position[0]+1 > 7:
       pass 

   elif parent_board[position[0]+1][position[1]] == other_player:
       local_flips.append((position[0]+1,position[1]))
       for diag in range(2,8):
           if position[0]+diag > 7 :
               break

           if parent_board[position[0]+diag][position[1]] == other_player:
               local_flips.append((position[0]+diag,position[1]))
               continue

           elif parent_board[position[0]+diag][position[1]] == player:
               flips.extend(local_flips)
  
           else:
               break

   local_flips = []
   if position[0]-1 < 0:
       pass 

   elif parent_board[position[0]-1][position[1]] == other_player:
       local_flips.append((position[0]-1,position[1]))
       for diag in range(2,8):
           if position[0]-diag < 0 :
               break

           if parent_board[position[0]-diag][position[1]] == other_player:
               local_flips.append((position[0]-diag,position[1]))
               continue

           elif parent_board[position[0]-diag][position[1]] == player:
               flips.extend(local_flips)

           else:
               break

   local_flips = []
   if position[0]+1 > 7 or position[1]-1 < 0:
       pass 

   elif parent_board[position[0]+1][position[1]-1] == other_player:
       local_flips.append((position[0]+1,position[1]-1))
       for diag in range(2,8):
           if position[0]+diag > 7 or position[1]-diag <0:
               break

           if parent_board[position[0]+diag][position[1]-diag] == other_player:
               local_flips.append((position[0]+diag,position[1]-diag))
               continue

           elif parent_board[position[0]+diag][position[1]-diag] == player:
               flips.extend(local_flips)

           else:
               break
 
   local_flips = []
   if position[0]+1 >7 or position[1]+1 >7:
       pass 

   elif parent_board[position[0]+1][position[1]+1] == other_player:
       local_flips.append((position[0]+1,position[1]+1))
       for diag in range(2,8):
           if position[0]+diag > 7 or position[0]+diag > 7:
               break

           if parent_board[position[0]+diag][position[1]+diag] == other_player:
               local_flips.append((position[0]+diag,position[1]+diag))
               continue

           elif parent_board[position[0]+diag][position[1]+diag] == player:
               flips.extend(local_flips)

           else:
               break

   local_flips = []
   if position[0]-1 < 0 or position[1]+1 > 7:
       pass 

   elif parent_board[position[0]-1][position[1]+1] == other_player:
       local_flips.append((position[0]-1,position[1]+1))
       for diag in range(2,8):
           if position[0]-diag < 0  or position[1]+diag > 7:
               break

           if parent_board[position[0]-diag][position[1]+diag] == other_player:
               local_flips.append((position[0]-diag,position[1]+diag))
               continue

           elif parent_board[position[0]-diag][position[1]+diag] == player:
              flips.extend(local_flips)

           else:
               break

   local_flips = []
   if position[0]-1 < 0 or position[1]-1 < 0:
       pass 

   elif parent_board[position[0]-1][position[1]-1] == other_player:
       local_flips.append((position[0]-1,position[1]-1))
       for diag in range(2,8):
           if position[0]-diag < 0  or position[0]-diag < 0:
               break

           if parent_board[position[0]-diag][position[1]-diag] == other_player:
               local_flips.append((position[0]-diag,position[1]-diag))
               continue

           elif parent_board[position[0]-diag][position[1]-diag] == player:
               flips.extend(local_flips)

           else:
               break
   return flips

def create_board_for(position,parent_board,player):
    flips = []
    flips = get_all_flips(position,parent_board,player)
    modified_current_scene = deepcopy(parent_board)
    if flips != []:
        flips.append(position)
        for flip_item in flips:
            modified_current_scene[flip_item[0]][flip_item[1]] = player

    return modified_current_scene

def calculate_value(node, current_board,player):
    
    my_score =mm_get_playerscore(my_player, current_board)

    opponent_score = mm_get_playerscore(opponent, current_board)

    final_score_for_position = my_score-opponent_score
    return final_score_for_position 


def check_if_node_terminates(player,check_board):
    derived = get_children(player,check_board)
    if derived == []:
        return True 
    else:
        return False


def print_mm_output_to_file(next_scene, printable_mm_output):
    output_file = open("output.txt","w")
    for line in next_scene:
        output_file.write("".join(line)+"\n")

    output_file.write("Node,Depth,Value"+"\n")

    for ele in printable_mm_output:
        node = ele[0]
        node_name = coord_name_map[node]
        value = str(ele[2])

        if value == "-2147483647":
            value = "-Infinity"
        elif value == "2147483647":
            value = "Infinity"
        output_file.write(str(node_name)+","+str(ele[1])+","+value+"\n")

def print_ab_output_to_file(next_scene, print_ab_output):
    output_file = open("output.txt","w")
    for line in next_scene:
        output_file.write("".join(line)+"\n")

    output_file.write("Node,Depth,Value,Alpha,Beta"+"\n")

    for ele in printable_ab_output:
        node = ele[0]
        node_name = coord_name_map[node]
        value = str(ele[2])
        alpha = str(ele[3])
        beta = str(ele[4])

        if value =="-2147483647": 
            value = "-Infinity"
        elif value=="2147483647":
            value = "Infinity"
        if alpha == "-2147483647":
            alpha = "-Infinity"
        elif alpha == "2147483647":
            alpha = "Infinity"
        if beta == "-2147483647":
            beta = "-Infinity"
        elif beta == "2147483647":
            beta = "Infinity"
 
        output_file.write(str(node_name)+","+str(ele[1])+","+value+","+alpha+","+beta+"\n")



def AIMA_minimax_maxval(node,depth,current_board,is_terminal,player):
    if(depth == cuttingoff_depth):

        calculated_value = calculate_value(node,current_board,player)
        printable_mm_output.append((node,depth,calculated_value)) 
        return calculated_value 

    v = -2147483647    

    if is_terminal == True:

        calculated_value = calculate_value(node,current_board,player)

        opp_is_terminal = check_if_node_terminates(opponent,current_board)
        printable_mm_output.append(("pass",depth+1,v))

        v1 = AIMA_minimax_minval("pass" ,depth+1, current_board, opp_is_terminal,opponent) 
        return v1

    children = get_children(my_player,current_board) 
    children.sort()
    if node != 'pass':
        printable_mm_output.append((node,depth,v))

    for child in children:
        child_board = create_board_for(child, current_board, my_player)
        is_terminal = check_if_node_terminates(opponent,child_board)

        if is_terminal == True:
            calculated_val = calculate_value(child,child_board,opponent)
            printable_ab_output.append((child,depth+1,calculated_val))

        v = max(v,AIMA_minimax_minval(child, depth+1, child_board, is_terminal,opponent))
        if (check_if_node_terminates(opponent, current_board) == True):
            printable_mm_output.append(("pass",depth,v))
        else:
            printable_mm_output.append((node,depth,v))

    return v


def AIMA_minimax_minval(node,depth,current_board,is_terminal,player):
    if(depth == cuttingoff_depth): 

        calculated_value = calculate_value(node,current_board,player)
        printable_mm_output.append((node,depth,calculated_value)) 
        return calculated_value

    v = 2147483647

    if is_terminal == True:

        opp_is_terminal = check_if_node_terminates(my_player,current_board)
        printable_mm_output.append(("pass",depth+1,v))

        v1 = AIMA_minimax_maxval(node, depth+1, current_board, is_terminal,my_player) 
        return v1

    children = get_children(opponent, current_board)
    children.sort()
    if node != 'pass':
        printable_mm_output.append((node,depth,v)) 

    for child in children:
        child_board = create_board_for(child, current_board,  opponent)
        is_terminal = check_if_node_terminates(my_player, child_board)

        if is_terminal == True:
            calculated_val = calculate_value(child,child_board,my_player)
            printable_ab_output.append((child,depth+1,calculated_val))

        v = min(v,AIMA_minimax_maxval(child, depth+1, child_board, is_terminal,my_player)) 
        if (check_if_node_terminates(my_player,current_board) == True):
            printable_mm_output.append(("pass",depth,v))
        else:
            printable_mm_output.append((node,depth,v))

    return v


def AIMA_minimax_initiation(): 
    node = ('root')
    depth = 0
    global move_board_dict
    global printable_mm_output
    next_move = ()

    is_terminal = check_if_node_terminates(my_player,current_scene)

    v = AIMA_minimax_maxval(node,depth,current_scene,is_terminal,my_player) 

    printable_mm_output.append((node,depth,v))
    if printable_mm_output[-1] == printable_mm_output[-2]:
        printable_mm_output.pop()

    if v == -2147483647:
        next_scene = current_scene

    elif len(printable_mm_output) > 1:
        for pos in printable_mm_output:
            if pos[2] == v and pos[1] == 1:
                next_move = pos[0]
                break

        if next_move== ('root') or next_move == 'pass':
            next_scene = current_scene
        else:
            next_scene = create_board_for(next_move,current_scene,my_player)
    else:
        next_scene = current_scene

    print_mm_output_to_file(next_scene, printable_mm_output)
        

def AIMA_AB_max_val(node,depth,current_board,is_terminal,player,alpha,beta):

    if  depth == cuttingoff_depth:

        calculated_value = calculate_value(node,current_board,player)
        printable_ab_output.append((node,depth,calculated_value,alpha,beta)) 
        
        return calculated_value

    v = -2147483647

    if is_terminal==True:

        if depth == 0:
            printable_ab_output.append((node,depth,v,alpha,beta))

        opp_is_terminal = check_if_node_terminates(opponent,current_board)
        printable_ab_output.append(("pass",depth+1,v,alpha,beta))

        v1 = AIMA_AB_min_val("pass", depth+1, current_board, opp_is_terminal,opponent, alpha, beta) 

        return v1

    children = get_children(my_player, current_board)
    children.sort()
    if node != 'pass':
        printable_ab_output.append((node,depth,v,alpha,beta))

    for child in children:
        child_board = create_board_for(child, current_board,  my_player)

        is_terminal = check_if_node_terminates(opponent, child_board)
        if is_terminal == True:
            calculated_val = calculate_value(child,child_board,opponent)
            printable_ab_output.append((child,depth+1,calculated_val,alpha,beta))

        v = max(v,AIMA_AB_min_val(child, depth+1, child_board, is_terminal, opponent,alpha,beta))

        if v >= beta:
            printable_ab_output.append((node,depth,v,alpha,beta))
            return v
        alpha = max(alpha,v)
        printable_ab_output.append((node,depth,v,alpha,beta))
        

    return v

def AIMA_AB_min_val(node,depth,current_board,is_terminal,player,alpha,beta):

    if depth == cuttingoff_depth:

        calculated_value = calculate_value(node,current_board,player)
        printable_ab_output.append((node,depth,calculated_value,alpha,beta))

        return calculated_value

    v = 2147483647

    if is_terminal==True:

        opp_is_terminal = check_if_node_terminates(my_player,current_board)
        printable_ab_output.append(("pass",depth+1,v,alpha,beta))

        v1 = AIMA_AB_max_val("pass", depth+1, current_board, opp_is_terminal,my_player, alpha, beta) 

        
        return v1

    children = get_children(opponent, current_board) 
    children.sort()
    if node != 'pass':
        printable_ab_output.append((node,depth,v,alpha,beta))

    for child in children:
        child_board = create_board_for(child, current_board, opponent)
        is_terminal = check_if_node_terminates(my_player, child_board)
        if is_terminal == True:
            calculated_val = calculate_value(child,child_board,my_player)
            printable_ab_output.append((child,depth+1,calculated_val,alpha,beta))
 
        v = min(v,AIMA_AB_max_val(child, depth+1, child_board, is_terminal, my_player, alpha,beta))

        if v<=alpha:
            printable_ab_output.append((node,depth,v,alpha,beta))
            return v
        beta = min(beta,v)
        printable_ab_output.append((node,depth,v,alpha,beta))
    return v


def AIMA_alphabeta_initiation():
    node = ('root')
    depth = 0
    global printable_ab_output 
    global alpha
    global beta
    next_move = ()

    is_terminal = check_if_node_terminates(my_player,current_scene)

    v = AIMA_AB_max_val(node,depth,current_scene,is_terminal,my_player,alpha,beta) 

    if alpha != v:
        alpha = max(alpha,v)

    printable_ab_output.append((node,depth,v,alpha,beta))
    if printable_ab_output[-1] == printable_ab_output[-2]:
        printable_ab_output.pop() 
    if v == -2147483647:
        next_scene = current_scene 

    elif len(printable_ab_output) > 1:

        for pos in printable_ab_output:
            if pos[2] == v and pos[1] == 1:
                next_move = pos[0]
                break

        if next_move== ('root') or next_move == 'pass':
            next_scene = current_scene
        else:
            next_scene = create_board_for(next_move,current_scene,my_player)

    else:
        next_scene = current_scene

    print_ab_output_to_file(next_scene, printable_ab_output) 


if algo_type == 1:
    
    greedy() 
    scores = []
    scores = position_score_dict.values()
    position_score_items = position_score_dict.items()
    desc_scores = sorted(scores)
    desc_scores.reverse()

    if len(position_score_dict) == 0:
        print_output_into_file(current_scene) 
        exit(0)
        
    highest_score = desc_scores[0]
    possible_solutions = []

    duplicate_count = desc_scores.count(highest_score)
    if duplicate_count == 1:
        for high in position_score_items:
            if high[1] == highest_score:

                possible_solutions.append(high[0])

    elif duplicate_count > 1:
        position_score_items = position_score_dict.items()

        for item in position_score_items:
            if item[1] == highest_score:
                possible_solutions.append(item[0])

    possible_solutions.sort()
    final_destination = possible_solutions[0]   

    modified_current_scene = deepcopy(current_scene) 

    for path in position_flips_dict.keys():
        if path == final_destination:
            flip_list = position_flips_dict[path] 
            for flip_item in flip_list:
                modified_current_scene[flip_item[0]][flip_item[1]] = my_player

            print_output_into_file(modified_current_scene)

elif algo_type == 2:
    AIMA_minimax_initiation()

elif algo_type == 3:
    AIMA_alphabeta_initiation()
