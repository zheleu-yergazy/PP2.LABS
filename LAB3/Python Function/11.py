def is_polindrom(word):
    word = word.replace(" ", "").lower()
    return word == word[::-1]

w = input("Вводите слово: ")
if is_polindrom(w):
    print("Это палиндром")
else:
    print("Не палиндром")




