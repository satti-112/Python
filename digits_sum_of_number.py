print("Welcome to calculator of sum of digits of a number")
num = int(input("Enter a number (0-1000): "))
total = 0

while num > 0:
    digit = num % 10
    total += digit
    num = num // 10

print("Sum of digits is:", total)
