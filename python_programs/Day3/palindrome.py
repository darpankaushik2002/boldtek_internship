#AIM:-Check if the given string is palindrome or not
a=input("Enter a string:-")
rev=a[::-1]
if a == rev:
    print("The string is palindrome")
else:
    print("This is not palindrome")