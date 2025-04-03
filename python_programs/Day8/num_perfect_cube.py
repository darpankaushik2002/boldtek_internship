num = int(input("Enter a number: "))
root = int(num ** (1/3))
print("Perfect Cube" if root ** 3 == num else "Not a Perfect Cube")
