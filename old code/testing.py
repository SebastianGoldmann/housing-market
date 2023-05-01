
buyers = []
population = [1,2,3,4,5,6]
for person in population:
            if person == 1:
                buyers.append(population.pop(person))

print(population)
print(buyers)

sellers = [45,456,456,657,67,2]

print(zip(buyers,sellers))

for a,b in zip(buyers,sellers):
    print(a)
    print(b)

#FASTER SEARCH ALGORITHMS TO FIND THE BEST PRICES BINARY SEARCH

def buyPriceCalculator(self, targetHousingtype):
    if self.housingType >= targetHousingtype:
        return None

    # Set initial bounds for the binary search
    low = 0
    high = 10**6

    # Keep searching until the bounds are within a certain tolerance
    while high - low > 1e-6:
        # Calculate the midpoint of the current bounds
        mid = (low + high) / 2
        # Calculate the possible utility if the person buys a house
        # at the midpoint price
        possibleUtility = self.calculatePossibleUtility(
            possibleWealth=self.wealth - mid,
            possibleHouse=targetHousingtype
        )
        # If the possible utility is greater than the current utility,
        # we can raise the lower bound of the search
        if possibleUtility > self.currentutility:
            low = mid
        # Otherwise, we can lower the upper bound of the search
        else:
            high = mid
    # Return the lower bound of the search as the maximum price
    # the person is willing to pay for a house
    return low
