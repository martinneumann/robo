#!/usr/bin/env python

import camera
import numpy as np
import cv2
import game as rules
from gi.repository import Gtk
import gi
import importlib
import socket
import sys
import time
from operator import itemgetter
gi.require_version('Gtk', '3.0')

displayWindow = cv2.namedWindow("displayWindow", cv2.WINDOW_NORMAL)


edges = []
board_fields = {}

current_player = 1  # player 1 or 2
current_piece = []  # position of current piece
current_target = []  # position of target move
current_move = []  # move [piece_position, move_type]
validation_move = ""  # move for validation
lbl_player = None
lbl_moves = None
position = None
player_has_won = False
game_type = "none"
eat_move = "00"
number_of_beaten_pieces = 0
current_garbage = 0
gargabe_pos = ['A0', 'A9']


class communicationManager():
    receivedMessage = ""    # response received from robot
    messageToSend = ""      # message to be sent
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    current_player = 1

    def __init__(self):
        print("setup")

    def _connect(self):
        server_address = ("192.168.0.101", 9000)
        print("connecting to server, address is: " + str(server_address))
        # sock.bind(('', 9000))
        self.sock.connect(server_address)

    def _disconnect(self):
        self.sock.close()

    def sendMove(self, move):
        for msg in move:
            # loop over all messages and send them
            # wait for response before sending another
            self.sock.sendall(msg)
            print("send data " + msg)
            receivedMessage = self.sock.recv(2)
            if (receivedMessage == "ok"):
                print("received 'ok'")
                continue
            elif (receivedMessage == "error"):
                print("Robot reported an error.")
                break
            else:
                continue


comManager = communicationManager()


class gui(Gtk.Window):
    def on_window1_destroy(self, object, data=None):
        print("quit with cancel")
        Gtk.main_quit()

    def on_gtk_quit_activate(self, menuitem, data=None):
        print("quit from menu")
        Gtk.main_quit()

    def __init__(self):
        Gtk.Window.__init__(self)


# state machine


class state(object):
    def __init__(self):
        print("Current state: " + str(self.__class__.__name__))

# class calibration:


class initial(state):
    def __init__(self):
        print("Welcome! \nDo you want to start a game against a human or against me, the AI?\nPress 1 for human vs. human and 2 for human vs. AI!")

    def on_event(self, event):
        # initialization
        if event == '1':
            return new_game_human()
        if event == '2':
            return new_game_cpu()
        return self


class new_game_human(state):
    def __init__(self):
        print("Ok then! A game against another human!\n")

    def on_event(self, event):
        # start new game human vs. human

        if event == '1':
            return find_piece()
        return self


class new_game_cpu(state):
    def __init__(self):
        print("Ok then! You want to play against me! Let's start.\n")

    def on_event(self, event):
        # start new game human vs. cpu

        if event == '1':
            return find_piece()
        return self


class find_piece(state):
    def __init__(self):
        print("Can you help me find the next piece? Please point at it.\n")

    def on_event(self, event):
        # find the piece the human is pointing at
        # detectGesture()

        if event == '1':
            return find_location()
        return self


class find_location():
    def __init__(self):
        print("Thanks! Can you show me where to move it next? Confirm when done!\n")

    def on_event(self, event):
        # chain of locations is possible

        if event == '1':
            return find_location()
        if event == '2':
            return perform_move()
        return self


class perform_move():
    def __init__(self):
        print("I'm moving the piece now...\n")

    def on_event(self, event):
        # perform this move

        if event == '1':
            return change_player()
        return self


class change_player():
    def __init__(self):
        print("It's now the other player's turn!\n")

    def on_event(self, event):
        # change the player human -> human2 or -> cpu, cpu -> human
        if event == '1':
            return find_piece()
        return self


class state_machine(object):
    def __init__(self):
        # self.state = calibration()
        print("test")

    def on_event(self, event):
        self.state = self.state.on_event(event)

#
# Gtk Handler functions
#


