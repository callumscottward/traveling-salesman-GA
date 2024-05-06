from ga import *
        
def main():
    print('Welcome to my Traveling Salesman route finder, utilizing the top 1000 cities of the US and genetic algorithms to evolve potential routes.\n')
    
    generations = getGenerationsParam()
    populationSize = getPopulationSizeParam()
    
    gaData = gaRouteFinder(generations, populationSize)
    displayGaData(gaData)

if __name__ == "__main__":
    main()
