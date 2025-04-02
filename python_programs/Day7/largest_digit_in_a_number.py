num = int(input("Enter a number: "))
largest = 0
while num > 0:
    largest = max(largest, num % 10)
    num //= 10
print("Largest Digit:", largest)
