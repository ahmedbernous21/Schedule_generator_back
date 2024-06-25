import random
from deap import base, creator, tools, algorithms
from main.models import Teacher, Module, Group, Classroom, TimeSlot, Schedule, Planning
from django.db import transaction

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


class ScheduleGenerator:
    def __init__(self, planning_id):
        self.planning_id = planning_id

    def generate_schedule(self):
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        toolbox = base.Toolbox()
        toolbox.register(
            "individual", tools.initIterate, creator.Individual, self.init_individual
        )
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", self.evaluate)
        toolbox.register("mate", self.cx_individual)
        toolbox.register("mutate", self.mut_individual)
        toolbox.register("select", tools.selTournament, tournsize=3)

        population = toolbox.population(n=100)
        ngen = 50
        cxpb = 0.5
        mutpb = 0.2

        algorithms.eaSimple(population, toolbox, cxpb, mutpb, ngen, verbose=True)

        best_ind = tools.selBest(population, 1)[0]

        planning = Planning.objects.get(pk=self.planning_id)

        with transaction.atomic():
            planning.schedules.clear()

            scheduled_timeslots = (
                set()
            )  # To track already scheduled (day, time, classroom) combinations

            for entry in best_ind:
                group = entry["group"]
                module = entry["module"]
                day = entry["day"]
                time = entry["time"]
                classroom = entry["classroom"]
                timeslot_type = entry["type"]

                # Check if a timeslot with the same (day, time, classroom) combination is already scheduled
                if self.is_timeslot_scheduled(
                    day, time, classroom, scheduled_timeslots
                ):
                    continue  # Skip adding this timeslot

                timeslot = TimeSlot.objects.create(
                    day=day,
                    time=time,
                    type=timeslot_type.upper(),
                    module=module,
                    classroom=classroom,
                )

                schedule, created = Schedule.objects.get_or_create(
                    group=group,
                    planning=planning,
                    user=group.planning.user,  # Assuming user is associated with the group's planning
                )
                schedule.addTimeSlot(timeslot)

                # Add this (day, time, classroom) combination to scheduled_timeslots
                scheduled_timeslots.add((day, time, classroom))

        return "Successfully generated schedule"

    def is_timeslot_scheduled(self, day, time, classroom, scheduled_timeslots):
        """
        Helper method to check if a timeslot with the same (day, time, classroom)
        combination is already scheduled.
        """
        return (day, time, classroom) in scheduled_timeslots

    def init_individual(self):
        individual = []
        planning = Planning.objects.get(pk=self.planning_id)
        groups = planning.groups.all()
        modules = planning.modules.all()
        classrooms = list(planning.classrooms.all())

        random.shuffle(classrooms)

        for module in modules:
            module_hours = {
                "COURS": module.cours_hours,
                "TD": module.td_hours,
                "TP": module.tp_hours,
            }

            for session_type, hours in module_hours.items():
                if hours > 0:
                    suitable_classrooms = [
                        c
                        for c in classrooms
                        if c.type == CLASSROOM_TYPES[f"{session_type.lower()}_hours"]
                    ]

                    if not suitable_classrooms:
                        continue

                    num_sessions = int(hours / 1.5)
                    sessions = []

                    for _ in range(num_sessions):
                        day = random.choice(DAYS)
                        time = random.choice(TIMES)
                        classroom = random.choice(suitable_classrooms)
                        sessions.append((day, time, classroom, session_type))

                    for group in groups:
                        for session in sessions:
                            day, time, classroom, session_type = session
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

    def evaluate(self, individual):
        conflicts = 0
        scheduled_timeslots = set()  # To track (day, time, classroom) combinations
        group_schedules = {}  # To track each group's schedule
        cours_schedules = {}  # To track cours schedules for each module

        for schedule in individual:
            group = schedule["group"]
            module = schedule["module"]
            day = schedule["day"]
            time = schedule["time"]
            classroom = schedule["classroom"]
            session_type = schedule["type"]

            # Check if this (day, time, classroom) combination has already been scheduled
            if self.is_timeslot_scheduled(day, time, classroom, scheduled_timeslots):
                if (
                    session_type != "COURS"
                    or (module, day, time, classroom) not in cours_schedules
                ):
                    conflicts += 1
            else:
                scheduled_timeslots.add((day, time, classroom))

            # Check for conflicts within the same group's schedule
            if group not in group_schedules:
                group_schedules[group] = set()

            if (day, time) in group_schedules[group]:
                if (
                    session_type != "COURS"
                    or (module, day, time) not in cours_schedules
                ):
                    conflicts += 1
            else:
                group_schedules[group].add((day, time))

            # Track cours schedules
            if session_type == "COURS":
                cours_schedules[(module, day, time, classroom)] = True

            if time not in TIMES[:3]:  # Adjust to prioritize earlier timeslots
                conflicts += 1

        return (conflicts,)

    def cx_individual(self, ind1, ind2):
        size = min(len(ind1), len(ind2))
        for i in range(size):
            if random.random() < 0.5:
                ind1[i], ind2[i] = ind2[i], ind1[i]
        return ind1, ind2

    def mut_individual(self, individual):
        if len(individual) > 0:
            i = random.randint(0, len(individual) - 1)
            individual[i]["day"] = random.choice(DAYS)
            individual[i]["time"] = random.choice(TIMES)
            individual[i]["classroom"] = random.choice(list(Classroom.objects.all()))
        return (individual,)
