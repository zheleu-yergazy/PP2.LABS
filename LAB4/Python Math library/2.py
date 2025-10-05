def area_of_trap(A,B,C):
    
    if A<0 or B<0 or C<0:
        return "Invalid values: sides and height must be positive."
    
    if abs(B - C) > (B + C) or A > (B + C):
        return "Impossible trapezoid: invalid proportions."

    return (B + C) * A / 2

A = int(input("Enter height: "))
B = int(input("Enter first value: "))
C = int(input("Enter second value: "))
    
print(area_of_trap(A,B,C))