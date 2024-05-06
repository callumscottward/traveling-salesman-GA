import math
import geopy.distance

def findCityPairDistanceDegrees(city1, city2):
    city1Coord = city1[1]
    city2Coord = city2[1]

    return math.sqrt(((city1Coord[0] - city2Coord[0]) ** 2) +
                     ((city1Coord[1] - city2Coord[1]) ** 2))

def findCityPairDistanceMiles(city1, city2):
    city1Coord = city1[1]
    city2Coord = city2[1]
    
    return geopy.distance.geodesic(city1Coord, city2Coord).miles

def findRouteDistanceDegrees(route):
    distance = 0

    for i in range(len(route) - 1):
        distance += findCityPairDistanceDegrees(route[i], route[i+1])
    distance += findCityPairDistanceDegrees(route[-1], route[0])

    return distance

def findRouteDistanceMiles(route):
    distance = 0

    for i in range(len(route) - 1):
        distance += findCityPairDistanceMiles(route[i], route[i+1])
    distance += findCityPairDistanceMiles(route[-1], route[0])

    return distance
