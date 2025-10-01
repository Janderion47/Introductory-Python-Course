# Problem 1
name = input("What is your name? ")
print(f"Hello, {name}. Nice to meet you")

# Problem 2
ToReverse = input("Please input a word to be reversed. ")
ReversedString = "".join(reversed(ToReverse))
print(f"{ReversedString}")

# Problem 3
sentence = input("Write a sentence. ")
sentence_len = len(sentence)
print(f"The sentence has {sentence_len} characters.")

# Problem 5
word = input("Enter a word. ")
if word.lower() == word.lower()[::-1]:
    print("The word is a palindrome.")
else:
    print("The word is not a palindrome")

# Problem 4
word = input("Enter a word.")
vowels = "aeiouAEIOU"
vowel_count = sum(1 for char in word if char in vowels)
print(f"Number of vowels: {vowel_count}")
