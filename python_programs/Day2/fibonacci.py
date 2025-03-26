#Aim to print fibonacci sequence
a=0
b=1
num=int(input("Enter the count or number of fibonnaci numbers:-"))
if num==1:
    print(0)
else:
    print(a)
    print(b)
    
    for i in range(2,num):
        c=a+b
        a=b
        b=c
        print(c)
    