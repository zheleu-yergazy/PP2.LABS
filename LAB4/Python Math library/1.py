import math

def deg_to_rad(D):
    return D * math.pi / 180

x = int(input("Enter degree: "))

print(round(deg_to_rad(x),5))