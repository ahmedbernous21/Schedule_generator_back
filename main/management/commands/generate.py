import random
import numpy as np
from deap import base, creator, tools, algorithms
from django.core.management.base import BaseCommand
from main.models import (
    Teacher,
    Module,
    Group,
    Classroom,
    TimeSlot,
    Schedule,
    Planning,
)

DAYS = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
TIMES = [
    "8h:00-9h:30",
    "9h:30-11h:00",
    "11h:00-12h:30",
    "12h:30-14h:00",
    "14h:00-15h:30",
    "15h:30-17h:00",
]
CLASSROOM_TYPES = {
    "cours_hours": "AMPHI",
    "td_hours": "TD",
    "tp_hours": "TP",
}


# Fitness function
def evaluate(individual):
    conflicts = 0
    for schedule in individual:
        # Check for conflicts
        pass  # You need to implement your conflict checking logic here
    return (conflicts,)


# Initialization function
def init_individual():
    individual = []
    # Create schedule for each group and each module
    groups = Group.objects.all()
    modules = Module.objects.all()
    classrooms = list(Classroom.objects.all())
    random.shuffle(classrooms)

    for group in groups:
        for module in modules:
            for session_type, hours in [
                ("cours_hours", module.cours_hours),
                ("td_hours", module.td_hours),
                ("tp_hours", module.tp_hours),
            ]:
                if hours <= 0:
                    continue
                suitable_classrooms = [
                    c for c in classrooms if c.type == CLASSROOM_TYPES[session_type]
                ]
                if not suitable_classrooms:
                    continue

                for _ in range(int(hours / 1.5)):
                    day = random.choice(DAYS)
                    time = random.choice(TIMES)
                    classroom = random.choice(suitable_classrooms)
                    individual.append(
                        {
                            "group": group,
                            "module": module,
                            "day": day,
                            "time": time,
                            "classroom": classroom,
                            "type": session_type,
                        }
                    )
    return individual


# Crossover function
# Crossover function
def cx_individual(ind1, ind2):
    size = min(len(ind1), len(ind2))
    for i in range(size):
        if random.random() < 0.5:
            ind1[i], ind2[i] = ind2[i], ind1[i]
    return ind1, ind2


# Mutation function
def mut_individual(individual):
    if len(individual) > 0:
        i = random.randint(0, len(individual) - 1)
        individual[i]["day"] = random.choice(DAYS)
        individual[i]["time"] = random.choice(TIMES)
        individual[i]["classroom"] = random.choice(list(Classroom.objects.all()))
    return (individual,)


class Command(BaseCommand):
    help = "Generate an optimized schedule using genetic algorithm"

    def handle(self, *args, **kwargs):
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        toolbox = base.Toolbox()
        toolbox.register(
            "individual", tools.initIterate, creator.Individual, init_individual
        )
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", evaluate)
        toolbox.register("mate", cx_individual)
        toolbox.register("mutate", mut_individual)
        toolbox.register("select", tools.selTournament, tournsize=3)

        population = toolbox.population(n=100)
        ngen = 50
        cxpb = 0.5
        mutpb = 0.2

        algorithms.eaSimple(population, toolbox, cxpb, mutpb, ngen, verbose=True)

        best_ind = tools.selBest(population, 1)[0]

        # Save the best schedule to the database
        planning = Planning.objects.create(speciality="Example Speciality")
        for entry in best_ind:
            group = entry["group"]
            module = entry["module"]
            day = entry["day"]
            time = entry["time"]
            classroom = entry["classroom"]
            timeslot_type = entry["type"]

            timeslot = TimeSlot.objects.create(
                day=day,
                time=time,
                type=timeslot_type.upper(),
                module=module,
                classroom=classroom,
            )

            schedule, created = Schedule.objects.get_or_create(
                group=group,
            )
            schedule.addTimeSlot(timeslot)

        planning.save()
        self.stdout.write(self.style.SUCCESS("Successfully generated schedule"))
