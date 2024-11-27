from mido import MidiFile
from pydub import AudioSegment
from pydub.generators import Square
from typing import List, Tuple
import numpy as np

def midiToFreq(midiNumber: int) -> float:
    # Formula for converting MIDI to frequency
    return 440 * (2 ** ((midiNumber - 69) / 12))

def readMidiNotes(midiFilePath: str) -> List[Tuple[int, float]]:
    midiFile = MidiFile(midiFilePath)
    notes = []
    currentTime = 0.0

    # Looping through each message in the midi file
    # A message is basically an event (or a note) in a midi file
    for message in midiFile:
        currentTime += message.time
        
        # 'note_on' indicates when a note/event starts
        if message.type == 'note_on' and message.velocity > 0:
            notes.append((message.note, currentTime))

    return notes

def createWavFromNotes(notes: List[Tuple[int, float]], outputPath: str, noteDuration: float = 0.5):
    if not notes:
        raise ValueError("Whoa! No notes provided.")
    
    # Creating an empty audio segment
    maxTime = max(time for _, time in notes) + noteDuration
    baseAudio = AudioSegment.silent(duration=int(maxTime * 1000)) # pydub uses milliseconds

    # Generating and adding each note
    for noteNum, noteTime in notes:
        frequency = midiToFreq(noteNum)

        # Generating a square wave for this note
        squareWave = Square(frequency)
        noteSegment = squareWave.to_audio_segment(
            duration=int(noteDuration * 1000),
            volume = -20.0 # To reduce the volume (decibels)
        )

        # Applying fade in and out to prevent clicks
        noteSegment = noteSegment.fade_in(50).fade_out(50) # 50ms

        # Right position at the correct time
        position = int(noteTime * 1000) # Converting to milliseconds
        baseAudio = baseAudio.overlay(noteSegment, position=position)

    # Exporting the final audio
    baseAudio.export(outputPath, format="wav")

def main():
    try:
        # Reading the MIDI file
        midiFilePath = "MIDIs\MK For Proj.mid"
        notes = readMidiNotes(midiFilePath)

        print("Notes found!")

        # Creating the WAV file
        outputPath = 'output.wav'
        createWavFromNotes(notes, outputPath)
        print(f"\nWAV file created successfully: {outputPath}")
    
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()