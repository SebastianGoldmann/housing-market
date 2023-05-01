import numpy as np
from enum import IntEnum
import random
import matplotlib.pyplot as plt
from tqdm import tqdm

class HousingTypes(IntEnum):
    NOHOUSE = 0
    ENTRYHOME = 1
    LUXURY = 2

class PersonTypes(IntEnum):
    STARTER = 0
    MOVER = 1

class Person():
    """
    A class to represent a person.

    Attributes
    ----------
    personType
        Defines the financial status of a person.
    housingType
        Defines which housingtype belongs to this person.
    wealth
        Defines the amount of money this person has.
    buyPrices
        Defines the maximun he is willing to pay for a given house.
    sellPrice
        Defines the minimun he wants for his current house.


    Methods
    -------
    def calculateUtility(self):
        This method calculates the current utilty based on his wealth and housingtype.
    """

    def __init__(self, personType: PersonTypes, housingType: HousingTypes, wealth: int):
        self.personType = personType
        self.housingType = housingType
        self.wealth = wealth
        self.currentutility = self.calculateUtility()
        self.bidPriceTargetHouse = [None, None, None]
        self.askPriceTargetHouse = [None, None, None]

    def calculateUtility(self):
        a = 10**6
        return (- np.exp(-self.wealth/a) + - np.exp(-self.housingType*200000/a) + 2)
    
    def calculatePossibleUtility(self, possibleWealth,  possibleHouse):
        a = 10**6
        return (- np.exp(-possibleWealth/a) + - np.exp(-possibleHouse*200000/a) + 2)

    def buyPriceCalculator(self, targetHousingtype):
        #Input wealth, house currently owning and target buyinghome type
        #Return the maximal price for which the utility is higher with buying the target home

        if self.housingType >= targetHousingtype:
            return None
        else:
            for amount in self.wealth - np.linspace(0, self.wealth, 1001):
                possibleUtility = self.calculatePossibleUtility(possibleHouse=targetHousingtype, possibleWealth=self.wealth-amount)
                if possibleUtility > self.currentutility:
                    if amount > self.wealth:
                        return self.wealth
                    if self.wealth <0:
                        return None
                    else:
                        return amount
            return None

    def sellPriceCalculator(self, targetHousingtype):
        # Imput wealth, house currently owning and target home you want to move to
        # Return the maximal price for which the utility is higher with selling your home and moving to the target home
        if self.housingType <= targetHousingtype:
            return None
        else:
            for amount in  np.linspace(0,10**9,1001):
                possibleUtility = self.calculatePossibleUtility(possibleWealth=self.wealth+amount, possibleHouse=targetHousingtype)
                if possibleUtility > self.currentutility:
                    return amount
            return None

    def calculateBuyAndSellPrice(self):
        for house in list(HousingTypes):
            self.askPriceTargetHouse[house] = self.sellPriceCalculator(house)
            self.bidPriceTargetHouse[house] = self.buyPriceCalculator(house)

    def Salary(self):
        self.wealth += np.random.normal()*10_000_000

