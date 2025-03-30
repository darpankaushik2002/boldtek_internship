#AIM:-Count the number of vowels in a given string
a=input("Enter a string:-")

string=a.lower()
vowels=["a","e","i","o","u"]
count=0
for char in string:
    if char in vowels:
        count=count +1
print("No of vowels" , count)