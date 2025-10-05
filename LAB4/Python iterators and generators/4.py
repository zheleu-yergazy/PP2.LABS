def squares(A,B):
    for i in range (A, B + 1):
        yield i**2
        
A = int(input("Enter a: "))
B = int(input("Enter b: "))

for i in squares(A,B):
    print(i)