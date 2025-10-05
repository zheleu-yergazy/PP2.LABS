def div_by_2(N):
    for i in range (0, N + 1):
        if i%2==0:
            yield i
            
N = int(input())

str = [str(i) for i in div_by_2(N)]
print(",".join(str) + ".")