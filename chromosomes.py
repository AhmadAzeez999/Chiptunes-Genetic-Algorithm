import random

class Chromosome:
    # Initializing a chromosome with random notes, range C4 to B4
    def __init__(self, targetMelody, numOfRows, numOfCols, noteRange=(60,72), bestGenes=None):
        self.noteRange = noteRange
        self.numOfRows = numOfRows # Number of rows in the 2D array
        self.numOfCols = numOfCols # Number of columns
        self.targetMelody = targetMelody

        if bestGenes is not None:
            self.genes = bestGenes
        else:
            self.genes = self.initializeGenes()

        self.fitnessScore = 0 # 0 by default
        self.calculateFitness()

    def initializeGenes(self):
        return [random.randint(self.noteRange[0], self.noteRange[1]) for _ in range(self.numOfCols)
                for _ in range(self.numOfRows)]
    
    def mutate(self, mutationRate=0.1):
        if random.random() < mutationRate:
            randomRow = random.randint(0, self.numOfRows - 1)
            randomCol = random.randint(0, self.numOfCols - 1)
            self.genes[randomRow][randomCol] = random.randint(self.noteRange[0], self.noteRange[1])
            self.fitnessScore = self.calculateFitness()

    def crossover(self, mate):
        crossoverRow = random.randint(1, self.numOfNotes - 1)
        crossoverCol = random.randint(1, self.numOfCols - 1)
        
        childGenes = [
            self.genes[row][:crossoverCol] + mate.genes[row][crossoverCol:]

            if row == crossoverRow else self.genes[row]
            for row in range(self.numOfRows)
        ]

        child = Chromosome(self.targetMelody, self.numOfRows, self.numOfCols, self.noteRange)
        child.genes = childGenes
        
        return child
    
    def calculateFitness(self):
        # targetMelody will be an array of MIDI notes representing the target melody
        self.fitnessScore = sum(
            1 for i in range(self.numOfRows)
            for j in range(self.numOfCols)
            if self.genes[i][j] == self.targetMelody[i][j]
        )

        return self.fitnessScore
    
    def __repr__(self):
        return f"Chromosome(fitness={self.fitnessScore}, genes={self.genes})"