def reverse_words(sentence):
    words = sentence.split()
    reversed_words = [word[::-1] for word in words]
    return ' '.join(reversed_words)

# Example usage:
input_str = "My Name is Jessa"
print(reverse_words(input_str))  # Output: yM emaN si asseJ
