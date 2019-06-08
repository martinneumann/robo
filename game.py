import operator


def restart_game():
    position = "000A10C10E10G10B20D20F20H20A30C30E30G30B80D80F80H80A70C70E70G70B60D60F60H6000"
    b = "000A30B40000000000000000000000000000000D6000000000000000000000000000000000000"
    c = "000B40C50000000000000000000000000000000E7000000000000000000000000000000000000"
    print(len(position))
    return position  # return begin Position for a new game


def new_position(old_position, move):
    # TODO did Peace change to King ?

    if move[0:2] == old_position[0:2]:  # delete must_move
        old_position = "00" + old_position[2:76]
    s = list(old_position)

    # remove old position and get new one
    # give the position of the beginning string
    po = old_position.find(move[0:2])
    s[po] = move[3]
    s[po+1] = move[4]
    letter = ["A", "B", "C", "D", "E", "F", "G", "H", "X"]  # move "A1 B2"
    pos_1 = int(move[1])
    pos_2 = int(move[4])
    pos_A = letter.index(move[0])
    pos_B = letter.index(move[3])
    # define king
    # try
    food = "000"
    if pos_2-2 == pos_1:  # advance w to b
        if pos_B > pos_A:  # rigth
            food = letter[pos_A + 1] + str(pos_1 + 1)
        elif pos_B < pos_A:  # left
            food = letter[pos_A - 1] + str(pos_1 + 1)
    elif pos_2+2 == pos_1:  # recule b to w
        if pos_B > pos_A:  # rigth
            food = letter[pos_A + 1] + str(pos_1 - 1)
        elif pos_B < pos_A:  # left
            food = letter[pos_A - 1] + str(pos_1 - 1)

    fo = old_position.find(food)
    s[fo - 1] = "0"
    s[fo] = "0"
    s[fo + 1] = "0"
    mid_pos = "".join(s)
    for x in range(12):
        xx = (x * 3) + 2
        xxx = xx + 3
        wpeace_pos = mid_pos[xx:xxx]
        # for white
        if wpeace_pos[2] == "8":  # define king
            s[xx] = "1"
        xx2 = xx + 36
        xxx2 = xxx + 36
        # for black
        bpeace_pos = mid_pos[xx2:xxx2]
        if bpeace_pos[2] == "1":
            s[xx2] = "1"
    # TODO define muste play move
    # 1 define if the last peace is in a serry of eating
    white_pos = old_position[2:38]
    black_pos = old_position[38:74]
    # verifi the color
    white_place = verif_place(white_pos, move[0:2])
    white_goal = verif_place(white_pos, move[3:5])
    black_place = verif_place(black_pos, move[0:2])
    black_goal = verif_place(black_pos, move[3:5])
    if white_place[0] == "0" and white_place != "000":  # if not king and it is a white turn
        if pos_1 + 2 == pos_2:  # if the white move is eating verifi if he can eat again
            second_food1 = verif_place(
                black_pos, letter[pos_B + 1] + str(pos_2 + 1))
            second_food2 = verif_place(
                black_pos, letter[pos_B - 1] + str(pos_2 + 1))
            if second_food1 != "000" and second_food1[1] != "H" and second_food1[1] != "A" and second_food1[2] != "1" and second_food1[2] != "8":
                # verify there is no black on the goal
                second_goal1_b = verif_place(
                    black_pos, letter[pos_B + 2] + str(pos_2 + 2))
                # verify there is no white on the goal
                second_goal1_w = verif_place(
                    white_pos, letter[pos_B + 2] + str(pos_2 + 2))
                # if food is there and goal is empty then you must eat
                if second_goal1_b == "000" and second_goal1_w == "000":
                    s[0] = move[3]
                    s[1] = move[4]
            if second_food2 != "000" and second_food2[1] != "H" and second_food2[1] != "A" and second_food2[2] != "1" and second_food2[2] != "8":
                second_goal2_b = verif_place(
                    black_pos, letter[pos_B - 2] + str(pos_2 + 2))
                second_goal2_w = verif_place(
                    white_pos, letter[pos_B - 2] + str(pos_2 + 2))
                if second_goal2_b == "000" and second_goal2_w == "000":
                    s[0] = move[3]
                    s[1] = move[4]

    if black_place[0] == "0" and black_place != "000":  # if not king and it is a black turn
        if pos_1 - 2 == pos_2:
            second_food1 = verif_place(
                white_pos, letter[pos_B + 1] + str(pos_2 - 1))
            second_food2 = verif_place(
                white_pos, letter[pos_B - 1] + str(pos_2 - 1))
            if second_food1 != "000" and second_food1[1] != "H" and second_food1[1] != "A" and second_food1[2] != "1" and second_food1[2] != "8":
                    # verify there is no black on the goal
                second_goal1_b = verif_place(
                    black_pos, letter[pos_B + 2] + str(pos_2 - 2))
                second_goal1_w = verif_place(
                    white_pos, letter[pos_B + 2] + str(pos_2 - 2))
                if second_goal1_b == "000" and second_goal1_w == "000":
                    s[0] = move[3]
                    s[1] = move[4]
            if second_food2 != "000" and second_food2[1] != "H" and second_food2[1] != "A" and second_food2[2] != "1" and second_food2[2] != "8":
                # verify there is no black on the goal
                second_goal2_b = verif_place(
                    black_pos, letter[pos_B - 2] + str(pos_2 - 2))
                second_goal2_w = verif_place(
                    white_pos, letter[pos_B - 2] + str(pos_2 - 2))
                if second_goal2_b == "000" and second_goal2_w == "000":
                    s[0] = move[3]
                    s[1] = move[4]
    if white_place[0] == "1" or black_place[0] == "1":  # if a king is in the move
        if (pos_1 == pos_2 - 2) or (pos_1 == pos_2 + 2):  # if the king is eating
            if white_place[0] == "1":  # white king eat black food
                second_food1 = verif_place(
                    black_pos, letter[pos_B + 1] + str(pos_2 + 1))
                second_food2 = verif_place(
                    black_pos, letter[pos_B + 1] + str(pos_2 - 1))
                second_food3 = verif_place(
                    black_pos, letter[pos_B - 1] + str(pos_2 - 1))
                second_food4 = verif_place(
                    black_pos, letter[pos_B - 1] + str(pos_2 + 1))
            if black_place[0] == "1":  # black king eat white food
                second_food1 = verif_place(
                    black_pos, letter[pos_B + 1] + str(pos_2 + 1))
                second_food2 = verif_place(
                    black_pos, letter[pos_B + 1] + str(pos_2 - 1))
                second_food3 = verif_place(
                    black_pos, letter[pos_B - 1] + str(pos_2 - 1))
                second_food4 = verif_place(
                    black_pos, letter[pos_B - 1] + str(pos_2 + 1))

            if second_food1 != "000" and second_food1[1] != "H" and second_food1[1] != "A" and second_food1[2] != "1" and second_food1[2] != "8":
                # verify there is no black on the goal
                second_goal1_b = verif_place(
                    black_pos, letter[pos_B + 2] + str(pos_2 + 2))
                second_goal1_w = verif_place(
                    white_pos, letter[pos_B + 2] + str(pos_2 + 2))
                if second_goal1_b == "000" and second_goal1_w == "000":
                    s[0] = move[3]
                    s[1] = move[4]
            if second_food2 != "000" and second_food2[1] != "H" and second_food2[1] != "A" and second_food2[2] != "1" and second_food2[2] != "8":
                # verify there is no black on the goal
                second_goal2_b = verif_place(
                    black_pos, letter[pos_B + 2] + str(pos_2 - 2))
                second_goal2_w = verif_place(
                    white_pos, letter[pos_B + 2] + str(pos_2 - 2))
                if second_goal2_b == "000" and second_goal2_w == "000":
                    s[0] = move[3]
                    s[1] = move[4]
            if second_food3 != "000" and second_food3[1] != "H" and second_food3[1] != "A" and second_food3[2] != "1" and second_food3[2] != "8":
                # verify there is no black on the goal
                second_goal3_b = verif_place(
                    black_pos, letter[pos_B - 2] + str(pos_2 - 2))
                second_goal3_w = verif_place(
                    white_pos, letter[pos_B - 2] + str(pos_2 - 2))
                if second_goal3_b == "000" and second_goal3_w == "000":
                    s[0] = move[3]
                    s[1] = move[4]
            if second_food4 != "000" and second_food4[1] != "H" and second_food4[1] != "A" and second_food4[2] != "1" and second_food4[2] != "8":
                # verify there is no black on the goal
                second_goal4_b = verif_place(
                    black_pos, letter[pos_B - 2] + str(pos_2 + 2))
                second_goal4_w = verif_place(
                    white_pos, letter[pos_B - 2] + str(pos_2 + 2))
                if second_goal4_b == "000" and second_goal4_w == "000":
                    s[0] = move[3]
                    s[1] = move[4]
    # if white_goal != "000" and black_goal != "000":#if the goal is occupied

    # if king (can advance and recule)... else(only advance) ...
    new_position = "".join(s)
    return new_position


