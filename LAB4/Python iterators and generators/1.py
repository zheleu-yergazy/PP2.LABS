def square_to_n(N):
    for i in range (1, N + 1):
        yield i**2
        
N = int(input("Enter: "))

for i in square_to_n(N):
    print(i)