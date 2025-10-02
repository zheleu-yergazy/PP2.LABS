def reverse_words():
    s = input("Введите предложение: ")
    words = s.split()
    return " ".join(words[::-1])

print(reverse_words())