def white_win(position):
    # if no peaces black or no possible move for white
    # TODO if no peace of the
    a = False
    white_pos = position[38:74]
    for char in white_pos:
        if (char != '0'):
            return False
    return True
    '''
    if black_pos == "0000000000000000000000000000000000000":
        a = True
    return a
    #else return false
    #TODO funktion to tell if the turn of a player is over
    '''


def black_win(position):
    # if no peaces black or no possible move for white
    # TODO if no peace of the
    a = False
    black_pos = position[2:38]
    for char in black_pos:
        if (char != '0'):
            return False
    return True
    '''
    for char in 
    if white_pos == "0000000000000000000000000000000000000":
        a = True
    return a
    #else return false
    #TODO funktion to tell if the turn of a player is over
    '''


def end_turn_player(position):
    end_turn = True
    if position[0:2] != "00":
        end_turn = False
    return end_turn


def Valid_move(position, move):  # move is in form "A1 B2"
    a = True

    letter = ["A", "B", "C", "D", "E", "F", "G", "H"]

    pos1 = move[1]
    posA = move[0]
    pos2 = move[4]
    posB = move[3]
    int_pos1 = int(pos1)
    int_pos2 = int(pos2)
    # +1 so it will be between 1 and 8 in sted of 0 and 7
    int_posA = letter.index(posA) + 1
    int_posB = letter.index(posB) + 1

    white_pos = position[2:38]
    black_pos = position[38:74]
    # verifi the color
    white_place = verif_place(white_pos, move[0:2])
    white_goal = verif_place(white_pos, move[3:5])
    black_place = verif_place(black_pos, move[0:2])
    black_goal = verif_place(black_pos, move[3:5])
    # if No Pieace in the begin move
    if white_place == "000" and black_place == "000":
        a = False
    if white_place[0] == "0" and white_place != "000":  # if not king and it is a white turn
        if int_pos1 > int_pos2:  # if not advancing
            a = False
    elif black_place[0] == "0" and black_place != "000":
        if int_pos1 < int_pos2:
            a = False
    # if the goal of played collor is occupied
    if (white_goal != "000" and white_place != "000") or (black_goal != "000" and black_place != "000"):
        a = False
    # if in the black square
    if abs(int_posA - int_posB) != abs(int_pos1 - int_pos2) or (abs(int_posA - int_posB) != 1 and abs(int_posA - int_posB) != 2):
        a = False

    # if new position is logic
    if ((int_pos1 + 1 == int_pos2) or (int_pos1 - 1 == int_pos2)) and ((int_posA + 1 == int_posB) or (int_posA - 1 == int_posB)):
        1 == 1
    elif((int_pos1 + 2 == int_pos2) or (int_pos1 - 2 == int_pos2)) and ((int_posA + 2 == int_posB) or (int_posA - 2 == int_posB)):
        if (int_pos1 + 2 == int_pos2) and (int_posA + 2 == int_posB):
            food_position = letter[int_posA] + str(int_pos1 + 1)
        elif(int_pos1 + 2 == int_pos2) and (int_posA - 2 == int_posB):
            food_position = letter[int_posA-2] + str(int_pos1 + 1)
        elif(int_pos1 - 2 == int_pos2) and (int_posA + 2 == int_posB):
            food_position = letter[int_posA] + str(int_pos1 - 1)
        elif(int_pos1 - 2 == int_pos2) and (int_posA - 2 == int_posB):
            food_position = letter[int_posA - 2] + str(int_pos1 - 1)

        food_black = verif_place(black_pos, food_position)
        food_white = verif_place(white_pos, food_position)
        # if the food with the opposite color is not in the trajectory
        if white_place != "000" and food_black == "000":
            a = False
        elif black_place != "000" and food_white == "000":
            a = False
    priority = position[0:2]  # if the priority is not played
    if priority != "00" and priority != "01" and priority != "02":
        # if in the move is not eating
        if priority != move[0:2] and ((int_pos1 - 2 == int_pos2) or(int_pos1 + 2 == int_pos2)):
            a = False
    # TODO if white is supposed to eat and he is not
    # TODO if black is supposed to eat and he is not
    if position[0:2] != "00" and position[0:2] != "01" and position[0:2] != "02":
        if position[0:2] != move[0:2] or abs(int_pos1 - int_pos2) != 2:
            a = False
    # if valid
    return a
    # else return false
