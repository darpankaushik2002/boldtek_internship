num = 153
total = sum(int(d)**3 for d in str(num))
print("Armstrong" if total == num else "Not Armstrong")
