import folium
from colour import Color
from routeMath import *

def getGenerationsParam():
    while True:
        try:
            generations = int(input(('Please enter the amount of route set generations you would like to generate\n' +
                                     '(the larger the number, the greater the probable best route efficiency): ')))
            
            if generations < 1 or generations > 1000:
                raise ValueError
            
            break
        except:
            print("ERROR: Number must be an integer in the range of (1-1000).\n")
    
    print()
    return generations

def getPopulationSizeParam():
    while True:
        try:
            populationSize = int(input(("Please enter the amount of routes to generate in each generation's population\n" +
                                        '(the larger the number, the quicker evolution will progress thanks to better odds): ')))
            
            if populationSize < 1 or populationSize > 1000:
                raise ValueError
            
            break
        except:
            print("ERROR: Number must be an integer in the range of (1-1000).\n")
    
    print()
    return populationSize

def cleanUpCsv(citiesCsvList):
    # Converts CSV list of dicts to singular dictionary of (city, state) tuple keys and (lat, lon) tuple values
    citiesDict = {}

    for city in citiesCsvList:
        citiesDict[(city['City'], city['State'])] = (float(city['lat']), float(city['lon']))

    return citiesDict

def printRoutePath(route):
    routeCities = [city[0] for city in route]

    print(f'{routeCities[0][0]}, {routeCities[0][1]}', end='')
    for city in routeCities[1:]:
        print(f' -> {city[0]}, {city[1]}', end='')
    
    print('\n')

def mapRoutePath(route, fileName):
    routeCoords = [city[1] for city in route]
    colors = generateRainbowGradient()

    map = folium.Map(location=[38.3283, -96.0795], zoom_start=5) # Approximate center of US

    for i in range(1, len(routeCoords)-1):
        folium.PolyLine([[routeCoords[i-1][0], routeCoords[i-1][1]],
                         [routeCoords[i][0], routeCoords[i][1]]],
                         color=colors[i-1], weight=2, opacity=1).add_to(map)
    
    folium.PolyLine([[routeCoords[-2][0], routeCoords[-2][1]],
                     [routeCoords[-1][0], routeCoords[-1][1]]],
                     color=colors[-2], weight=2, opacity=1).add_to(map)
    
    folium.PolyLine([[routeCoords[-1][0], routeCoords[-1][1]],
                     [routeCoords[0][0], routeCoords[0][1]]],
                     color=colors[-1], weight=2, opacity=1).add_to(map)
    
    map.save(fileName)

def generateRainbowGradient():
    colors = list(Color("red").range_to(Color("orange"), 167))
    colors.extend(list(Color("orange").range_to(Color("yellow"), 167)))
    colors.extend(list(Color("yellow").range_to(Color("green"), 166)))
    colors.extend(list(Color("green").range_to(Color("blue"), 167)))
    colors.extend(list(Color("blue").range_to(Color("purple"), 167)))
    colors.extend(list(Color("purple").range_to(Color("red"), 166)))
    
    colors = [color.hex for color in colors]
    
    return colors

