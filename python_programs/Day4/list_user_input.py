data=[]
while True:
    name=input("Enter the name:")
    data.append(name)
    
    choice=input("Enter another name??(y/n) : ")
    if choice.casefold() == "n":
        break

for element in data:
    print(element)