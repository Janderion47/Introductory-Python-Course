# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 09:43:06 2025

@author: jadenpaula
"""

from decimal import Decimal, getcontext
#from uncertainties import ufloat

getcontext().prec = 3

Unit_measurement = 100000 # Per this many people
InitialPopulation=int(input('Beginning Population?: '))
ConvertStat=Decimal(Unit_measurement/InitialPopulation)

Prevalence = Decimal(input("How many affected?: "))*ConvertStat
print("Prevalence:", Prevalence, "per", Unit_measurement, "people were affected.")

Incidence = Decimal(input("How many new people affected?: "))*ConvertStat
print("Incidence: ",Incidence, "per", Unit_measurement, "was the incidence rate for the time period.")

MortalityRate=Decimal(input("How many people died?: "))*ConvertStat
print("Mortality Rate:", MortalityRate, "per", Unit_measurement, "people died for the time period.")


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
        question1=int(input("What was the age of a person who died? (answer 0 if no ages are known): "))
        
        difference=LifeExpectation-question1
        print("This person lost", difference, "years of life")
