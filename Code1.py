# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 09:43:06 2025

@author: jadenpaula
"""

#from uncertainties import ufloat

Unit_measurement = 100000 # Per this many people

InitialPopulation=int(input('Beginning Population?: '))

Prevalence = int(input("How many affected?: "))*Unit_measurement/InitialPopulation
print("Prevalence:", Prevalence, "per", Unit_measurement, "people were affected.")

Incidence = int(input("How many new people affected?: "))*Unit_measurement/InitialPopulation
print("Incidence: ",Incidence, "per", Unit_measurement, "was the incidence rate for the time period.")

MortalityRate=int(input("How many people died?: "))*Unit_measurement/InitialPopulation
print("Mortality Rate:", MortalityRate, "per", Unit_measurement, "people died for the time period.")

# TODO: Need to add calculation of the years lost