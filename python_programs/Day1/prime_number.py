#AIM:- To check if number is prime or composite
num=int(input("Enter any number:-"))
if num==1:
    print("num is neither prime nor composite")
elif num > 1:
    for i in range(2,num):
        if num % i ==0:
            print("num is composite")
            break
    else:
        print("num is prime")
            