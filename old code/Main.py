# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 15:54:12 2022

@author: andre
"""
import numpy as np

#%% defenitions
def utilityTot(wealth, housingtype):
    '''
    Input Wealth what a person has on his bank, housingtype is a integer: 0= no house, 1 = entry home, 2 = Luxourios home
    Output is utilty
    '''
    a = 10**6
    utility = - np.exp(-wealth/a)  + - np.exp(-housingtype*200000/a) +2
    return utility

def buyPriceCalculator(wealth, currentHouse, moveTo):
    '''
    Imput wealth, house currently owning and target buyinghome type
    Return the maximal price for which the utility is higher with buying the target home
    '''
    if currentHouse>= moveTo: 
        print('you dont want to buy')
        return False
    else:
        
        currentUtility = utilityTot(wealth, currentHouse)
        for amound in 10**6 - np.linspace(0,10**6,1001):
            possibleUtility = utilityTot(wealth-amound, moveTo)
            if possibleUtility > currentUtility:
                price = amound
                if amound >wealth:
                    price = wealth
                return price
                break
def sellPriceCalculator(wealth, currentHouse, moveTo):
    ''''
    Imput wealth, house currently owning and target home you want to move to
    Return the maximal price for which the utility is higher with selling your home and moving to the target home
    '''
    if currentHouse<= moveTo: 
        print('you dont want to sell')
        return False
    else:
        currentUtility = utilityTot(wealth, currentHouse)
        for amound in np.linspace(0,10**6,1001):
            possibleUtility = utilityTot(wealth+amound, moveTo)
            if possibleUtility > currentUtility:
                price = amound
                return price
                break  

def buySellPriceInGridElement(gridRow):
    '''
    imput is a row of the grid holding the following structure:
    
    Colomn 0, type of person : 0 = starter, 1 = mover
    Colomn 1, type of current home: 0= no home, 1 = entry home, 2 = luxory home
    Colomn 2, current wealth

    output is the right buy and sell prices for certain movements, holding the following scruture 
    Minimal Sell or maximal buy prices for certain moves
    Colomn 3, 0-> 1
    Colomn 4, 1-> 0
    Colomn 5, 0-> 2
    Colomn 6, 2-> 0
    Colomn 7, 1-> 2
    Colomn 8  2-> 1
    '''
    returnGridRow = gridRow
    currentHouse = gridRow[1]
    wealth = gridRow[2]
    
    
    if currentHouse == 0:
        returnGridRow[3] = buyPriceCalculator(wealth, currentHouse, 1)
        returnGridRow[5] = buyPriceCalculator(wealth, currentHouse, 2)
    if currentHouse == 1:
        returnGridRow[4] = sellPriceCalculator(wealth, currentHouse, 0)
        returnGridRow[7] = buyPriceCalculator(wealth, currentHouse, 2)
    if currentHouse == 2:
        returnGridRow[6] = sellPriceCalculator(wealth, currentHouse, 0)
        returnGridRow[8] = sellPriceCalculator(wealth, currentHouse, 1)
        
    return returnGridRow

def wealthNextYear(currentWealth):

    '''
    imput current wealth
    output new wealth for next year
    '''
    futureWealth = currentWealth + np.random.normal()*20000
    return futureWealth

def Dealmaker(players):
    '''
    The minimum bid will be connected to the minimum ask. 
    '''
    pass

#%% Grid initialisaton
numberStart = 50
initialWealthStart = 380000
numberMover = 50
initialWealthMover = 50000

'''
Colomn 0, type of person : 0 = starter, 1 = mover
Colomn 1, type of current home: 0= no home, 1 = entry home, 2 = luxory home
Colomn 2, current wealth

Minimal Sell or maximal buy prices for certain moves
Colomn 3, 0-> 1
Colomn 4, 1-> 0
Colomn 5, 0-> 2
Colomn 6, 2-> 0
Colomn 7, 1-> 2
Colomn 8  2-> 1

'''

grid = np.ones((numberStart+numberMover,9))*99
grid2 = np.ones((numberStart+numberMover,9))*99
grid[0:50,0] = 0
grid[50:,0] = 1
grid[0:50,1] = 0
grid[50:75,1] = 1
grid[75:,1] = 2
grid[0:50,2] = initialWealthStart
grid[50:,2] = initialWealthMover

for ii in range(100):
    grid2[ii,:] = buySellPriceInGridElement(grid[ii,:])

#%% ?
