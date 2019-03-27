#!/usr/bin/env python

import camera
import game as rules
from gi.repository import Gtk
import gi
import importlib
import socket
import sys
from operator import itemgetter
gi.require_version('Gtk', '3.0')

edges = []
board_fields = {}


class communicationManager():
    receivedMessage = ""    # response received from robot
    messageToSend = ""      # message to be sent
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

    def newGameHuman(self, *args):
        # reset board
        # start game
        print("resetting board...")
        print("board successfully reset.")
        print("current turn: player 1")
        foundPoint = camera.detectGesture()
        print(str(board_fields))
        # get move
        # perform move
        # update Board (determine winner, pieces to remove, damen)
        # change player -> jmp get move

    def newGameAI(self, *args):
        # reset board
        # start game (human)
        print("resetting board...")

    def startCalibration(self, *args):
        edges = camera.calibrate()

        # sorted(edges)
        # edges.sort(key=itemgetter(1))
        print("successfully calibrated.")
        print("board edges are: " +
              str(edges[0]) + ", " + str(edges[2]) + ", " + str(edges[4]) + ", " + str(edges[6]))
        print("calculating fields...")
        x_dist = (edges[0][0] - edges[2][0])/10
        print("x dist: " + str(x_dist))
        y_dist = (edges[0][1] - edges[4][1])/10
        print("y dist: " + str(y_dist))
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
        x_val = edges[2][0] + x_dist  # first x value
        y_val = edges[6][1] + y_dist  # first y value
        print("x val: " + str(x_val) + ", y val: " + str(y_val))
        field_edges = []
        for let in letters:
            # A, B, C, ...
            for num in numbers:
                # create fields
                # 1, 2, 3, ...
                tmp = str(let + num)
                board_fields[tmp] = [x_val, y_val]
                x_val = x_val + x_dist
            y_val += y_dist
            x_val = edges[2][0] + x_dist  # first x value

        print("board: " + str(board_fields))
        print("setup ready.")

    def performMove(self, *args):
        print("performing move...")

        # test code
        # move = ["1C1", "2C1", "1D2", "3D2"]
        b = rules.valid_move("A1", "C2 B2")
        print(str(b))
        # end test code
        # comManager.sendMove(move)


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
        moves.append("1" + camera.detectGesture())


builder = Gtk.Builder()

#
# Main Function
#


def main():
    win = gui()
    builder.add_from_file("gui.glade")
    window = builder.get_object("win")
    label = builder.get_object("connectionState")
    # win.connect("destroy", Gtk.main_quit)
    builder.connect_signals(Handler())
    Gtk.main()


if __name__ == '__main__':
    main()
