import simulation_objects as SO
import Visualization_class as VS

population = SO.Population()
population.createMovers(numbOfMovers=10000, percentageInEntry=0.8, intialWealth=100_000)
population.createStarters(numbOfStarters=2000, intialWealth=600_000)
population.simulate(tradingYears=100)

Visualiziation = VS.visualizeHousingMarket(population)
Visualiziation.plotPrices()
#Visualiziation.boxPlotPrices(luxury=True)
#Visualiziation.boxPlotPrices(luxury=False)
Visualiziation.numbOfDailyTrades()