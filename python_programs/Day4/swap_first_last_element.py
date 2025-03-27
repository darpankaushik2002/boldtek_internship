#AIM:-To swap first and last element of a list
mylist=[15,16,3,4,5,3]
size=len(mylist)
temp=mylist[0]
mylist[0]=mylist[size-1]
mylist[size-1]=temp
print("List after swapping",mylist)
