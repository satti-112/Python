while True:
    number = int(input("Enter a number: "))

    if number < 2:
        print("Not a prime number. Try again.")
        continue

    is_prime = True  # Assume it's prime unless we find a factor

    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            is_prime = False
            break

    if is_prime:
        print("Prime number entered. Program ends.")
        break
    else:
        print("Not a prime number. Try again.")
