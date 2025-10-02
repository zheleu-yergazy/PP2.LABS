def grams_to_ounces(grams):
    return 28.3495231 * grams

grams = float(input("Введите массу в граммах: "))

ounces = grams_to_ounces(grams)
print(f"{grams} грамм = {ounces} унций")
 
