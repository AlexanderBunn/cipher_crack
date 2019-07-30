import random, sys
from deap import base, creator, tools

class GeneticAlgorithm():
    def __init__(self, cipher):
        self.cipher = cipher
        self.evolutions = 100
        self.pop_size = 3000
        self.mutindpb = 0.8
        self.cxindpb = 0.8
        self.mutletterpb = 2/26
        self.cxletterpb = 2/26
        self.survpb = 1000/5000
        self.ciphertext = None
        self.fitness = None
        self.weights = None
        self.toolbox = base.Toolbox()

    def __load_tools(self):
        creator.create("FitnessMax", base.Fitness, weights=self.weights)
        creator.create("Individual", list, fitness=creator.FitnessMax)
        self.toolbox.register("indices", random.sample, list('abcdefghijklmnopqrstuvwxyz'), 26)
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.indices)
        # self.toolbox.register("mate", self.cipher.mate, indpb=self.cxletterpb)
        self.toolbox.register("select", tools.selBest)
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=self.mutletterpb)
        self.toolbox.register("evaluate", self.__get_fitness)

    def __get_key(self, ind):
        return ''.join(ind)

    def __get_decipher(self, ind):
        key = self.__get_key(ind)
        return self.cipher.decipher(key, self.ciphertext)


    def __get_fitness(self, inds):
        # input(inds)
        guesses = [self.__get_decipher(ind) for ind in inds]
        # input(guesses)
        return self.fitness(guesses)

    def set_fitness(self, fitness, weights):
        self.weights = weights
        self.fitness = fitness
        self.__load_tools()

    def set_ciphertext(self, ciphertext):
        self.ciphertext = ciphertext

    def crack(self):
        sys.stdout.write('\n')
        sys.stdout.flush()
        pop = []
        for i in range(self.pop_size):
            ind = self.toolbox.individual()
            pop.append(ind)
        fit = self.toolbox.evaluate(pop)
        for i in range(self.pop_size):
            pop[i].fitness.values = [fit[0][i][0]]

        # Modification of the algorithm shown here: 
        # https://deap.readthedocs.io/en/master/examples/ga_onemax.html
        
        champ_counter = 0
        old_champ = self.toolbox.select(pop, 1)[0]
        for g in range(self.evolutions):
            new_champ = self.toolbox.select(pop, 1)[0]
            if new_champ.fitness.values == old_champ.fitness.values:
                champ_counter += 1
                if champ_counter > 8:
                    break
            else:
                champ_counter = 0
                old_champ = new_champ
            # Select the next generation individuals
            for ind in pop:
                if not ind.fitness.values:
                    input("WTF")
            survival_count = int(self.pop_size * self.survpb)
            offspring = self.toolbox.select(pop, survival_count)
            # review = [i for i in offspring if self.toolbox.evaluate(i)[0] > 0.5]
            # for i in review:
            #     print(self.__decipher(i), self.toolbox.evaluate(i), i.fitness.values)
            for o in self.toolbox.select(offspring, 1):
                sys.stdout.write('\r')
                sys.stdout.flush()
                out_line = 'Cracking --> ' + self.__get_decipher(o) + ' | ' + str(round(o.fitness.values[0], 2))
                sys.stdout.write(out_line)
                sys.stdout.flush()

            # Clone the selected individuals
            next_gen = [self.toolbox.clone(offspring[i % survival_count]) for i in range(self.pop_size)]

            # # Apply crossover on the next_gen
            # for ind1, ind2 in zip(next_gen[::2], next_gen[1::2]):
            #     if random.random() < self.cxindpb:
            #         self.toolbox.mate(ind1, ind2)
            #         del ind1.fitness.values
            #         del ind2.fitness.values

            # Apply mutation on the next_gen
            for mutant in next_gen:
                if random.random() < self.mutindpb:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in next_gen if not ind.fitness.valid]
            fit = self.toolbox.evaluate(invalid_ind)
            for i in range(len(invalid_ind)):
                invalid_ind[i].fitness.values = [fit[0][i][0]]

            pop[:] = next_gen
        winner = self.toolbox.select(pop, 1)[0]
        print('')
        return self.__get_key(winner), self.__get_decipher(winner)
