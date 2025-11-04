def climbStairs(n):
    if n == 0 or n == 1:
        return 1
    else:
        return climbStairs(n - 1) + climbStairs(n - 2)

print("Enter the number of steps:")
n = int(input())
print("Number of ways to climb the staircase:", climbStairs(n))
