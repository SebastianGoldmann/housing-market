import matplotlib.pyplot as plt
import numpy as np

class visualizeHousingMarket():
    def __init__(self, simulation):
        self.simulation = simulation

    def get_average(self, prices):
        if len(prices) == 0:
            return None
        return sum(prices)/len(prices)

    def plotPrices(self):
        # Get the average housing price for each Day
        averageLuxuryPrices = [self.get_average(dailyHousePrices) for dailyHousePrices in self.simulation.luxuryHousePrices]
        averageEntryPrices = [self.get_average(dailyHousePrices) for dailyHousePrices in self.simulation.entryHousePrices]       

        plt.plot(range(len(averageEntryPrices)),averageEntryPrices, 'ro', label = 'Entry')
        plt.plot(range(len(averageLuxuryPrices)),averageLuxuryPrices, 'ro', color = 'blue', label = 'Luxury')
        plt.ylim(bottom=0)
        plt.xlabel('Years')
        plt.ylabel('Price $')
        plt.title('Average housing Price')
        plt.legend()
        plt.show()
    
    def boxPlotPrices(self, luxury:bool):
        data = self.simulation.luxuryHousePrices if luxury else self.simulation.entryHousePrices

        fig = plt.figure(figsize =(15, 7))
        plt.boxplot(data)
        plt.xlabel('Years')
        plt.ylabel('Housingprice $')
        title = 'Luxury housing prices' if luxury else 'Entry housing prices'
        plt.title(title)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

    def numbOfDailyTrades(self):
        #create two lists
        numbOfLuxuryTrades = [len(dailyHousePrices) for dailyHousePrices in self.simulation.luxuryHousePrices]
        numbOfEntryTrades = [len(dailyHousePrices) for dailyHousePrices in self.simulation.entryHousePrices]

        #create plot 
        fig, ax = plt.subplots()
        index = np.arange(len(numbOfLuxuryTrades))
        bar_width = 0.5
        opacity = 0.8

        Entry = plt.bar(index, numbOfLuxuryTrades, bar_width, alpha=opacity, color='b',
        label='Luxury homes')

        Luxury = plt.bar(index + bar_width, numbOfEntryTrades, bar_width,
        alpha=opacity,
        color='r',
        label='Entry homes')

        plt.xlabel('years')
        plt.ylabel('Number of trades')
        plt.title('Houses traded on each day')
        plt.legend()
        plt.tight_layout()
        plt.show()