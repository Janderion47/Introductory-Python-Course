# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 09:35:09 2025

"""

# print("Bruh")

temperature = None
Response = None

while temperature == None: # Will keep looping as long as the "temp == None" is true.
    try:
        temperature = float(input("What is the patient's temperature?: "))
    except ValueError: # ValueError is when float() is unhappy about it's input.
        print("Please input a valid value for temperature.")

if temperature >= 99.5:
    Response = "The patient has a high temperature."
elif temperature < 99.5:
    Response = "The patient's temperature is normal."

print(Response)