class Population:
    """
    A class that that represents the population filled with person classes. 
    
    Attributes
    ----------
    The population creates an empty list for all the persons.

    Methods
    -------
    def createStarters(self, numbOfStarters, intialWealth):
        Adds the starter persons to the population
    
    def createMovers(self, numbOfMovers, intialWealth, percentageInEntry):
        Adds the mover persons to the population

    def findMaxBidMinAsk(self, housingType):
        Find the person with the highest bid and lowest ask for the given housing type

    def partitionPersons(self, housingType, maxBid, minAsk):
        Partition the persons that are willing to buy or sell between the given prices
    
    def createEqualLengthList(self, buyers, sellers):
        makes the buyers and sellers equal length and returns the excess to the population.
                
    """
    population = []
    luxuryHousePrices = []
    entryHousePrices = []
    def __init__(self):
        print('simulation initialized...')

    def createStarters(self, numbOfStarters, intialWealth):
        #adds the starter persons to the population
        for i in range(numbOfStarters):
            self.population.append(Person(wealth= intialWealth, housingType=HousingTypes.NOHOUSE,personType=PersonTypes.STARTER))
        return 

    def createMovers(self, numbOfMovers, intialWealth, percentageInEntry):
        #Adds the mover persons to the population
        for _ in range(int((numbOfMovers+1)*percentageInEntry)):
            self.population.append(Person(wealth= intialWealth, housingType=HousingTypes.ENTRYHOME,personType=PersonTypes.MOVER))
            
        for _ in range(int((1-percentageInEntry)*(numbOfMovers))):
               self.population.append(Person(wealth= intialWealth, housingType=HousingTypes.LUXURY,personType=PersonTypes.MOVER))
        return 

    def findMaxBidMinAsk(self, housingType, targetHouse):
        #Find the person with the highest bid and lowest ask for the given housing type
        maxBid = -1
        minAsk = float('inf')
        for person in self.population:
            #determine max bid
            if person.bidPriceTargetHouse[targetHouse] != None:
                if person.bidPriceTargetHouse[targetHouse] > maxBid:
                    maxBid = person.bidPriceTargetHouse[targetHouse]
            #determine min ask.
            if person.askPriceTargetHouse[housingType] != None:   
                if person.askPriceTargetHouse[housingType] < minAsk:
                    minAsk = person.askPriceTargetHouse[housingType]
        return maxBid, minAsk
    
    def partitionPersons(self, housingType, targetHouse, maxBid, minAsk):
        # Partition the persons that are willing to buy or sell between the given prices
        buyers = []
        sellers = []
        #check if persons are in list.
        for person in self.population:
            #add buyers
            try:
                if person.bidPriceTargetHouse[targetHouse] >= minAsk:
                    buyers.append(person)
                    self.population.remove(person)
            except TypeError: pass
            #add sellers
            try:
                if person.housingType == targetHouse and person.askPriceTargetHouse[housingType] <= maxBid:
                    sellers.append(person)
                    self.population.remove(person)
            except TypeError: pass
        return buyers, sellers

    def determinePrice(self, bid, ask):
        # Generate a random number within the range of prices
        priceRange = bid - ask
        return (ask + priceRange/2)

    def createEqualLengthList(self, buyers, sellers):
        #makes the buyers and sellers equal length and returns the excess to the population.
        buyers = buyers
        sellers = sellers
        if len(buyers) > len(sellers):
            self.population = self.population + buyers[len(sellers):]
            del buyers[len(sellers):]
        if len(sellers) < len(sellers):
            self.population =  self.population + sellers[len(buyers):]
            del sellers[len(buyers):]
        return buyers, sellers

    def trade(self):
        luxuryPrices = []
        entryPrices = []
        for housingType in range(0,1):
            for targetHouse in range(housingType+1,3):
                # Find the max bid and min ask from current to target house
                maxBid, minAsk = self.findMaxBidMinAsk(housingType, targetHouse)

                # Partition the persons that are willing to buy or sell between these prices
                buyers, sellers = self.partitionPersons(housingType, targetHouse, maxBid, minAsk)
                buyers, sellers = self.createEqualLengthList(buyers, sellers)
                random.shuffle(buyers)
                # Iterate over the buyers and sellers and make them trade if the bid is higher than the ask
                try:
                    for buyer, seller in zip(buyers, sellers):
                        if buyer.bidPriceTargetHouse[targetHouse] > seller.askPriceTargetHouse[housingType]:
                            # Trade the houses and update the wealth of the buyer and seller
                            price = self.determinePrice(buyer.bidPriceTargetHouse[targetHouse], seller.askPriceTargetHouse[housingType])
                            seller.housingType = HousingTypes(housingType)
                            buyer.housingType = HousingTypes(targetHouse)
                            buyer.wealth -= price
                            seller.wealth += price
                            #append housing sell prices.
                            if targetHouse == HousingTypes.LUXURY:
                                luxuryPrices.append(price)
                            else:
                                entryPrices.append(price)
                except TypeError:            
                    pass
                #Return the buyers and sellers to population
                self.population = self.population + buyers + sellers
            self.entryHousePrices.append(entryPrices) 
            self.luxuryHousePrices.append(luxuryPrices)

    def updatePopulation(self):
        # Iterate over all the persons and add their salary to their wealth
        for person in self.population:
            person.Salary()         
            person.currentutility = person.calculateUtility()
            person.calculateBuyAndSellPrice()

    def simulate(self, tradingDays):
        #simulate for N tradingdays.
        if not self.population:
            print('add players to the simulation first')
            exit()
        else:
            for _ in tqdm(range(tradingDays)):
                self.updatePopulation() 
                self.trade()
            print('simulation ended') 

#Example on how to start a simulation.
def main():
    population = Population()
    population.createMovers(numbOfMovers=200, percentageInEntry=0.5, intialWealth=100_000)
    population.createStarters(numbOfStarters=200, intialWealth=600_000)
    population.simulate(tradingDays=100)


    '''
    Hierna kan je data analyze doen met de verzamelde data. Mocht je meer data 
    willen verzamelen, dan moet je dat in de classes toevoegen
    '''

if __name__ == "__main__":
    main()