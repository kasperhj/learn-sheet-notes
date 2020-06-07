
from tkinter import Tk, Canvas, Frame, BOTH
import mypy
import random
import itertools
from winsound import Beep

class StaffGeometry():
    def __init__(self):
        self.x_offset = 10
        self.y_offset = 100
        self.length = 300
        self.spacing = 20
        self.c5_position = 3.0*self.spacing

class Note():
    def __str__(self):
        return self.__str

    def __repr__(self):
        return self.__str

    def __init__(self, note : str):
        self.is_sharp = "#" in note
        self.is_flat = "_" in note
        self.__str = note
        self.note = note[0]
        self.octave = int(note[-1])
        
        def f(x:str):
            return {
                'F': 1.5,
                'G': 2.0,
                'A': 2.5,
                'B': 3.0,
                'C': 0.0,
                'D': 0.5,
                'E': 1.0,
            }.get(x, 1)    # 1 is default if x not found

        note_dist = f(str.upper(self.note))
        octave_dist = 5 - self.octave
        self.dist_from_c5 = -(note_dist-(3.5*octave_dist))
        dist_from_staff_bottom = -(self.dist_from_c5-2.5)
        dist_from_staff_top = -(self.dist_from_c5+1.5)
        self.is_on_line = not float(self.dist_from_c5).is_integer()
        
        # If the note is below the bottom staff line, the ledger goes on the top of the note, otherwise the ledger goes on the bottom of the note.
        self.ledger_position = 'above' if dist_from_staff_bottom < 0 else 'below'

        note_is_outside_staff = abs(dist_from_staff_top)+abs(dist_from_staff_bottom) > 5
        
        if note_is_outside_staff:
            # Figure out how many ledgers we need
            a = min(dist_from_staff_bottom, dist_from_staff_top, key=abs)
            self.ledger_count = int(abs(a))
        else:
            self.ledger_count = 0

class Staff(Frame):

    def __init__(self, staff_geometry: StaffGeometry):
        super().__init__()
        self.__line_dist = 30
        self.__staff_geometry = staff_geometry
        self.__canvas = Canvas(self)
        self.initUI()

    def draw_staff(self):
        sg = self.__staff_geometry
        for i in range(1,6):
            self.__canvas.create_line(sg.x_offset, sg.y_offset+i*sg.spacing, sg.x_offset+sg.length, sg.y_offset+i*sg.spacing)

    def draw_note(self, note : Note):
        sg = self.__staff_geometry
        h = sg.spacing
        pos = sg.c5_position + (h*note.dist_from_c5)

        # Draw open note
        self.__canvas.create_oval(sg.x_offset, sg.y_offset+pos, sg.x_offset+h*1.4, sg.y_offset+pos-h)
        
       # Draw ledgers
        for i in range(note.ledger_count):
            if note.ledger_position == 'above':
                ledger = pos-h*i
                if note.is_on_line:
                    ledger = ledger+h/2
            else:
                ledger = pos+h*(i+1)
                if note.is_on_line:
                    ledger = ledger-h/2

            self.__canvas.create_line(sg.x_offset-6, sg.y_offset+ledger-h, sg.x_offset+h*1.4+6, sg.y_offset+ledger-h)

        if note.is_sharp:
            self.__canvas.create_line(sg.x_offset-h,     sg.y_offset+pos-h/2-4, sg.x_offset-h/2,   sg.y_offset+pos-h/2-4, width=2)
            self.__canvas.create_line(sg.x_offset-h,     sg.y_offset+pos-h/2+4, sg.x_offset-h/2,   sg.y_offset+pos-h/2+4, width=2)
            self.__canvas.create_line(sg.x_offset-h-4,   sg.y_offset+pos-h/2-8, sg.x_offset-h-4,   sg.y_offset+pos-h/2+8, width=2)
            self.__canvas.create_line(sg.x_offset-h/2,   sg.y_offset+pos-h/2-8, sg.x_offset-h/2,   sg.y_offset+pos-h/2+8, width=2)

        #sg.x_offset += h*2+5

    def initUI(self):
        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)
        # Move the display of a note to the middle of the staff
        self.__staff_geometry.x_offset += self.__staff_geometry.length /2 - self.__staff_geometry.spacing /2 
        self.__canvas.pack(fill=BOTH, expand=1)

    def draw_random_note(self):
        self.__canvas.delete("all")
        self.draw_staff()

        # Create some notes.
        product = itertools.product(['4','5'],['C','D','E','F','G','A','B'])
        notes = [n+o for (o,n) in product]

        random_note = Note(random.choice(notes))

        self.draw_note(random_note)

        return random_note

tk = Tk()
staff = Staff(StaffGeometry())
tk.geometry("600x450+300+300")



def play_note(frequency, duration):
    Beep(frequency, duration)

import random
import mido

notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

def note_from_midi_code (n: int) -> str:
    return notes[n % 12] + str(n//12)

def freq_from_midi_code (n:int) -> float:
    m = n - 8 # MIDI note numbers are 8 offset from piano key numbers (https://en.wikipedia.org/wiki/Piano_key_frequencies)
    a = 440
    twelfth_root_2 = 2 ** (1.0/12.0)
    f = twelfth_root_2 ** (n-49) * a
    return int(f)

note = staff.draw_random_note()
print("Get: " + str(note))

with mido.open_input() as inport:
    while True:
        tk.update_idletasks()
        tk.update()
        
        for msg in inport.iter_pending():
            if msg.type == 'note_on':
                print(note_from_midi_code(msg.note))
                if str(note) == note_from_midi_code(msg.note):
                    play_note(freq_from_midi_code(msg.note),500)
                    note = staff.draw_random_note()
                    print("Get: " + str(note))