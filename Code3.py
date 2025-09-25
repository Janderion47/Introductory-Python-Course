# Problem 1
Name = input("Hello, what is your name?: ")
print("Hi {}, it is good to have you here.".format(Name))
# Receives the name and prints it in a nice sentence.

# Problem 2
ToReverse = input("Please input a word to be reversed.")
ReversedString = ToReverse[::-1]
print("Reversed: {}".format(ReversedString))
# The Variable[::-1] reverses a string.

# Problem 3
Meow = input("Please give a sentence.")
print("The length of the string is {}".format(len(Meow)))
# len() takes strings and returns the length of the string.

# Problem 4
Meeow= input("Please give another sentence or word.")
vowelcount=0
for i in Meeow:
    if i in ["a","e","i","o","u"]:
        vowelcount+=1
print("The number of vowels in that input is {}".format(vowelcount))
# A 'for' loop takes every element in a variable (string,etc)
# and works with each one to do some operation.
# This 'for' loop will look at every letter in the input and will
# increment the 'vowelcount' variable by 1.

# Problem 5
Meeeow=input("Provide a word please.")
if Meeeow == Meeeow[::-1]:
    print("{} is a palindrome.".format(Meeeow))
else:
    print("{} is not a palindrome.".format(Meeeow))
# Using the string reversal trick learned for problem 2, we compare the
# input variable with it's reversed form. It will print that the word
# is or is not a palindrome.

# Problem 6
secret = input("Provide something to make secret: ")
output = ""
for i in secret:
    if i == ' ':
        output += "_"
    else:
        try:
            output += i.upper()
        except:
            pass

print(output)
# For every character in the input string, it will add an underscore for each
# space in the string, and will return the uppercase form of every letter.