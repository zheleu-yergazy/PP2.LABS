def filter_prime(numbers):
    primes = []
    for n in numbers:
        if n > 1:
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    break
            else:
                primes.append(n)
    return primes

nums = list(map(int, input("Введите числа через пробел: ").split()))
print(filter_prime(nums))
