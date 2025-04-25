def remove_greater_than_50(numbers):
    return [num for num in numbers if num <= 50]

# Example usage:
number_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
print(remove_greater_than_50(number_list))  # Output: [10, 20, 30, 40, 50]
