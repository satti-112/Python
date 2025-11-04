# Multipurpose Converter Program

# Function for temperature conversions
def temperature_converter():
    print("\nTemperature Converter")
    print("1. Celsius to Fahrenheit")
    print("2. Fahrenheit to Celsius")
    print("3. Celsius to Kelvin")
    print("4. Kelvin to Celsius")
    print("5. Fahrenheit to Kelvin")
    print("6. Kelvin to Fahrenheit")
    choice = input("Select conversion (1-6): ")
    if choice == '1':
        # Celsius to Fahrenheit
        c = float(input("Enter Celsius: "))
        f = (c * 9/5) + 32
        print(f"{c}°C = {f}°F")
    elif choice == '2':
        # Fahrenheit to Celsius
        f = float(input("Enter Fahrenheit: "))

        c = (f - 32) * 5/9
        print(f"{f}°F = {c}°C")

    elif choice == '3':
        # Celsius to Kelvin
        c = float(input("Enter Celsius: "))
        k = c + 273.15
        print(f"{c}°C = {k}K")
    elif choice == '4':
        # Kelvin to Celsius
        k = float(input("Enter Kelvin: "))
        c = k - 273.15
        print(f"{k}K = {c}°C")
    elif choice == '5':
        # Fahrenheit to Kelvin
        f = float(input("Enter Fahrenheit: "))
        k = (f - 32) * 5/9 + 273.15
        print(f"{f}°F = {k}K")
    elif choice == '6':
        # Kelvin to Fahrenheit
        k = float(input("Enter Kelvin: "))
        f = (k - 273.15) * 9/5 + 32
        print(f"{k}K = {f}°F")
    else:
        print("Invalid choice.")

# Function for length conversions
def length_converter():
    print("\nLength Converter")
    print("1. Kilometers to Meters")
    print("2. Meters to Centimeters")
    print("3. Centimeters to Inches")
    print("4. Inches to Feet")
    print("5. Feet to Kilometers")
    print("6. Meters to Kilometers")
    print("7. Centimeters to Meters")
    print("8. Inches to Centimeters")
    print("9. Feet to Inches")
    print("10. Kilometers to Feet")
    choice = input("Select conversion (1-10): ")
    if choice == '1':
        # Kilometers to Meters
        km = float(input("Enter kilometers: "))
        m = km * 1000
        print(f"{km} km = {m} m")
    elif choice == '2':
        # Meters to Centimeters
        m = float(input("Enter meters: "))
        cm = m * 100
        print(f"{m} m = {cm} cm")
    elif choice == '3':
        # Centimeters to Inches
        cm = float(input("Enter centimeters: "))
        inch = cm / 2.54
        print(f"{cm} cm = {inch} inches")
    elif choice == '4':
        # Inches to Feet
        inch = float(input("Enter inches: "))
        ft = inch / 12
        print(f"{inch} inches = {ft} feet")
    elif choice == '5':
        # Feet to Kilometers
        ft = float(input("Enter feet: "))
       
        km = ft * 0.0003048
        print(f"{ft} feet = {km} km")
    elif choice== '6' :
        # Meters to Kilometers
        m = float(input("Enter meters: "))
        km = m / 1000
        print(f"{m} m = {km} km")  

    elif choice == '7':
        # Centimeters to Meters
        cm = float(input("Enter centimeters: "))
        m = cm / 100
        print(f"{cm} cm = {m} m")
    elif choice == '8':
        # Inches to Centimeters
        inch = float(input("Enter inches: "))
        cm = inch * 2.54
        print(f"{inch} inches = {cm} cm")
    elif choice == '9':
        # Feet to Inches
        ft = float(input("Enter feet: "))
        inch = ft * 12
        print(f"{ft} feet = {inch} inches")
    elif choice == '10':
        # Kilometers to Feet
        km = float(input("Enter kilometers: "))
        ft = km * 3280.84
        print(f"{km} km = {ft} feet")
    else:
        print("Invalid choice.")

# Function for weight conversions
def weight_converter():
    print("\nWeight Converter")
    print("1. Kilograms to Pounds")
    print("2. Pounds to Kilograms")
    print("3. Kilograms to Grams")
    print("4. Grams to Kilograms")
    print("5. Pounds to Grams")
    print("6. Grams to Pounds")
    choice = input("Select conversion (1-6): ")
    if choice == '1':
        # Kilograms to Pounds
        kg = float(input("Enter kilograms: "))
       
        lb = kg * 2.20462
        print(f"{kg} kg = {lb} lbs")
    elif choice == '2':
        # Pounds to Kilograms
        lb = float(input("Enter pounds: "))
       
        kg = lb / 2.20462
        print(f"{lb} lbs = {kg} kg")
    elif choice == '3':
        # Kilograms to Grams
        kg = float(input("Enter kilograms: "))
       
        g = kg * 1000
        print(f"{kg} kg = {g} g")
    elif choice == '4':
        # Grams to Kilograms
        g = float(input("Enter grams: "))
      
        kg = g / 1000
        print(f"{g} g = {kg} kg")
    elif choice == '5':
        # Pounds to Grams
        lb = float(input("Enter pounds: "))
       
        g = lb * 453.592
        print(f"{lb} lbs = {g} g")
    elif choice == '6':
        # Grams to Pounds
        g = float(input("Enter grams: "))
      
        lb = g / 453.592
        print(f"{g} g = {lb} lbs")
    else:
        print("Invalid choice.")

def speed_converter():
    print("\nSpeed Converter")
    print("1. Kilometers/hour to Meters/second")
    print("2. Meters/second to Kilometers/hour")
    print("3. Kilometers/hour to Miles/hour")
    print("4. Miles/hour to Kilometers/hour")
    print("5. Meters/second to Miles/hour")
    print("6. Miles/hour to Meters/second")
    choice = input("Select conversion (1-6): ")
    if choice == '1':
        # Kilometers/hour to Meters/second
        kmh = float(input("Enter km/h: "))
      
        ms = kmh / 3.6
        print(f"{kmh} km/h = {ms} m/s")
    elif choice == '2':
        # Meters/second to Kilometers/hour
        ms = float(input("Enter m/s: "))
      
        kmh = ms * 3.6
        print(f"{ms} m/s = {kmh} km/h")
    elif choice == '3':
        # Kilometers/hour to Miles/hour
        kmh = float(input("Enter km/h: "))
        
        mph = kmh * 0.621371
        print(f"{kmh} km/h = {mph} mph")
    elif choice == '4':
        # Miles/hour to Kilometers/hour
        mph = float(input("Enter mph: "))
       
        kmh = mph / 0.621371
        print(f"{mph} mph = {kmh} km/h")
    elif choice == '5':
        # Meters/second to Miles/hour
        ms = float(input("Enter m/s: "))
       
        mph = ms * 2.23694
        print(f"{ms} m/s = {mph} mph")
    elif choice == '6':
        # Miles/hour to Meters/second
        mph = float(input("Enter mph: "))
        
        ms = mph / 2.23694
        print(f"{mph} mph = {ms} m/s")
    else:
        print("Invalid choice.")

# Main menu function to select converter module
def main_menu():
    while True:
        print("\n--- Multipurpose Converter ---")
        print("1. Temperature Converter")
        print("2. Length Converter")
        print("3. Weight Converter")
        print("4. Speed Converter")
        print("5. Exit")
        choice = input("Select module (1-5): ")
        if choice == '1':
            temperature_converter()
        elif choice == '2':
            length_converter()
        elif choice == '3':
            weight_converter()
        elif choice == '4':
            speed_converter()
        elif choice == '5':
            print("Exiting the converter. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
main_menu()            