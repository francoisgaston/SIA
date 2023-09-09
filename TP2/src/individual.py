import math
from copy import deepcopy
from enum import Enum
import random


class ItemProp(Enum):
    STRENGTH = 0
    AGILITY = 1
    EXPERTISE = 2
    RESISTANCE = 3
    LIFE = 4
    HEIGHT = 5


class Individual:

    FITNESS_FUNCTION = None
    CROSSOVER_FUNCTION = None
    MAX_ITEM = 150.0
    MAX_PROPS = 6
    DELTA_PERCENTAGE = 0.2

    # Recibe el arreglo de propiedades
    # No deben sumar 150 o cumplir con las restricciones de altura
    # Las normaliza automáticamente antes de devolver
    def __init__(self, properties):
        self.properties = properties

    @staticmethod
    def generate_individual():
        propierties = Individual.__generate_items()
        propierties = Individual.__normalize(propierties)
        return Individual(propierties)

    @staticmethod
    def __generate_items():
        item_count = len(ItemProp) - 1
        propierties = [0] * item_count
        for i in range(item_count):
            propierties[i] = random.uniform(0, 150-1)
        propierties.append(random.uniform(1.3, 2.0))
        return propierties

    #habria que seleccionar un elemento del arreglo y modificarlo con un random
    #o por ahi setearlo random y re-normalizar
    def mutate_gen(self, index):
        if index == ItemProp.HEIGHT.value:
            self.properties[index] = random.uniform(1.3, 2.0)
        else:
            delta = self.properties[index] * Individual.DELTA_PERCENTAGE
            self.properties[index] = random.uniform(max(0, self.properties[index]-delta),min(150, self.properties[index]+delta))
        return

    '''
    def __generate_items():
        dirichlet_samples = np.random.dirichlet(np.ones(5), size=1)[0]
        return dirichlet_samples * 150
    '''

    @staticmethod
    def __normalize(vector):
        # Normalizes values for all properties except height
        total = sum(vector[:ItemProp.HEIGHT.value])
        for i in range(0, ItemProp.HEIGHT.value):
            vector[i] = (vector[i]/total) * Individual.MAX_ITEM
        return vector

    @staticmethod
    def crossover(individual_1, individual_2):
        # crossover of properties
        # ans1, ans2, man = Individual.CROSSOVER_FUNCTION(individual_1.properties, individual_2.properties, Individual.MAX_PROPS)
        ans1, ans2 = Individual.CROSSOVER_FUNCTION(individual_1.properties, individual_2.properties, Individual.MAX_PROPS)
        ans1 = Individual.__normalize(ans1)
        ans2 = Individual.__normalize(ans2)
        return Individual(ans1), Individual(ans2)

    def normalize(self):
        self.properties = Individual.__normalize(self.properties)

    @staticmethod
    def clone(individual):
        if isinstance(individual, Individual):
            return deepcopy(individual)
        raise Exception("obj is not an individual")

    def __hash__(self):
        return hash(tuple(self.properties))

    def __eq__(self, other):
        if isinstance(other, Individual):
            return self.properties == other.properties
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.fitness() < other.fitness()

    def height(self):
        return self.properties[ItemProp.HEIGHT.value]

    def fitness(self):
        return Individual.FITNESS_FUNCTION(self.attack(),self.defense())

    def attack(self):
        return (self.agility() + self.expertise()) * self.strength() * self.ATM()

    def defense(self):
        return (self.resistance() + self.expertise()) * self.life() * self.DEM()

    def strength(self):
        return 100*math.tanh(0.01 * self.properties[ItemProp.STRENGTH.value])

    def agility(self):
        return math.tanh(0.01 * self.properties[ItemProp.AGILITY.value])

    def expertise(self):
        return 0.6 * math.tanh(0.01 * self.properties[ItemProp.EXPERTISE.value])

    def resistance(self):
        return math.tanh(0.01 * self.properties[ItemProp.RESISTANCE.value])

    def life(self):
        return 100 * math.tanh(0.01 * self.properties[ItemProp.LIFE.value])

    def ATM(self):
        height = self.properties[ItemProp.HEIGHT.value]
        return 0.5 - math.pow((3*height)-5,4) + math.pow((3*height)-5,2) + height/2.0

    def DEM(self):
        height = self.properties[ItemProp.HEIGHT.value]
        return 2 + math.pow(3 * height - 5, 4) - math.pow(3 * height - 5, 2) - height/2.0

