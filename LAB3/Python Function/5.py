from itertools import permutations

def print_permutations():
    s = input("Введите строку: ")
    for p in permutations(s):
        print("".join(p))

print_permutations()
