import math

def area_of_polygon(n, a):
    if n < 3 or a <= 0:
        return "Invalid polygon: must have at least 3 sides and positive length."
    area = (n * a**2) / (4 * math.tan(math.pi / n))
    return area

n = int(input("Enter number of sides: "))
a = float(input("Enter length of each side: "))

result = area_of_polygon(n, a)

# Проверяем: число это или текст
if isinstance(result, (int, float)):
    print("Area of the regular polygon:", round(result, 3))
else:
    print(result)

