# from docx import Document
# from docx.shared import Pt, Inches
# from docx.enum.text import WD_ALIGN_PARAGRAPH

# # Create document
# doc = Document()

# # ===== TITLE PAGE =====
# title_section = doc.sections[0]
# title_header = title_section.header
# title_para = title_header.paragraphs[0]
# title_para.text = "COMSATS UNIVERSITY ISLAMABAD\nDepartment of Computer Science"
# title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

# # Course information table
# table = doc.add_table(rows=5, cols=2)
# table.style = 'Table Grid'

# # Table data
# data = [
#     ("NAME", "Ahsan Raza\nMuzammil Ghaffar"),
#     ("REGISTRATION NO.", "SP25-BDS-003\nSP25-BDS-034"),
#     ("COURSE INFO.", "CSC101 - INTRODUCTION TO ICT"),
#     ("Assignment no 4", "31 May"),
#     ("INSTRUCTOR", "PROF. MUHAMMAD HARIS")
# ]

# # Populate table
# for row_idx, (label, value) in enumerate(data):
#     label_cell = table.cell(row_idx, 0)
#     value_cell = table.cell(row_idx, 1)
#     label_cell.text = label
#     value_cell.text = value
#     label_cell.paragraphs[0].runs[0].bold = True

# doc.add_page_break()

# # ===== PROBLEM SOLUTIONS =====
# problems = [
#     {
#         "title": "Problem 1: Calculator Function",
#         "desc": "Write a calculator function that takes two numbers and a string specifying the operation and returns the result. It should be able to do addition, subtraction, multiplication, and division.",
#         "code": """def calculator(a, b, operation):
#     if operation == 'add':
#         return a + b
#     elif operation == 'subtract':
#         return a - b
#     elif operation == 'multiply':
#         return a * b
#     elif operation == 'divide':
#         if b == 0:
#             raise ValueError("Cannot divide by zero!")
#         return a / b
#     else:
#         raise ValueError("Invalid operation")"""
#     },
#     {
#         "title": "Problem 2: Largest of Four Numbers",
#         "desc": "Write a program that takes in 4 numbers and returns the largest number of them all.",
#         "code": """def largest_of_four(a, b, c, d):
#     return max(a, b, c, d)"""
#     },
#     {
#         "title": "Problem 3: Fibonacci Sequence",
#         "desc": "Write a function that takes in a number and returns the Fibonacci sequence till that number.",
#         "code": """def fibonacci_sequence(n):
#     sequence = [0, 1]
#     while sequence[-1] + sequence[-2] <= n:
#         sequence.append(sequence[-1] + sequence[-2])
#     return sequence"""
#     },
#     {
#         "title": "Problem 4: Shape Area Calculator",
#         "desc": "Write a function that calculates area for different shapes (square, rectangle, circle, triangle) with rectangle as default.",
#         "code": """def area_calculator(shape='rectangle', *args):
#     if shape == 'rectangle':
#         return args[0] * args[1]
#     elif shape == 'square':
#         return args[0] ** 2
#     elif shape == 'circle':
#         return 3.14159 * args[0] ** 2
#     elif shape == 'triangle':
#         return 0.5 * args[0] * args[1]
#     else:
#         raise ValueError("Invalid shape")"""
#     },
#     {
#         "title": "Problem 5: Pascal's Triangle",
#         "desc": "Write a Python function that prints the first n rows of Pascal's triangle.",
#         "code": """def pascals_triangle(n):
#     triangle = []
#     for i in range(n):
#         row = [1] * (i+1)
#         if i > 1:
#             for j in range(1, i):
#                 row[j] = triangle[i-1][j-1] + triangle[i-1][j]
#         triangle.append(row)
    
#     # Format and print
#     max_width = len(' '.join(map(str, triangle[-1])))
#     for row in triangle:
#         print(' '.join(map(str, row)).center(max_width))"""
#     }
# ]

# # Add problems to document
# for problem in problems:
#     doc.add_heading(problem["title"], level=1)
#     doc.add_paragraph(problem["desc"])
#     doc.add_heading("Solution Code:", level=2)
    
#     code_para = doc.add_paragraph()
#     runner = code_para.add_run(problem["code"])
#     runner.font.name = 'Courier New'
    
#     doc.add_paragraph(" ")

# # ===== RUBRIC SECTION =====
# doc.add_heading("Assignment Evaluation Rubric", level=1)

# # Rubric table
# rubric = doc.add_table(rows=1, cols=5)
# rubric.style = 'Table Grid'
# hdr_cells = rubric.rows[0].cells
# hdr_cells[0].text = 'Criterion'
# hdr_cells[1].text = 'Excellent (85-100%)'
# hdr_cells[2].text = 'Good (70-84%)'
# hdr_cells[3].text = 'Satisfactory (50-69%)'
# hdr_cells[4].text = 'Unsatisfactory (<50%)'

# # Rubric data
# criteria = [
#     ("1. Problem Understanding (15%)", 
#      "Clear and complete problem understanding; appropriate assumptions stated",
#      "Mostly clear understanding with minor assumption issues",
#      "Some misunderstanding; vague assumptions",
#      "Major misunderstanding or problem not identified"),
    
#     ("2. Algorithm Design (20%)",
#      "Efficient, well-structured algorithm with logical flow",
#      "Mostly correct logic with minor flaws",
#      "Partially correct logic; inefficiencies present",
#      "Flawed or missing algorithm design"),
    
#     ("3. Code Implementation (25%)",
#      "Syntactically correct, runs flawlessly, meets all requirements",
#      "Minor syntax or logic errors, mostly functional",
#      "Compiles but has major runtime/logical issues",
#      "Fails to run or doesn't address problem"),
    
#     ("4. Code Readability (15%)",
#      "Well-commented, clean, modular code; proper naming conventions",
#      "Adequate formatting with few improvements needed",
#      "Poor structure; inconsistent naming; limited commenting",
#      "Disorganized and unreadable code"),
    
#     ("5. Testing & Output (15%)",
#      "Extensive test cases with correct results",
#      "Adequate testing with mostly correct outputs",
#      "Limited testing; some incorrect outputs",
#      "No testing or incorrect results")
# ]

# # Add rubric data
# for criterion in criteria:
#     row_cells = rubric.add_row().cells
#     for i in range(5):
#         row_cells[i].text = criterion[i]

# # Save document
# doc.save("Lab_Assignment_4_Solutions.docx")