# intern funktions


def verif_place(color_pos, place):  # 36 caracter in color_pos 0 1 2 ... 35 // place must be in 2 caracter exp: B1 // if it retur the same position(3 character) then it exist but if it return 000 then there is no peace in tha place
    a = "000"
    count = 1
    for x in range(12):
        pos = color_pos[count:count+2]
        count = count + 3
        # print(pos)
        if place == pos:
            a = color_pos[count-4:count-1]
    return a  # rerurn 3 char


def food_pos(move):  # return the position of the food exp:"C4" if no food the return "00"
    food = "00"
    letter = ["A", "B", "C", "D", "E", "F", "G", "H", "X"]
    pos_1 = int(move[1])
    pos_2 = int(move[4])
    pos_A = letter.index(move[0])
    pos_B = letter.index(move[3])
    if pos_1 + 2 == pos_2:  # advancing
        if pos_A + 2 == pos_B:  # right
            food = letter[pos_A + 1] + str(pos_1 + 1)
        elif pos_A - 2 == pos_B:
            food = letter[pos_A - 1] + str(pos_1 + 1)
    elif pos_1 - 2 == pos_2:
        if pos_A + 2 == pos_B:
            food = letter[pos_A + 1] + str(pos_1 - 1)
        elif pos_A - 2 == pos_B:
            food = letter[pos_A - 1] + str(pos_1 - 1)
    return food


