email = input("Enter your email: ")
password = input("Enter your password: ")

correct_email = "abc@gmail.com"
correct_password = "abc"

if email == correct_email and password == correct_password:
    print("User is logged in")
elif email == correct_email and password != correct_password:
    print("Incorrect password")
elif email != correct_email and password == correct_password:
    print("Incorrect email")

else:
    print("Both email and password are incorrect")
