import random

startPopulation = 50
infantMortality = 5
youthMortality = 45
agriculture = 5
disasterChance = 10
fertilityx = 18
fertilityy = 35
food = 0
peopleDictionary = []


class Person:
    def __init__(self, age):
        self.gender = random.randint(0, 1)
        self.age = age
        self.pregnant = 0


def harvest(food, agriculture):
    ablePeople = 0
    for person in peopleDictionary:
        if person.age > 8:
            ablePeople += 1


    food += ablePeople * agriculture
    if food < len(peopleDictionary):
        del peopleDictionary[0:int(len(peopleDictionary) - food)]
        food = 0
    else:
        food -= len(peopleDictionary)


def reproduce(fertilityx, fertilityy, infantMortality):
    for person in peopleDictionary:
        if person.gender == 1:
            if person.age > fertilityx:
                if person.age < fertilityy:
                    if random.randint(0, 5) == 1:
                        if random.randint(0, 100) > infantMortality:
                            peopleDictionary.append(Person(0))


def beginSim():
    for x in range(startPopulation):
        peopleDictionary.append(Person(random.randint(18, 50)))


def runYear(food, agriculture, fertilityx, fertilityy, infantMortality, disasterChance):
    harvest(food, agriculture)
    for person in peopleDictionary:
        if person.age > 80:
            peopleDictionary.remove(person)
        else:
            person.age += 1

    reproduce(fertilityx, fertilityy, infantMortality)


    if random.randint(0, 100) < disasterChance:
        del peopleDictionary[0:int(random.uniform(0.05, 0.2) * len(peopleDictionary))]

    print(len(peopleDictionary))

    infantMortality *= 0.985

    return infantMortality

beginSim()
while len(peopleDictionary) < 100000 and len(peopleDictionary) > 1:
    infantMortality = runYear(food, agriculture, fertilityx, fertilityy, infantMortality, disasterChance)