def turn_endet(position):
    end = True
    if position[0:2] != "00":
        end = False
    return end
# TODO 9allek ismail use MAP and Filter


def print_position(position):
    # TODO
    str_list = "hello"
    white_pos = position[2:38]
    black_pos = position[38:74]
    line9 = "----------"
    line8 = "|        |8"
    line7 = "|        |7"
    line6 = "|        |6"
    line5 = "|        |5"
    line4 = "|        |4"
    line3 = "|        |3"
    line2 = "|        |2"
    line1 = "|        |1"
    line0 = "----------"
    line00 = " ABCDEFGH "
    letter = ["A", "B", "C", "D", "E", "F", "G", "H"]
    s1 = list(line1)
    s2 = list(line2)
    s3 = list(line3)
    s4 = list(line4)
    s5 = list(line5)
    s6 = list(line6)
    s7 = list(line7)
    s8 = list(line8)
    matrix_list = [s1, s2, s3, s4, s5, s6, s7, s8]

    for x in range(12):  # for white
        xx = 3 * x
        peace_w = white_pos[xx:xx+3]
        peace_b = black_pos[xx:xx+3]
        if peace_w != "000":
            x_cor_w = letter.index(peace_w[1]) + 1
            y_cor_w = int(peace_w[2]) - 1
            symbole_w = "O"
            if peace_w[0] == "1":
                symbole_w = "0"
            matrix_list[y_cor_w][x_cor_w] = symbole_w
        if peace_b != "000":
            x_cor_b = letter.index(peace_b[1]) + 1
            y_cor_b = int(peace_b[2]) - 1
            symbole_b = "X"
            if peace_b[0] == "1":
                symbole_b = "&"
            matrix_list[y_cor_b][x_cor_b] = symbole_b
    line1 = "".join(s1)
    line2 = "".join(s2)
    line3 = "".join(s3)
    line4 = "".join(s4)
    line5 = "".join(s5)
    line6 = "".join(s6)
    line7 = "".join(s7)
    line8 = "".join(s8)
    print(line9)
    print(line8)
    print(line7)
    print(line6)
    print(line5)
    print(line4)
    print(line3)
    print(line2)
    print(line1)
    print(line0)
    print(line00)

    return matrix_list
# https://thepythonguru.com/python-builtin-functions/reduce/
# TODO see Filter In Python
# TODO see reduce


