#AIM:- To print prime number in an interval
lower=int(input("Enter lower limit number:-"))

upper=int(input("Enter upper limit number:-"))

for num in range(lower,upper+1):
    if num >1:
        for i in range(2,num):
            if num % 2==0:
                break
        else:
            print(num)
    