#Aim:-to sort words in a given string in alphabetical order
a=input("Enter a string:-")
w=a.split(" ")
print(w)
for i in range (len(w)):
    w[i]=w[i].lower()
w.sort()
print("the sorted words",w)