def displayGaData(gaData):
    print(f"The algorithm is now complete. Choose one of the following options to view statistics on the data collected:")

    routeToDisplay = input('1. Best route in first generation\n' +
                           '2. Worst route in first generation\n' +
                           '3. Average route length in first generation\n' +
                           '4. Best route in last generation\n' +
                           '5. Worst route in last generation\n' +
                           '6. Average route length in last generation\n' +
                           '7. All-time fastest route\n' +
                           '8. All-time slowest route\n' +
                           '9. Quit\n' +
                           'Enter your choice in the form of a number: ')
    
    while routeToDisplay not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        routeToDisplay = input("ERROR: Number must be an integer in the range of (1-9): ")
    
    while routeToDisplay != '9':
        match routeToDisplay:
            case '1':
                print('Route path:')
                printRoutePath(gaData['First Generation Best'])
                print(f"Route distance: {findRouteDistanceMiles(gaData['First Generation Best'])} miles")

                saveMap = input('\nWould you like to save an interactive map of this route?\n' +
                                '1. Yes\n' +
                                '2. No\n' +
                                'Choose one: ')
                
                while saveMap not in ['1', '2']:
                    saveMap = input('ERROR: Enter 1 or 2: ')
                
                if saveMap == '1':
                    print('Saving...')
                    mapRoutePath(gaData['First Generation Best'], 'firstGenBest.html')
                    print('Saved. See firstGenBest.html for the map.')
            case '2':
                print('Route path:')
                printRoutePath(gaData['First Generation Worst'])
                print(f"Route distance: {findRouteDistanceMiles(gaData['First Generation Worst'])} miles")

                saveMap = input('\nWould you like to save an interactive map of this route?\n' +
                                '1. Yes\n' +
                                '2. No\n' +
                                'Choose one: ')
                
                while saveMap not in ['1', '2']:
                    saveMap = input('ERROR: Enter 1 or 2: ')
                
                if saveMap == '1':
                    print('Saving...')
                    mapRoutePath(gaData['First Generation Worst'], 'firstGenWorst.html')
                    print('Saved. See firstGenWorst.html for the map.')
            case '3':
                print(f"\nAverage route length: {gaData['First Generation Average']} miles")
            case '4':
                print('Route path:')
                printRoutePath(gaData['Last Generation Best'])
                print(f"Route distance: {findRouteDistanceMiles(gaData['Last Generation Best'])} miles")

                saveMap = input('\nWould you like to save an interactive map of this route?\n' +
                                '1. Yes\n' +
                                '2. No\n' +
                                'Choose one: ')
                
                while saveMap not in ['1', '2']:
                    saveMap = input('ERROR: Enter 1 or 2: ')
                
                if saveMap == '1':
                    print('Saving...')
                    mapRoutePath(gaData['Last Generation Best'], 'lastGenBest.html')
                    print('Saved. See lastGenBest.html for the map.')
            case '5':
                print('Route path:')
                printRoutePath(gaData['Last Generation Worst'])
                print(f"Route distance: {findRouteDistanceMiles(gaData['Last Generation Worst'])} miles")

                saveMap = input('\nWould you like to save an interactive map of this route?\n' +
                                '1. Yes\n' +
                                '2. No\n' +
                                'Choose one: ')
                
                while saveMap not in ['1', '2']:
                    saveMap = input('ERROR: Enter 1 or 2: ')
                
                if saveMap == '1':
                    print('Saving...')
                    mapRoutePath(gaData['Last Generation Worst'], 'lastGenWorst.html')
                    print('Saved. See lastGenWorst.html for the map.')
            case '6':
                print(f"\nAverage route length: {gaData['Last Generation Average']} miles")
            case '7':
                print(f"Fastest route path (occuring in generation {gaData['All-Time Best Generation']}):")
                printRoutePath(gaData['All-Time Best'])
                print(f"Route distance: {findRouteDistanceMiles(gaData['All-Time Best'])} miles")

                saveMap = input('\nWould you like to save an interactive map of this route?\n' +
                                '1. Yes\n' +
                                '2. No\n' +
                                'Choose one: ')
                
                while saveMap not in ['1', '2']:
                    saveMap = input('ERROR: Enter 1 or 2: ')
                
                if saveMap == '1':
                    print('Saving...')
                    mapRoutePath(gaData['All-Time Best'], 'allTimeBest.html')
                    print('Saved. See allTimeBest.html for the map.')
            case '8':
                print(f"Slowest route path (occuring in generation {gaData['All-Time Worst Generation']}):")
                printRoutePath(gaData['All-Time Worst'])
                print(f"Route distance: {findRouteDistanceMiles(gaData['All-Time Worst'])} miles")

                saveMap = input('\nWould you like to save an interactive map of this route?\n' +
                                '1. Yes\n' +
                                '2. No\n' +
                                'Choose one: ')
                
                while saveMap not in ['1', '2']:
                    saveMap = input('ERROR: Enter 1 or 2: ')
                
                if saveMap == '1':
                    print('Saving...')
                    mapRoutePath(gaData['All-Time Worst'], 'allTimeWorst.html')
                    print('Saved. See allTimeWorst.html for the map.')
            case _:
                print('ERROR: Number must be an integer in the range of (1-9).')
        
        returnToMenu = input('\nNow, would you like to return to the menu options or quit?\n' +
                             '1. Return to menu\n' +
                             '2. Quit\n' +
                             'Choose one: ')
        
        while returnToMenu not in ['1', '2']:
            returnToMenu = input('ERROR: Enter 1 or 2: ')
        
        if returnToMenu == '1':
            routeToDisplay = input('\n1. Best route in first generation\n' +
                                   '2. Worst route in first generation\n' +
                                   '3. Average route length in first generation\n' +
                                   '4. Best route in last generation\n' +
                                   '5. Worst route in last generation\n' +
                                   '6. Average route length in last generation\n' +
                                   '7. All-time fastest route\n' +
                                   '8. All-time slowest route\n' +
                                   '9. Quit\n' +
                                   'Enter your choice in the form of a number: ')
        else:
            while routeToDisplay not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                routeToDisplay = input("ERROR: Number must be an integer in the range of (1-9): ")

            routeToDisplay = '9'
