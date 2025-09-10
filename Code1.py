# -*- coding: utf-8 -*-

from decimal import Decimal, getcontext
#from uncertainties import ufloat

getcontext().prec = 3

Unit_measurement = 100000 # Per this many people
InitialPopulation=int(input('Beginning Population?: '))
ConvertStat=Decimal(Unit_measurement/InitialPopulation)

Prevalence = Decimal(input("How many affected?: "))*ConvertStat
print("Prevalence:", Prevalence, "per", Unit_measurement, "people affected.")

Incidence = Decimal(input("How many new people affected?: "))*ConvertStat
print("Incidence:",Incidence, "new cases per", Unit_measurement, "people.")

MortalityRate=Decimal(input("How many people died?: "))*ConvertStat
print("Mortality Rate:", MortalityRate, "deaths per", Unit_measurement, "people.")


CalcYearsLost = input("Calculate years of potential life lost?: ")
if CalcYearsLost=="y":
    CalcYearsLost=True
else:
    CalcYearsLost=False

LifeExpectation = None

while CalcYearsLost:
    if LifeExpectation==None:
        LifeExpectation= float(input("What is the life expectancy age?: "))
    else:
        try:
            question1=int(input("What was the age of a person who died? (Provide no answer if no ages are known): "))
            difference=LifeExpectation-question1
            if difference<0:
                difference=0
            print("This person lost", difference, "years of life")
        except ValueError:
            CalcYearsLost = False
        
        
