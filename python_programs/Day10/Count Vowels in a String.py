def count_vowels(s):
    vowels = 'aeiouAEIOU'
    return sum(1 for char in s if char in vowels)

# Example usage:
print(count_vowels("Hello World"))  # Output: 3
