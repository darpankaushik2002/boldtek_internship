#AIM:- To find factorial of a number
num=int(input("enter any number:-"))
if num <0:
    print("factorial doesnot exist for negative number")
if num ==0:
    print("factorial is 1")
fact=1
if num>0:
    
    for i in range(1,num+1):
        fact=fact*i
    print("factorial of the given number is:-",fact)