def make_move(position):  # black is the KI
    move = "00"
    letter = ["A", "B", "C", "D", "E", "F", "G", "H", "X"]
    black_pos = position[38:74]
    white_pos = position[2:38]
    black_peaces = list()
    white_peaces = list()
    all_move = {}
    # generate 2 list for peaces (black and white)
    for x in range(12):
        xx = 3*x
        b_peace_string = black_pos[xx:xx+3]
        if b_peace_string != "000":
            b_peace = [int(b_peace_string[0]), letter.index(b_peace_string[1]), int(
                b_peace_string[2])]  # Warning: the letter is orgenized from 0 to 7 (not 1 to 8)
            black_peaces.append(b_peace)
        #form [peace1[d,x1,y1], peace2[d,x2,y2], ...]
        w_peace_string = white_pos[xx:xx+3]
        if w_peace_string != "000":
            w_peace = [int(b_peace_string[0]), letter.index(
                w_peace_string[1]), int(w_peace_string[2])]
            white_peaces.append(w_peace)
    # define all moves
    for x in black_peaces:
        if x[0] == 0:  # for normel black_peaces
            pos_1 = letter[x[1] + 1] + str(x[2]-1)
            pos_2 = letter[x[1] - 1] + str(x[2]-1)
            black_pos_1 = verif_place(black_pos, pos_1)
            black_pos_2 = verif_place(black_pos, pos_2)
            white_pos_1 = verif_place(white_pos, pos_1)
            white_pos_2 = verif_place(white_pos, pos_2)

            if black_pos_1 == "000" and white_pos_1 == "000":
                movement = letter[x[1]] + str(x[2]) + " " + pos_1
                priority = 1
                #all_move.update({movement_2 : priority})##########
                # add move to the dictionaries
                all_move[movement] = priority
            if black_pos_2 == "000" and white_pos_2 == "000":
                movement = letter[x[1]] + str(x[2]) + " " + pos_2
                priority = 1
                #all_move.update({movement : priority})##########
                all_move[movement] = priority
            # if there is food
            if white_pos_1 != "000":
                posA = white_pos_1[1]
                pos1 = white_pos_1[2]
                int_posA = letter.index(posA)
                int_pos1 = int(pos1)
                pos_after_food_1 = letter[int_posA + 1] + str(int_pos1 - 1)
                if verif_place(white_pos, pos_after_food_1) == "000" and verif_place(black_pos, pos_after_food_1) == "000":
                    movement_2 = letter[x[1]] + \
                        str(x[2]) + " " + pos_after_food_1
                    priority = 5
                    #all_move.update({movement_2 : priority})##########
                    all_move[movement_2] = priority
            if white_pos_2 != "000":
                posA = white_pos_2[1]
                pos1 = white_pos_2[2]
                int_posA = letter.index(posA)
                int_pos1 = int(pos1)
                pos_after_food_2 = letter[int_posA - 1] + str(int_pos1 - 1)
                if verif_place(white_pos, pos_after_food_2) == "000" and verif_place(black_pos, pos_after_food_2) == "000":
                    movement_2 = letter[x[1]] + \
                        str(x[2]) + " " + pos_after_food_2
                    priority = 5
                    #all_move.update({movement_2 : priority})##########
                    all_move[movement_2] = priority

        elif x[0] == 1:  # for Dama_peace
            pos_1 = letter[x[1] + 1] + str(x[2]-1)
            pos_2 = letter[x[1] - 1] + str(x[2]-1)
            pos_3 = letter[x[1] - 1] + str(x[2]+1)
            pos_4 = letter[x[1] + 1] + str(x[2]+1)
            black_pos_1 = verif_place(black_pos, pos_1)
            black_pos_2 = verif_place(black_pos, pos_2)
            black_pos_3 = verif_place(black_pos, pos_3)
            black_pos_4 = verif_place(black_pos, pos_4)
            white_pos_1 = verif_place(white_pos, pos_1)
            white_pos_2 = verif_place(white_pos, pos_2)
            white_pos_2 = verif_place(white_pos, pos_3)
            white_pos_2 = verif_place(white_pos, pos_4)
            if black_pos_1 == "000" and white_pos_1 == "000":
                movement = letter[x[1]] + str(x[2]) + " " + pos_1
                priority = 1
                #all_move.update({movement : priority})
                # add move to the dictionaries
                all_move[movement] = priority
            if black_pos_2 == "000" and white_pos_2 == "000":
                movement = letter[x[1]] + str(x[2]) + " " + pos_2
                priority = 1
                #all_move.update({movement : priority})
                # add move to the dictionaries
                all_move[movement] = priority
            if black_pos_3 == "000" and white_pos_3 == "000":
                movement = letter[x[1]] + str(x[2]) + " " + pos_3
                priority = 1
                #all_move.update({movement : priority})
                # add move to the dictionaries
                all_move[movement] = priority
            if black_pos_4 == "000" and white_pos_4 == "000":
                movement = letter[x[1]] + str(x[2]) + " " + pos_4
                priority = 1
                #all_move.update({movement : priority})
                # add move to the dictionaries
                all_move[movement] = priority
            # if there is food
            if white_pos_1 != "000":
                posA = white_pos_1[1]
                pos1 = white_pos_1[2]
                int_posA = letter.index(posA)
                int_pos1 = int(pos1)
                pos_after_food_1 = letter[int_posA + 1] + str(int_pos1 - 1)
                if verif_place(white_pos, pos_after_food_1) == "000" and verif_place(black_pos, pos_after_food_1) == "000":
                    movement_2 = letter[x[1]] + \
                        str(x[2]) + " " + pos_after_food_1
                    priority = 5
                    #all_move.update({movement_2 : priority})####################
                    all_move[movement_2] = priority
            if white_pos_2 != "000":
                posA = white_pos_2[1]
                pos1 = white_pos_2[2]
                int_posA = letter.index(posA)
                int_pos1 = int(pos1)
                pos_after_food_2 = letter[int_posA - 1] + str(int_pos1 - 1)
                if verif_place(white_pos, pos_after_food_2) == "000" and verif_place(black_pos, pos_after_food_2) == "000":
                    movement_2 = letter[x[1]] + \
                        str(x[2]) + " " + pos_after_food_2
                    priority = 5
                    #all_move.update({movement_2 : priority})####################
                    all_move[movement_2] = priority
            if white_pos_3 != "000":
                posA = white_pos_3[1]
                pos1 = white_pos_3[2]
                int_posA = letter.index(posA)
                int_pos1 = int(pos1)
                pos_after_food_3 = letter[int_posA - 1] + str(int_pos1 + 1)
                if verif_place(white_pos, pos_after_food_3) == "000" and verif_place(black_pos, pos_after_food_3) == "000":
                    movement_2 = letter[x[1]] + \
                        str(x[2]) + " " + pos_after_food_3
                    priority = 5
                    #all_move.update({movement_2 : priority})#####################
                    all_move[movement_2] = priority
            if white_pos_4 != "000":
                posA = white_pos_2[1]
                pos1 = white_pos_2[2]
                int_posA = letter.index(posA)
                int_pos1 = int(pos1)
                pos_after_food_4 = letter[int_posA + 1] + str(int_pos1 + 1)
                if verif_place(white_pos, pos_after_food_4) == "000" and verif_place(black_pos, pos_after_food_4) == "000":
                    movement_2 = letter[x[1]] + \
                        str(x[2]) + " " + pos_after_food_4
                    priority = 5
                    #all_move.update({movement_2 : priority})######################
                    all_move[movement_2] = priority

    move_list = list(all_move.items())
    for x in range(len(move_list)):
        abc = move_list[x][0]
        if (letter.index(abc[0]) > 7) or (letter.index(abc[3]) > 7):
            all_move.pop(abc)
        elif Valid_move(position, abc) == False:
            all_move.pop(abc)

    # move_list = all_move.items()#new list without the fals moves(well if it was there)
    # TODO if must play defined move = must play
    mmove = "0"
    if position[0:2] != "00":
        to_move = position[1]  # inial pos + ziel
        for x in range(len(move_list)):
            abc = move_list[x]
            if abc[0][1] == to_move:

                #abc[1] = a + 5
                mmove = abc[0]
                #all_move.update({abc[0]: abc[1]})
    if mmove != "0":
        move = mmove
    else:
        move = max(all_move.items(), key=operator.itemgetter(1))[0]

    # move =

    return move


def verif_collor(position, move, color):
    bool_color = False
    pos = move[0:2]
    white_pos = position[2:38]
    black_pos = position[38:74]
    if color == "black":
        if verif_place(black_pos, pos) != "000":
            bool_color = True
    if color == "white":
        if verif_place(white_pos, pos) != "000":
            bool_color = True
    # TODO if color played is correct
    return bool_color


def begin_game():
    print("New Game!!!")
    position = restart_game()
    while 1:
        print_position(position)
        print("Give the move to play(exp: A1 B2):")
        move = raw_input()
        if len(move) < 4:
            move = "00000"
        if Valid_move(position, move) == True and verif_collor(position, move, "white"):
            print("valid move  !!! :)")
            position = new_position(position, move)
            if (white_win(position)):
                print("white won")

            ki_move = make_move(position)
            position = new_position(position, ki_move)
            if position[0:2] != "00":
                ki_move = make_move(position)
                position = new_position(position, ki_move)
            if (black_win(position)):
                print("black won")
        else:
            print("unvalid move!!! :(")
    return 0


# begin_game()
