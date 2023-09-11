def warrior_fitness(attack, defense):
    return 0.6 * attack + 0.4 * defense


def archer_fitness(attack, defense):
    return 0.9 * attack + 0.1 * defense


def defender_fitness(attack, defense):
    return 0.1 * attack + 0.9 * defense


# TODO: check values in document
def infiltrate_fitness(attack, defense):
    return 0.8 * attack + 0.3 * defense


class Fitness:

    @staticmethod
    def from_string(string):
        match string.upper():
            case "WARRIOR":
                return warrior_fitness
            case "ARCHER":
                return archer_fitness
            case "DEFENDER":
                return defender_fitness
            case "INFILTRATE":
                return infiltrate_fitness
            case _:
                return warrior_fitness