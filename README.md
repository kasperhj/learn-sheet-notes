# What?
A simple application to assist in learning notes.
Once running, the program will display a staff (G-clef is not drawn though) and a random note.
Your objective is to press the corresponding key on your MIDI-keyboard.
Once successful, the frequency of the correct note will be played (through winsound; disable if you're on linux or mac) and a new random note will appear.

# How?
Connect a MIDI-keyboard to a computer running this application through Python.
I've tested the program on Windows 10 with an AKAI LPK25 and a Nektar LX61+.

# Implementation
This code was not designed but hacked together and glued around the edges.

# Todo
* Implement sharps and flats
* Add a G-clef to the staff
