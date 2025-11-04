# ===== PROBLEM 1: CALCULATOR FUNCTION =====
def calculator(a, b, operation):
    """
    Performs arithmetic operations (add, subtract, multiply, divide) on two numbers.
    
    Args:
        a (float): First number
        b (float): Second number
        operation (str): Operation type ('add', 'subtract', 'multiply', 'divide')
    
    Returns:
        float: Result of the arithmetic operation
    """
    if operation == 'add':
        return a + b
    elif operation == 'subtract':
        return a - b
    elif operation == 'multiply':
        return a * b
    elif operation == 'divide':
        if b == 0:
            raise ValueError("Cannot divide by zero!")
        return a / b
    else:
        raise ValueError("Invalid operation. Choose: 'add', 'subtract', 'multiply', 'divide'")

# ===== PROBLEM 2: LARGEST OF FOUR NUMBERS =====
def largest_of_four(a, b, c, d):
    """
    Returns the largest of four numbers.
    
    Args:
        a, b, c, d (float): Numbers to compare
    
    Returns:
        float: Largest number
    """
    return max(a, b, c, d)

# ===== PROBLEM 3: FIBONACCI SEQUENCE =====
def fibonacci_sequence(n):
    """
    Generates Fibonacci sequence up to the given number n.
    
    Args:
        n (int): Upper limit for the sequence
    
    Returns:
        list: Fibonacci sequence up to n
    """
    sequence = [0, 1]
    while sequence[-1] + sequence[-2] <= n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence

# ===== PROBLEM 4: SHAPE AREA CALCULATOR =====
def area_calculator(shape='rectangle', *args):
    """
    Calculates area of different shapes (rectangle, square, circle, triangle).
    Default shape is rectangle.
    
    Args:
        shape (str): Shape type ('rectangle', 'square', 'circle', 'triangle')
        *args: Measurements required for the shape
        
    Returns:
        float: Calculated area
    """
    if shape == 'rectangle':
        if len(args) != 2:
            raise ValueError("Rectangle requires 2 arguments: length and width")
        return args[0] * args[1]
    
    elif shape == 'square':
        if len(args) != 1:
            raise ValueError("Square requires 1 argument: side")
        return args[0] ** 2
    
    elif shape == 'circle':
        if len(args) != 1:
            raise ValueError("Circle requires 1 argument: radius")
        return 3.14159 * args[0] ** 2
    
    elif shape == 'triangle':
        if len(args) != 2:
            raise ValueError("Triangle requires 2 arguments: base and height")
        return 0.5 * args[0] * args[1]
    
    else:
        raise ValueError("Invalid shape. Choose: 'rectangle', 'square', 'circle', 'triangle'")

# ===== PROBLEM 5: PASCAL'S TRIANGLE =====
def pascals_triangle(n):
    """
    Prints the first n rows of Pascal's triangle.
    
    Args:
        n (int): Number of rows to generate
    """
    triangle = []
    for i in range(n):
        row = [1] * (i+1)
        if i > 1:
            for j in range(1, i):
                row[j] = triangle[i-1][j-1] + triangle[i-1][j]
        triangle.append(row)
        
    # Print formatted triangle
    max_width = len(' '.join(map(str, triangle[-1])))
    for row in triangle:
        print(' '.join(map(str, row)).center(max_width))

# ===== TESTING THE FUNCTIONS =====
if __name__ == "__main__":
    print("Problem 1: Calculator")
    print("5 + 3 =", calculator(5, 3, 'add'))
    print("10 - 4 =", calculator(10, 4, 'subtract'))
    
    print("\nProblem 2: Largest of Four")
    print("Largest of (12, 56, 34, 89):", largest_of_four(12, 56, 34, 89))
    
    print("\nProblem 3: Fibonacci Sequence")
    print("Fibonacci up to 50:", fibonacci_sequence(50))
    
    print("\nProblem 4: Area Calculator")
    print("Rectangle (4x5):", area_calculator('rectangle', 4, 5))
    print("Square (side=4):", area_calculator('square', 4))
    
    print("\nProblem 5: Pascal's Triangle (5 rows)")
    pascals_triangle(5)