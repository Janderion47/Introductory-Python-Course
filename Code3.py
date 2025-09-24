# Problem 1
Name = input("Hello, what is your name?: ")
print("Hi {}, it is good to have you here.".format(Name))

# Problem 2
ToReverse = input("Please input a word to be reversed.")
ReversedString = ToReverse[::-1]
print("Reversed: {}".format(ReversedString))

# Problem 3
Meow = input("Please give a sentence.")
print("The length of the string is {}".format(len(Meow)))

# Problem 4
Meeow= input("Please give another sentence or word.")
vowelcount=0
for i in Meeow:
    if i in ["a","e","i","o","u"]:
        vowelcount+=1
print("The number of vowels in that input is {}".format(vowelcount))

# Problem 5
Meeeow=input("Provide a word please.")
if Meeeow == Meeeow[::-1]:
    print("{} is a palindrome.".format(Meeeow))
else:
    print("{} is not a palindrome.".format(Meeeow))

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