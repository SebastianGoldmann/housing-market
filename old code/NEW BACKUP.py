import numpy as np
from enum import IntEnum
import random

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
        return - np.exp(-self.wealth/a) + - np.exp(-self.housingType*200000/a) + 2
    
    def calculatePossibleUtility(self, possibleWealth,  possibleHouse):
        a = 10**6
        return - np.exp(-possibleWealth/a) + - np.exp(-possibleHouse*200000/a) + 2

    def buyPriceCalculator(self, targetHousingtype):
        #Input wealth, house currently owning and target buyinghome type
        #Return the maximal price for which the utility is higher with buying the target home

        if self.housingType >= targetHousingtype:
            return None
        else:
            for amount in 10**6 - np.linspace(0, 10**6, 1001):
                possibleUtility = self.calculatePossibleUtility(possibleHouse=targetHousingtype, possibleWealth=self.wealth-amount)
                if possibleUtility > self.currentutility:
                    price = amount
                    if amount > self.wealth:
                        price = self.wealth
                    return price

    def sellPriceCalculator(self, targetHousingtype):
        # Imput wealth, house currently owning and target home you want to move to
        # Return the maximal price for which the utility is higher with selling your home and moving to the target home
        if self.housingType <= targetHousingtype:
            return None
        else:
            for amount in  np.linspace(0,10**6,1001):
                possibleUtility = self.calculatePossibleUtility(possibleWealth=self.wealth+amount, 
                                                                possibleHouse=targetHousingtype)
                if possibleUtility > self.currentutility:
                    return amount

    def calculateBuyAndSellPrice(self):

        for targetHousetype in list(HousingTypes):
            self.askPriceTargetHouse[targetHousetype] = self.sellPriceCalculator(targetHousetype)
            self.bidPriceTargetHouse[targetHousetype] = self.buyPriceCalculator(targetHousetype)
        return

    def Salary(self):
        self.wealth += np.random.normal()*20000
        return

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
    averagePrices = []
    def __init__(self):
        print('simulation initialized...')

    def createStarters(self, numbOfStarters, intialWealth):
        #adds the starter persons to the population
        for i in range(numbOfStarters):
            self.population.append(Person(wealth= intialWealth, housingType=HousingTypes.NOHOUSE,personType=PersonTypes.STARTER))
        return 

    def createMovers(self, numbOfMovers, intialWealth, percentageInEntry):
        #Adds the mover persons to the population
        for _ in range(int(numbOfMovers*percentageInEntry)):
            self.population.append(Person(wealth= intialWealth, housingType=HousingTypes.ENTRYHOME,personType=PersonTypes.MOVER))
            
        for _ in range(int((1-percentageInEntry)*numbOfMovers)):
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
        for person in self.population:
            try:
                if person.bidPriceTargetHouse[targetHouse] >= minAsk:
                    buyers.append(person)
                    self.population.remove(person)
            except TypeError: pass
            try:
                if person.askPriceTargetHouse[housingType] <= maxBid:
                    sellers.append(person)
                    self.population.remove(person)
            except TypeError: pass
        return buyers, sellers

    def determinePrice(self, bid, ask):
        # Generate a random number within the range of prices
        priceRange = bid - ask
        price = np.random.uniform(priceRange)
        return price

    def createEqualLengthList(self, buyers, sellers):
        #makes the buyers and sellers equal length and returns the excess to the population.
        buyers = buyers
        sellers = sellers
        if len(buyers) > len(sellers):
            self.population.append(buyers[len(buyers)+1:])
            del buyers[len(buyers)+1:]
        if len(sellers) < len(sellers):
            self.population.append(sellers[len(sellers)+1:])
            del sellers[len(sellers)+1:]
        return buyers, sellers

    def trade(self):
        for housingType in HousingTypes:
            for targetHouse in range(housingType+1,2):
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
                            print('we are trading')
                            # Trade the houses and update the wealth of the buyer and seller
                            price = self.determinePrice(buyer.bidPriceTargetHouse[targetHouse], seller.askPriceTargetHouse[housingType])
                            buyer.housingType = seller.housingType
                            seller.housingType = housingType
                            buyer.wealth -= price
                            seller.wealth += price
                            #self.averagePrices.append(np.average(tempPrices))
                        # Return the buyer and seller to the original list and remove them from the partition       
                        self.population.append(buyer)
                        self.population.append(seller)
                        buyers.remove(buyer)
                        sellers.remove(seller)              
                except TypeError: 
                    print('empty list')
                    pass



    def updatePersons(self):
        # Iterate over all the persons and add their salary to their wealth
        for person in self.population:
            person.Salary()         
            person.calculateUtility()
            person.calculateBuyAndSellPrice()

    def simulate(self, tradingDays):
        #simulate for N tradingdays.
        if not self.population:
            print('add players to the simulation first')
            exit()
        else:
            print('trading started...')
            for _ in range(tradingDays):
                self.updatePersons() 
                self.trade()
            print('trading finished')
            

# testing
def main():
    population = Population()
    population.createMovers(percentageInEntry=0.5, numbOfMovers=2, intialWealth=0)
    population.createStarters(numbOfStarters=1, intialWealth=10000_000)
    population.simulate(tradingDays=2)
    print('we are done')


if __name__ == "__main__":
    main()