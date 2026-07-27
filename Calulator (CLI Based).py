Num1 = float(input("Enter the first number: "))
Num2 = float(input("Enter the second number: "))
print("Select operation:")  
print("1. Add") 
print("2. Subtract")
print("3. Multiply")
print("4. Divide")
choice = input("Enter choice (1/2/3/4): ")

if choice == '1':
    print(Num1, "+", Num2, "=", Num1 + Num2)
elif choice == '2':
    print(Num1, "-", Num2, "=", Num1 - Num2)
elif choice == '3':
    print(Num1, "*", Num2, "=", Num1 * Num2)
elif choice == '4':
    if Num2 != 0:
        print(Num1, "/", Num2, "=", Num1 / Num2)
    else:
        print("Error! Division by zero.", "Please enter a non-zero second number.", ZeroDivisionError)  
else:
    print("Invalid input")

    print("Do you want to perform another calculation? (yes/no)")
    another_calculation = input().lower()
    if another_calculation == "yes":
        # Restart the calculation process
        pass
    else:
        print("Thank you for using the calculator!")