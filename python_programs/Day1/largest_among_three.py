#Check among the largest among three numbers
num1=int(input("Enter the first number:-"))
num2=int(input("Enter the second number:-"))
num3=int(input("Enter the third number:-"))
if num1>num2:
    if num1>num3:
        print("num1 is the largest")
    else:
        print("num3 is the largest") 
elif num2>num1:
    if num2>num3:
        print("num2 is the largest")
    else:
        print("num3 is largest")
else:
    print("num 3 is largest")   