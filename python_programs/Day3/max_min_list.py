#AIM:-To find the maximum and minimum element in a list
list=[2,100,3,40,15,90,1,34]
max=list[0]
n=len(list)

for i in range(1,n):
    if list[i]>max:
        max=list[i]
print("The max number is:-",max)
#finding min
min=list[0]
n=len(list)

for i in range(1,n):
    if list[i]<min:
        min=list[i]
print("The min number:-",min)
