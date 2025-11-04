# Simple Student Grade Calculator
# Demonstrates basic Python concepts for beginners

def main():
    """Main function that runs the grade calculator program"""
    print("Welcome to Simple Grade Calculator!")
    print("This program demonstrates basic Python concepts")
    
    # Variables and user input
    student_name = input("Enter student name: ")
    num_subjects = int(input("Enter number of subjects: "))
    
    # Lists to store subject information
    subjects = []
    marks = []
    
    # For loop to collect subject data
    for i in range(num_subjects):
        subject = input(f"Enter name of subject {i+1}: ")
        mark = float(input(f"Enter marks for {subject} (out of 100): "))
        subjects.append(subject)
        marks.append(mark)
    
    # Calculate total and average
    total_marks = sum(marks)
    average = total_marks / num_subjects
    
    # Conditional statements to determine grade
    if average >= 90:
        grade = 'A'
    elif average >= 80:
        grade = 'B'
    elif average >= 70:
        grade = 'C'
    elif average >= 60:
        grade = 'D'
    else:
        grade = 'F'
    
    # Display results
    print("\n" + "="*40)
    print(f"RESULT FOR {student_name.upper()}")
    print("="*40)
    
    # While loop to display subject marks
    i = 0
    while i < num_subjects:
        print(f"{subjects[i]}: {marks[i]}/100")
        i += 1
    
    print("-"*40)
    print(f"TOTAL MARKS: {total_marks}/{num_subjects*100}")
    print(f"AVERAGE: {average:.2f}%")
    print(f"GRADE: {grade}")
    print("="*40)
    
    # Demonstrate string operations
    message = "\nCongratulations " + student_name + "!" if grade in ['A', 'B', 'C'] else "\nBetter luck next time " + student_name + "!"
    print(message)
    
    # Demonstrate simple function
    def get_encouragement(grade):
        """Returns encouragement message based on grade"""
        if grade == 'A':
            return "Excellent work!"
        elif grade == 'B':
            return "Good job!"
        elif grade == 'C':
            return "You passed!"
        else:
            return "Keep practicing!"
    
    print(get_encouragement(grade))

# Run the program
if __name__ == "__main__":
    main()