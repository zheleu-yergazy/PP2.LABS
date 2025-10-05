def square_to_n(N):
    if N==0:
        print("Invalid value!!!")
        return
    for i in range (0, N + 1):
        if i%3==0 and i%4==0:
            yield i
            
N = int(input())

str = [str(i) for i in square_to_n(N)]
print(",".join(str) + ".")