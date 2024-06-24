import random
from deap import base, creator, tools, algorithms
import django
from django.conf import settings
from main.models import Schedule, TimeSlot, Module, Teacher, Classroom

django.setup()

# Define constants
POPULATION_SIZE = 50
GENERATIONS = 100
CXPB, MUTPB = 0.5, 0.2

# Setup DEAP genetic algorithm
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()


# Attribute generator
def generate_timeslot():
    return random.choice(TimeSlot.objects.all())


# Structure initializers
toolbox.register("attr_timeslot", generate_timeslot)
toolbox.register(
    "individual",
    tools.initRepeat,
    creator.Individual,
    toolbox.attr_timeslot,
    n=Schedule.objects.count(),
)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evaluate(individual):
    # Fitness function to evaluate the schedule
    fitness = 0
    schedule = Schedule()

    for idx, timeslot in enumerate(individual):
        module = Module.objects.all()[idx % Module.objects.count()]
        teacher = module.user.teacher
        classroom = Classroom.objects.filter(type=timeslot.type).first()

        if not schedule.timeslots.filter(
            module=module, teacher=teacher, classroom=classroom, time=timeslot.time
        ).exists():
            schedule.timeslots.add(timeslot)
            fitness += 1
        else:
            fitness -= 1

    return (fitness,)


def crossover(ind1, ind2):
    tools.cxTwoPoint(ind1, ind2)
    return ind1, ind2


def mutate(individual):
    if random.random() < MUTPB:
        index = random.randint(0, len(individual) - 1)
        individual[index] = generate_timeslot()
    return (individual,)


toolbox.register("evaluate", evaluate)
toolbox.register("mate", crossover)
toolbox.register("mutate", mutate)
toolbox.register("select", tools.selTournament, tournsize=3)


def main():
    pop = toolbox.population(n=POPULATION_SIZE)
    hof = tools.HallOfFame(1)

    # Algorithms.eaSimple is a simple genetic algorithm.
    algorithms.eaSimple(
        pop,
        toolbox,
        cxpb=CXPB,
        mutpb=MUTPB,
        ngen=GENERATIONS,
        stats=None,
        halloffame=hof,
        verbose=True,
    )

    return hof


if __name__ == "__main__":
    best_individuals = main()
    best_schedule = best_individuals[0]
    print("Best Schedule:", best_schedule)
