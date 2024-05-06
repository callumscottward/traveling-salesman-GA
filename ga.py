import random
import csv
from routeMath import *
from inputOutput import *

def createInitialPopulation(citiesDict, populationSize):
    population = []

    for _ in range(populationSize):
        route = list(citiesDict.items())
        random.shuffle(route) # Shuffles route in place
        population.append(route)
    
    return population

def tournamentSelection(population):
    return min(random.sample(population, 3), key=findRouteDistanceDegrees)

def crossover(parentRoute1, parentRoute2):
    childRoute = [None] * len(parentRoute1)

    crossoverStart, crossoverEnd = sorted(random.sample(range(len(parentRoute1)), 2))
    childRoute[crossoverStart:crossoverEnd] = parentRoute1[crossoverStart:crossoverEnd]

    j = 0 # j will index through parentRoute2 to find cities not in childRoute; i will index through childRoute
    for i in range(len(parentRoute2)):
        if i < crossoverStart or i >= crossoverEnd:
            while parentRoute2[j] in childRoute:
                j += 1
            childRoute[i] = parentRoute2[j]

    return childRoute

def mutate(route):
    cityIndex1, cityIndex2 = random.sample(range(len(route)), 2)
    route[cityIndex1], route[cityIndex2] = route[cityIndex2], route[cityIndex1]

    return route

def gaRouteFinder(generations, populationSize):
    print('Running algorithm (this may take a while)...')
    
    with open('us-cities-top-1k.csv', mode='r') as file:
        topCitiesCsv = csv.DictReader(file)
        topCitiesCsvList = list(topCitiesCsv)
    
    topCitiesDict = cleanUpCsv(topCitiesCsvList)

    population = createInitialPopulation(topCitiesDict, populationSize)
    
    firstGeneration = population
    firstGenBest = min(firstGeneration, key=findRouteDistanceDegrees)
    firstGenWorst = max(firstGeneration, key=findRouteDistanceDegrees)
    firstGenTotalDistance = sum([findRouteDistanceMiles(route) for route in firstGeneration])
    firstGenAvg = firstGenTotalDistance / len(firstGeneration)

    allTimeBest = firstGenBest
    allTimeBestGeneration = 1
    allTimeWorst = firstGenWorst
    allTimeWorstGeneration = 1

    for generationNumber in range(2, generations+1):
        nextGeneration = []

        for _ in range(populationSize):
            parentRoute1 = tournamentSelection(population)
            parentRoute2 = tournamentSelection(population)

            childRoute = crossover(parentRoute1, parentRoute2)

            if random.random() < 0.1:
                childRoute = mutate(childRoute)
            
            nextGeneration.append(childRoute)
        
        population = nextGeneration

        if findRouteDistanceDegrees(min(population, key=findRouteDistanceDegrees)) < findRouteDistanceDegrees(allTimeBest):
            allTimeBest = min(population, key=findRouteDistanceDegrees)
            allTimeBestGeneration = generationNumber
        
        if findRouteDistanceDegrees(max(population, key=findRouteDistanceDegrees)) > findRouteDistanceDegrees(allTimeWorst):
            allTimeWorst = max(population, key=findRouteDistanceDegrees)
            allTimeWorstGeneration = generationNumber
    
    lastGeneration = population
    lastGenBest = min(lastGeneration, key=findRouteDistanceDegrees)
    lastGenWorst = max(lastGeneration, key=findRouteDistanceDegrees)
    lastGenTotalDistance = sum([findRouteDistanceMiles(route) for route in lastGeneration])
    lastGenAvg = lastGenTotalDistance / len(firstGeneration)
    
    return {'First Generation Best': firstGenBest,
            'First Generation Worst': firstGenWorst,
            'First Generation Average': firstGenAvg,
            'Last Generation Best': lastGenBest,
            'Last Generation Worst': lastGenWorst,
            'Last Generation Average': lastGenAvg,
            'All-Time Best': allTimeBest,
            'All-Time Best Generation': allTimeBestGeneration,
            'All-Time Worst': allTimeWorst,
            'All-Time Worst Generation': allTimeWorstGeneration}
