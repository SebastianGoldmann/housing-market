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

        plt.plot(range(len(averageEntryPrices)),averageEntryPrices, color = 'red', label = 'Entry')
        plt.plot(range(len(averageLuxuryPrices)),averageLuxuryPrices, color = 'blue', label = 'Luxury')
        plt.ylim(bottom=0)
        plt.xlabel('Years')
        plt.ylabel('$')
        plt.title('Average housing Prices per year')
        plt.legend()
        plt.show()
    
    def boxPlotPrices(self, luxury:bool):
        data = self.simulation.luxuryHousePrices if luxury else self.simulation.entryHousePrices

        fig = plt.figure(figsize =(15, 7))
        plt.boxplot(data)
        plt.xlabel('weeks')
        plt.ylabel('$')
        title = 'Luxury housing prices' if luxury else 'Entry housing prices'
        plt.title(title)
        plt.xticks(ticks=np.arange(0, len(data), 7))
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

        plt.xlabel('Day')
        plt.ylabel('Number of trades')
        plt.title('Amount traded on each day')
        plt.legend()
        plt.tight_layout()
        plt.show()