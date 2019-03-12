#!/usr/bin/env python

import camera
from gi.repository import Gtk
import gi
import importlib
import socket
import sys
gi.require_version('Gtk', '3.0')


class communicationManager():
    receivedMessage = ""    # response received from robot
    messageToSend = ""      # message to be sent
    move = []               # complete move message list
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

    def sendMove(self):
        for msg in self.move:
            # loop over all messages and send them
            # wait for response before sending another
            sock.sendall(msg)
            print("send data" + msg)
            receivedMessage = sock.recv()
            if (receivedMessage == "ok"):
                continue
            else:
                print("Robot reported an error: " + receivedMessage)
                break

        move = []


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
        # detectGesture()
        print("Hello. Press any key to start calibration.")
        input()
        machine = state_machine()
        while(1):
            try:
                command = input()
            except SyntaxError:
                print("Unknown input.")
                continue
            except NameError:
                print("Name Error, please try again.")
                continue
            machine.on_event(str(command))
            print("Current state: " + machine.state.__class__.__name__)

    def newGameAI(self, *args):
        print("not implemented")

    def startCalibration(self, *args):
        camera.calibrate()

    def confirm(self, *args):
        print("not implemented")

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
