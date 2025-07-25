from mingus.containers import Note
from mingus.midi import fluidsynth

def create_music():
    note = Note("C", 4)
    fluidsynth.init()
    fluidsynth.play_Note(note)
    return "Musique créée."
