expected_input = "hello"  # Change this to the string you want to match

while True:
    user_input = input("Please enter '{0}': ".format(expected_input))
    if user_input == expected_input:
        break
    else:
        print("Sorry, that's not the right input. Please try again.")

# Continue with your code here, now that the input is correct
print("Great, you entered '{0}'!".format(expected_input))