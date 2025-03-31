import math

a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

lcm = (a * b) // math.gcd(a, b)
print("LCM of", a, "and", b, "is:", lcm)
