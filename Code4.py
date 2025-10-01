def c_to_f(celsius):
    fahrenheit = (celsius * 9/5)+32
    return fahrenheit

def f_to_c(fah):
    celsius = (fah - 32) * 5/9
    return celsius

userin = input("What temperature unit do you have to convert from? (Type 'C' if you have a celsius value and 'F' if you have a fahrenheit value.)")
temp = float(input("What is the temperature in that unit?"))
if userin.upper() == "C":
    print(f"The temperature in fahrenheit is {c_to_f(temp)}.")
if userin.upper() == "F":
    print(f"The temperature in celsius is {f_to_c(temp)}.")