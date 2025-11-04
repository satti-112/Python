# Simple Student Grade Management System

# 1. Student Data Entry
name = input("Enter student name: ")
roll_number = input("Enter roll number: ")
num_subjects = int(input("Enter number of subjects: "))

subjects = []
total_obtained = 0
total_marks = 0

# 2. Marks Input
for i in range(num_subjects):
    print(f"\nSubject {i+1}:")
    subject_name = input("  Enter subject name: ")
    subject_total = int(input("  Enter total marks: "))
    subject_obtained = int(input("  Enter obtained marks: "))
    subjects.append({
        'name': subject_name,
        'total': subject_total,
        'obtained': subject_obtained
    })
    total_obtained += subject_obtained
    total_marks += subject_total

# 3. Percentage & GPA Calculation
percentage = (total_obtained / total_marks) * 100

# Simple GPA/Grade scale
if percentage >= 90:
    grade = 'A+'
    gpa = 4.0
elif percentage >= 80:
    grade = 'A'
    gpa = 3.7
elif percentage >= 70:
    grade = 'B'
    gpa = 3.0
elif percentage >= 60:
    grade = 'C'
    gpa = 2.0
elif percentage >= 50:
    grade = 'D'
    gpa = 1.0
else:
    grade = 'F'
    gpa = 0.0

# 4. Result Summary
print("\n--- Result Summary ---")
print(f"Name: {name}")
print(f"Roll Number: {roll_number}")
print(f"Subjects:")

for subj in subjects:
    print(f"  {subj['name']}: {subj['obtained']} / {subj['total']}")

print(f"Total Marks: {total_obtained} / {total_marks}")
print(f"Percentage: {percentage:.2f}%")
print(f"Grade: {grade}")
print(f"GPA: {gpa}")