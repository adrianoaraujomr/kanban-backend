def my_pow(i, n):
    return multiplication(i, n)

def multiplication(i, n):
    result = 0
    for x in range(0, n):
        result += i
    return result