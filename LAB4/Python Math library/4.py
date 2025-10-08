def area_of_parallelogram(base, height):
    if base <= 0 or height <= 0:
        return "Invalid values: base and height must be positive."
    return base * height

b = float(input("Enter base of the parallelogram: "))
h = float(input("Enter height of the parallelogram: "))

result = area_of_parallelogram(b, h)

if isinstance(result, (int, float)):
    print("Area of the parallelogram:", round(result, 3))
else:
    print(result)
