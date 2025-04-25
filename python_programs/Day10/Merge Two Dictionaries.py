def merge_dicts(dict1, dict2):
    return {**dict1, **dict2}

# Example usage:
dict_a = {'a': 1, 'b': 2}
dict_b = {'c': 3, 'd': 4}
print(merge_dicts(dict_a, dict_b))  # Output: {'a': 1, 'b': 2, 'c': 3, 'd': 4}
