import random
from chromosomes import Chromosome

population = 1000
noteRange = (26, 127)

class GeneticAlgorithm:
    def __init__(self, targetSequence, populationSize=population):
        self.populationSize = populationSize
        self.targetSequence = targetSequence
        self.numOfRows = len(targetSequence)

        #Create an initial random population of Chromosomes
        self.population = [Chromosome(self.targetSequence, self.numOfRows, noteRange) for _ in range(self.populationSize)]

    def tournament(self):
        #Select the two best chromosomes based on fitness
        sortedPopulation = sorted(self.population, key=lambda x: x.fitnessScore, reverse=True)
        return sortedPopulation[:2]

    def evolve(self):
        generation = 0

        while generation <= 1000:  #Run for 1000, change later to maybe true
            print(f"\nGeneration {generation + 1}")

            #Sort population by fitness (best at the top)
            self.population.sort(key=lambda x: x.fitnessScore, reverse=True)

            #Check if the best chromosome matches the target sequence (perfect match)
            bestChromosome = self.population[0]
            print("Best fitness score in generation:", bestChromosome.fitnessScore)
            if bestChromosome.fitnessScore == self.numOfRows:
                print("Perfect match found!")
                print("Best Sequence:", bestChromosome.genes)
                break

            nextGeneration = [bestChromosome]

            #Create the rest of the next generation
            while len(nextGeneration) < self.populationSize:
                #Select parents using tournament selection
                parent1, parent2 = self.tournament()

                #Crossover to create children
                child1 = parent1.crossover(parent2)
                child2 = parent2.crossover(parent1)

                #Mutate the children
                child1.mutate()
                child2.mutate()

                #Add children to the next generation
                nextGeneration.append(child1)
                if len(nextGeneration) < self.populationSize:
                    nextGeneration.append(child2)

            #Replace old population with the new generation
            self.population = nextGeneration
            generation += 1

        return bestChromosome



     

target_sequence = [
    [69, 0.9], [71, 0.7], [69, 0.5], [72, 1.0], [74, 0.8],
    [76, 0.6], [77, 1.1], [79, 0.4], [81, 0.9], [83, 0.7]
]

ga = GeneticAlgorithm(targetSequence=target_sequence, populationSize=100)
best_chromosome = ga.evolve()
print(best_chromosome)
