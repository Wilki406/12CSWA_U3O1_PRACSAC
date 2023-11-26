# pseudocode calculation function
def calculate_calvalue(age, value):
    depreciation = value * 0.2 * age
    if depreciation > value:
        return 0
    return value - depreciation


# main function
def main():
    # pre-defining data types and dictionary
    books = {}
    entry_number = 1
    total_calvalue = 0

    # while loop for entering multiple textbooks
    while True:
        # getting input and storing in dictionary
        age = int(input(f"How old is the textbook (in years)? "))
        value = float(input(f"How much did you pay for the textbook? "))
        # using cal function with new data
        calvalue = calculate_calvalue(age, value)
        # calculating collection worth
        total_calvalue += calvalue

        # dictionary formatting
        books[entry_number] = {
            'age': age,
            'value': value,
            'calvalue': calvalue
        }

        # printing calculated info
        print("\n")
        print(f"This textbook is worth ${calvalue}0")
        print(f"The collection so far is worth ${total_calvalue}0\n")

        # + 1 so new line in dictionary
        entry_number += 1

        # ask if the loop should continue or not
        another_entry = input("Do you wish to enter another textbook? (y or n): ").lower()
        if another_entry != 'y':
            break


if __name__ == "__main__":
    main()
