text = input("Enter a string: ")
result = ""
for ch in text:
    if ch not in result:
        result += ch
print("Without duplicates:", result)
