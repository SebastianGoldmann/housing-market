import simulation_objects as SO
import Visualization_class as VS

population = SO.Population()
population.createMovers(numbOfMovers=5, percentageInEntry=0, intialWealth=100_000)
population.createStarters(numbOfStarters=5, intialWealth=600_000)
population.simulate(tradingYears=5)
print(f'The number of starters in no home : {population.starterToOtherHouse[0]}, entry home: {population.starterToOtherHouse[1]} and in luxury homes: {population.starterToOtherHouse[2]}')
print(f'The number of movers in no home : {population.moverToOtherHouse[0]}, entry home: {population.moverToOtherHouse[1]} and in luxury homes: {population.moverToOtherHouse[2]}')

# Visualiziation = VS.visualizeHousingMarket(population)
# Visualiziation.plotPrices()
# Visualiziation.boxPlotPrices(luxury=True)
# Visualiziation.boxPlotPrices(luxury=False)
# Visualiziation.numbOfDailyTrades()