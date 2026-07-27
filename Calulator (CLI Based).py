def calculator():
    """A simple CLI-based calculator that performs basic arithmetic operations."""
    
    while True:
        try:
            # Get user input
            num1 = float(input("\nEnter the first number: "))
            num2 = float(input("Enter the second number: "))
            
            # Display operation menu
            print("\nSelect operation:")  
            print("1. Add") 
            print("2. Subtract")
            print("3. Multiply")
            print("4. Divide")
            choice = input("Enter choice (1/2/3/4): ")
            
            # Perform calculation based on choice
            if choice == '1':
                result = num1 + num2
                print(f"{num1} + {num2} = {result}")
            elif choice == '2':
                result = num1 - num2
                print(f"{num1} - {num2} = {result}")
            elif choice == '3':
                result = num1 * num2
                print(f"{num1} * {num2} = {result}")
            elif choice == '4':
                if num2 != 0:
                    result = num1 / num2
                    print(f"{num1} / {num2} = {result}")
                else:
                    print("Error! Division by zero. Please enter a non-zero second number.")
            else:
                print("Invalid input! Please enter a choice between 1 and 4.")
                continue
            
            # Ask if user wants to continue
            another_calculation = input("\nDo you want to perform another calculation? (yes/no): ").lower()
            if another_calculation != "yes":
                print("Thank you for using the calculator!")
                break
                
        except ValueError:
            print("Invalid input! Please enter valid numbers.")
            continue

# Run the calculator
if __name__ == "__main__":
    calculator()