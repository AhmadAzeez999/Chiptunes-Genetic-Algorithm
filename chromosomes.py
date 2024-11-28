import random

class Chromosome:
    def __init__(self, targetMelody, numOfRows, noteRange=(60, 72), timeRange=(0.5, 1.5), bestGenes=None):
        self.noteRange = noteRange
        self.timeRange = timeRange
        self.numOfRows = numOfRows
        self.targetMelody = targetMelody
        
        # Initialize genes with random values if no bestGenes are provided
        if bestGenes is not None:
            self.genes = bestGenes
        else:
            self.genes = self.initializeGenes()

        self.fitnessScore = 0
        self.calculateFitness()

    def initializeGenes(self):
        # Generate random pairs of [note, time] within the specified ranges - it is a flatened 1d array ie pairs
        return [
            [random.randint(self.noteRange[0], self.noteRange[1]), round(self.targetMelody[i][1], 1)]
            for i in range(self.numOfRows)
        ]
    
    def mutate(self, mutationRate=0.1):
        if random.random() < mutationRate:
            randomIndex = random.randint(0, self.numOfRows - 1)
            self.genes[randomIndex] = [
                random.randint(self.noteRange[0], self.noteRange[1]),
                round(self.targetMelody[randomIndex][1], 1) 
            ]
            self.fitnessScore = self.calculateFitness()

    def crossover(self, mate):
        crossoverPoint = random.randint(1, self.numOfRows - 1)
        
        childGenes = self.genes[:crossoverPoint] + mate.genes[crossoverPoint:]

        child = Chromosome(self.targetMelody, self.numOfRows, self.noteRange, self.timeRange)
        child.genes = childGenes
        
        return child
    
    def calculateFitness(self):
        #Calculate the fitness based on matching both note and time..
        self.fitnessScore = sum(
            1 for i in range(self.numOfRows)
            if (self.genes[i][0] == self.targetMelody[i][0]) and (self.genes[i][1] == self.targetMelody[i][1])
        )
        return self.fitnessScore

    def __repr__(self):
        #Formatting the genes to only one decimal place for the time
        formatted_genes = [
            [note, round(time, 1)] for note, time in self.genes
        ]
        return f"Chromosome(fitness={self.fitnessScore}, genes={formatted_genes})"



