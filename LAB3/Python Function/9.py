import math

def sphere_volume(r):
    return (4/3) * math.pi * r**3

radius = float(input("Введите радиус: "))
print("Объем шара:", sphere_volume(radius))
