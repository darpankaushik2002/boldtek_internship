#AIM:- Program to remove duplicates from a list
data=[10,20,30,40,40,40,20,10,50,60,70]

def remove_duplicates(duplist):
    noduplist=[]
    for elements in duplist :
        if elements not in noduplist:
            noduplist.append(elements)
    return noduplist
       

print(remove_duplicates(data))