class Handler:
    # handlers for gui events
    current_player = 1

    def connectToServer(self, button):
        # connects to the robot
        comManager._connect()
        label = builder.get_object("connectionState")

        label.set_text("connected")
        print("Communication manager set up successfully.")

    def quitApp(self, *args):
        # shuts down the application
        comManager._disconnect()
        Gtk.main_quit()

    def getMove(self, *args):
        global position
        global game_type
        global eat_move
        global gargabe_pos
        global garbage
        global number_of_beaten_pieces
        global current_garbage

        turn_ended = False

        while(turn_ended == False and not rules.black_win(position) and not rules.white_win(position)):
            if current_player == 2 and game_type == "ai":  # player is AI
                movestring = rules.make_move(position)
                current_move = [["1" + movestring[0] + movestring[1]], ["2" + movestring[0] + movestring[1]],
                                ["1" + movestring[3] + movestring[4]], ["3" + movestring[3] + movestring[4]]]

            else:
                foundPoint, img = camera.detectGesture(position, board_fields)
                camera.draw_positions(
                    position, board_fields, img)

                # x = "0"
                # print("enter piece position: ")
                # x = raw_input()
                # foundPoint = board_fields[x]
                # print(str(board_fields))
                dist_min = 10000.0
                closest_point = ()
                closest_point_2 = ()
                eat_move = "00"

                for points in board_fields:
                    print("checking " + str(points) +
                          ": " + str(board_fields[points]))
                    # loop over all points and find closest
                    # print(str(camera.getDistance(
                    #    board_fields[points][0], board_fields[points][1], foundPoint[0], foundPoint[1])))

                    if (camera.getDistance(board_fields[points][0], board_fields[points][1], foundPoint[0], foundPoint[1]) < dist_min):
                        closest_point = (points, board_fields[points])
                        print("found lower distance: " + str(closest_point) + " with distance: " + str(
                            camera.getDistance(board_fields[points][0], board_fields[points][1], foundPoint[0], foundPoint[1])))

                        dist_min = camera.getDistance(
                            board_fields[points][0], board_fields[points][1], foundPoint[0], foundPoint[1])
                print("Found field is: " + str(closest_point) + " for piece.")
                print("Please point to the target now...")
                time.sleep(3)
                # raw_input()
                current_piece = closest_point
                movestring = str(current_piece[0]) + " => ..."
                # lbl_moves.set_text(movestring)
                print("Getting target.")
                dist_min = 100000

                # x = "0"
                # print("enter target position: ")
                # x = raw_input()
                # foundPoint = board_fields[x]
                foundPoint, _ = camera.detectGesture(position, board_fields)
                for points in board_fields:
                    # print(str(board_fields[points]))
                    # loop over all points and find closest
                    # print(str(camera.getDistance(
                    #     board_fields[points][0], board_fields[points][1], foundPoint[0], foundPoint[1])))
                    if (camera.getDistance(board_fields[points][0], board_fields[points][1], foundPoint[0], foundPoint[1]) < dist_min):
                        closest_point_2 = (points, board_fields[points])
                        # print("found lower distance: " + str(closest_point) + " with distance: " + str(
                        #    camera.getDistance(board_fields[points][0], board_fields[points][1], foundPoint[0], foundPoint[1])))

                        dist_min = camera.getDistance(
                            board_fields[points][0], board_fields[points][1], foundPoint[0], foundPoint[1])
                current_target = closest_point_2
                print("Found field is: " + str(current_target) + " for target.")

                current_move = [["1" + str(current_piece[0])], ["2" + str(current_piece[0])],
                                ["1" + str(current_target[0])], ["3" + str(current_target[0])]]
                print("Current move is: " + str(current_move))
                # move_str = str(current_move[0]) + str(current_target[0])
                # validation_move = str(current_piece + current_target)
                movestring = str(current_piece[0]) + \
                    " " + str(current_target[0])
                # print(str(position))
                # lbl_moves.set_text(movestring)
                print("\n *** TEST *** \n")
                if (rules.Valid_move(position, movestring) == False) or (rules.verif_collor(position, movestring, "white") == False):
                    print(
                        "Move is invalid, please try again! Starting new detection...")
                    # raw_input()
                    time.sleep(5)
                    return
                print("Move is valid.")

            if (rules.food_pos(movestring) != "00"):
                print("Player has to beat a piece!")
                eat_move = rules.food_pos(movestring)

            print("Food position: " + str(rules.food_pos(movestring)))
            position = rules.new_position(position, movestring)
            print("New position: " + str(position))

            turn_ended = rules.turn_endet(position)
            print("Player endet turn: " +
                  str(rules.turn_endet(position)))
            self.performMove(current_move)
            print("Detection finished.")
            position = rules.new_position(position, movestring)
            if (eat_move != "00"):
                print("a piece was beaten, performing removal...")
                if (current_player == 1):
                    current_move = [["1" + eat_move], ["2" +
                                                       eat_move], ["1" + gargabe_pos[0] + garbage[current_garbage]], ["3" + gargabe_pos[0] + garbage[current_garbage]]]
                else:
                    current_move = [["1" + eat_move], ["2" +
                                                       eat_move], ["1" + gargabe_pos[1] + garbage[current_garbage]], ["3" + gargabe_pos[1] + garbage[current_garbage]]]

                # current_move = [["1" + eat_move], ["2" +
                #                                   eat_move], ["1" + letters[number_of_beaten_pieces] + garbage[current_garbage]], ["3" + letters[number_of_beaten_pieces] + garbage[current_garbage]]]
                # number_of_beaten_pieces += 1
                # if (letters[number_of_beaten_pieces] == 'F'):
                #    number_of_beaten_pieces = 0
                #    current_garbage += 1

                self.performMove(current_move)

            eat_move = "00"
        rules.print_position(position)
        self.changePlayer()

    def newGameHuman(self, *args):
        global game_type
        game_type = "human"
        global position
        global player_has_won
        # reset board
        # start game
        print("resetting board...")
        position = rules.restart_game()

        print("board successfully reset.")
        print("current turn: player 1")
        current_player = 1
        while (player_has_won == False):
            if (rules.white_win(position)):
                print("White has won!")
            player_has_won = rules.white_win(position)

            if (rules.black_win(position)):
                print("Black has won!")
            player_has_won = rules.black_win(position)
            if (player_has_won == False):
                self.getMove()
            else:
                print("The game has ended.")
        return

    def newGameAI(self, *args):
        global game_type
        game_type = "ai"
        # reset board
        # start game (human)
        print("resetting board...")
        global position
        global player_has_won
        # reset board
        # start game
        print("resetting board...")
        position = rules.restart_game()

        print("board successfully reset.")
        print("current turn: player 1")
        current_player = 1
        while (player_has_won == False):
            if (rules.white_win(position)):
                print("White has won!")
            player_has_won = rules.white_win(position)

            if (rules.black_win(position)):
                print("Black has won!")
            player_has_won = rules.black_win(position)
            if (player_has_won == False):
                self.getMove()
            else:
                print("The game has ended.")
        return

    def startCalibration(self, *args):
        global board_fields
        board_fields, img = camera.calibrate()

        # sorted(edges)
        # edges.sort(key=itemgetter(1))

        print("board: " + str(board_fields))

        cap_ = cv2.VideoCapture(-1)
        _ret_, frame_ = cap_.read()
        for key, value in board_fields.iteritems():
            cv2.circle(frame_, value, 3, (100, 100, 100))
            cv2.putText(frame_, key, value, cv2.FONT_HERSHEY_SIMPLEX,
                        1, (100, 100, 100))

        both = np.hstack((frame_, img))
        cv2.imshow('displayWindow', both)

        print("setup ready.")

    def performMove(move, test):
        print(str(test))
        print("performing move " + str(move))
        # test code
        move = test
        flat_list = [item for sublist in move for item in sublist]
        print(str(flat_list))
        # move = ["1A3", "2A3"]
        # b = rules.valid_move("A1", "C2 B2")
        # print(str(b))
        # end test code
        comManager.sendMove(flat_list)     # @ACTIVATE
        lbl_moves.set_text = ""

        # change player
    def changePlayer(self, *args):
        global position
        print("changing player: " + str(lbl_player))
        time.sleep(3)
        global current_player
        global lbl_player
        rules.print_position(position)
        if current_player == 1:
            current_player = 2
            lbl_player.set_text("Player 2")
        else:
            current_player = 1
            lbl_player.set_text("Player 1")


class game():
    moves = []

    # game process
    # 1 connect to robot
    # start game against ai or human
    # player 1 chooses first move:
    # select piece (A1) - select position (B1) - confirm move (performMove)
    # message: ["1A1" , "200", "1B1", "300", "500"]
    # game logic checks if pieces have to be removed
    # player changes to player 2
    # select piece - select position - [...] - confirm move


def getMoveToPoint():
    # finds the next move within this move chain
    print("getting move")
    moves.append("1" + camera.detectGesture(position, board_fields)[0])


builder = Gtk.Builder()

#
# Main Function
#


def main():
    global lbl_player
    global lbl_moves
    global position
    global current_move
    win = gui()
    builder.add_from_file("gui.glade")
    window = builder.get_object("win")
    label = builder.get_object("connectionState")
    # win.connect("destroy", Gtk.main_quit)
    builder.connect_signals(Handler())
    lbl_player = builder.get_object("lbl_player")
    lbl_moves = builder.get_object("lbl_moves")

    print(str(lbl_player))
    Gtk.main()


if __name__ == '__main__':
    main()
