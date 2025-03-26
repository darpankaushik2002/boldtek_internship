#Aim=To find the sum of natural numbers
num=int(input("enter a positive number:-"))
if num <0:
    print("enter positive number")
else:
    sum=0
    while num>0:
        sum=sum+num
        num=num-1
    print(sum)