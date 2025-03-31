sentence = input("Enter a sentence: ")
words = sentence.split()

word_count = {}  # Empty dictionary to store word counts

for word in words:
    if word in word_count:
        word_count[word] += 1  
    else:
        word_count[word] = 1  
print("Word frequency:", word_count)
