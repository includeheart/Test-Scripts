first_value = int(input("Enter the first number: "))
second_value = int(input("Enter the second number: "))
operation = input("Enter the operation (+ or -): ")
if operation == "+":
    result = first_value + second_value
    print("The result is:", result)
elif operation == "-":
    result = first_value - second_value
    print("The result is:", result)
else:
    print("Invalid operation.")