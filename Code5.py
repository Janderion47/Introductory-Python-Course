import math
from decimal import Decimal
from random import gauss

def calculate_sample_size(z,p,error):
    return int(math.ceil(((Decimal(z)**2)*Decimal(p)*Decimal(1-p))/(Decimal(error)**2)))

#print(calculate_sample_size(1.96,0.5,0.05))

population_size= int(input("Population size? "))
confidence_lvl = int(input("Confidence level? (Enter in units of %) "))
margin_of_error= float(input("Desired margin of error? (Enter in units of %) "))/100

population = []
for _ in range(population_size):
    population.append(round(gauss(),3))

z_input = None

if confidence_lvl == 90:
    z_input = 1.645
elif confidence_lvl==95:
    z_input = 1.960
elif confidence_lvl==99:
    z_input = 2.579
else:
    raise Exception("Margin of error must be 90, 95, or 99.")

statistic = calculate_sample_size(z_input,0.5,margin_of_error)
print(f"The required sample size for systematic sampling is approximately {statistic}")

keep_working = True

while keep_working:
    desired_size = int(input("Sample size that you want to draw? "))
    if statistic < desired_size:
        print("The requested sample size is not feasible given the population size, confidence level, and the margin of error.")
        print(f"The maximum sample size possible given the above data is {statistic}.")
    elif statistic >= desired_size:
        working_data = []
        for i in range(desired_size):
            indexer = (population_size/desired_size)
            working_data.append(population[round(indexer*i)])
        
        print(working_data)
        keep_working=False
    else:
        raise Exception("Huh? That wasn't supposed to happen.")