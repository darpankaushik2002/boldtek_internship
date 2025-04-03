num = int(input("Enter a number: "))
last_digit = num % 10
while num >= 10:
    num //= 10
first_digit = num
print("Sum of First and Last Digit:", first_digit + last_digit)
