s = "hello world"
count = sum(1 for char in s if char.lower() in 'aeiou')
print("Vowel Count:", count)
