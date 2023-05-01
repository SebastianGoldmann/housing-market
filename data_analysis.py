import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

data = pd.read_csv("./DATA/data_file.csv", sep=';')

# replace income group name by just their values
def add_column(df):
    col1 = []
    col2 = []
    value1 = -6
    value2 = -4
    for i in range(len(df)):
        col1.append(value1)
        col2.append(value2)
        if value1 == 102:
            break
        value1 += 2
        value2 += 2
        if value1 == 100:
            value1 += 2
            value2 += 2
    df['starting_value'] = col1
    df['ending_value'] = col2
    return df

add_column(data)

data = data.drop(columns='Income group')


for i in range(len(data.starting_value)):
    plt.bar(data.starting_value[i], data['Households, total'][i], width=data.ending_value[i]-data.starting_value[i], align='edge', label = 'Household incomes')

# Generate data for the log-normal distribution
mean, sigma = 28, 0.4
x = np.linspace(0, 100, 1000)
pdf = stats.lognorm.pdf(x, sigma, scale=mean)

scale_factor = max(data['Households, total'])/ max(pdf)
pdf *= scale_factor

# Plot the log-normal distribution
plt.plot(x, pdf, color='red', linewidth=2, label = 'lognormal')
plt.title('standardized income')
plt.ylabel('number of households')
plt.xlabel('standardized income (x1000 euro)')
# Show the plot
#plt.show()

print(np.random.lognormal(sigma = 0.4)*28000)