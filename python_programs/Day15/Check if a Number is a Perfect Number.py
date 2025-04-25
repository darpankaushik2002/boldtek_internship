num = 28
divisors = [i for i in range(1, num) if num % i == 0]
if sum(divisors) == num:
    print("Perfect Number")
else:
    print("Not Perfect")
