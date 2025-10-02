def fahrenheit_to_celsius(f):
    return (5 / 9) * (f - 32)

f = float(input("Введите температуру в градусах Фаренгейта: "))

c = fahrenheit_to_celsius(f)

print(f"{f}°F = {c:.2f}°C")

    