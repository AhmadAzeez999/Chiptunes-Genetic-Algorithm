import random 
from pydub import AudioSegment
from pydub.playback import play

class Chromosome:
    # Initializing a chromosome with random notes, range C4 to B4
    def __init__(self, targetMelody, numOfNotes, noteRange=(60,72), bestGenes=None):
        self.noteRange = noteRange
        self.numOfNotes = numOfNotes
        self.targetMelody = targetMelody

        if bestGenes is not None:
            self.genes = bestGenes
        else:
            self.genes = self.initializeGenes()

        self.fitnessScore = 0 # 0 by default
        self.calculateFitness()

    def initializeGenes(self):
        return [random.randint(self.noteRange[0], self.noteRange[1]) for _ in range(self.numOfNotes)]
    
    def mutate(self, mutationRate=0.1):
        if random.random() < mutationRate:
            mutationPoint = random.randint(0, self.numOfNotes - 1)
            self.genes[mutationPoint] = random.randint(self.noteRange[0], self.noteRange[1])
            self.fitnessScore = self.calculateFitness()

    def crossover(self, mate):
        crossoverPoint = random.randint(1, self.numOfNotes - 1)
        childGenes = self.genes[:crossoverPoint] + mate.genes[crossoverPoint:]
        child = Chromosome(self.targetMelody, self.numOfNotes, self.noteRange)
        child.genes = childGenes
        
        return child
    
    def calculateFitness(self):
        # targetMelody will be an array of MIDI notes representing the target melody
        self.fitnessScore = sum(1 for i in range(self.numOfNotes) if self.genes[i] == self.targetMelody[i])

        return self.fitnessScore
    
    def __repr__(self):
        return f"Chromosome(fitness={self.fitnessScore}, genes={self.genes})"