text = input("Enter text: ")
freq = {}
for ch in text:
    freq[ch] = freq.get(ch, 0) + 1
max_char = max(freq, key=freq.get)
print("Most frequent character:", max_char)
