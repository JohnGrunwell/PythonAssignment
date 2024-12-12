from time import sleep
import pandas as pd  # import panda using value pd to access the framework
df = pd.read_csv("cats_dataset.csv")  # assign df to the csv to read from.
# Store the headers eg. breed, colour etc in strings for easy access.
HeaderBreed = str("Breed")
HeaderColor = str("Color")
HeaderAge = str("Age (Years)")
HeaderWeight = str("Weight (kg)")
HeaderGender = str("Gender")
# Provide a list of options that can be done by the user
Options = ["1-Search Row", "2-Search Breed", "3-Check Average Age", "4-Check Average Weight",
           "5-Search Colour","6-Search Gender", "7-Show All Data", "8-Exit"] # Multi line array of strings
# Necessary global variable to allow loops, ints and strings to be used within functions where needed.
LoopForCorrectInput = bool(True) # Keeps the correct input loop going until there is a proper user input
LoopForConfirmedInput = bool(True) # Keeps the loop going for confirming an input.
SelectedOption = int(0) # Stores input from the user, so that we can associate it with a function call
ConfirmInput = str("Empty") # This gets updated through the code y or n, mainly used on exit to confirm if the user wants to exit or not

def PrintOptions() -> int:
    for i in Options:
        print(f"{i}") # Print each option available in the Options array
    return int(input("\nPlease enter a option number: ")) - 1 # Subtracting 1 to ensure outputs can start from 0

def InvalidInput() -> None:
    print("Invalid input! Please enter a valid option.\n") # Simple error message

def Confirm_Input() -> str:
    return str(input(f"You are about to close the program, please confirm (Y/N)? \n")) # Return the input by the user for confirmation checking.

def ShowMenu() -> None:
    global SelectedOption # Access to the SelectedOption variable.
    while LoopForCorrectInput:
        try: # Basically attempts something in this case it attempts to print the options menu.
            # Allow the option to enter the number corresponding to the menu.
            SelectedOption = PrintOptions()
            break  # Exit loop if input is valid
        except ValueError:
            InvalidInput()

def ConfirmSelection() -> None:
    global SelectedOption
    global ConfirmInput
    while LoopForConfirmedInput:
        try:
            ConfirmInput = Confirm_Input().upper() # Ensures that we are checking the upper case of the user input to check correctly
            if ConfirmInput == str("Y"): # If user typed y remember we added .upper in the function so it would have set Y, if so, allow continuation of action
                break  # Exit loop if the user wishes to continue
            elif ConfirmInput == str("N"): # If the user did not want to exit we print the options again and then break out the loop
                SelectedOption = PrintOptions()
                ConfirmInput = Confirm_Input().upper()
                break  # Exit loop if a valid correct option has been picked
        except ValueError:
            InvalidInput() #Output an error if the input was not Y or N then re run the loop from the begining

def PrintRow(RowID: int) -> None:
    print(f"{df.loc[RowID]}\n") # Prints a specific row, which will be passed through to this function
    return

def PrintHeader() -> None:
    print(f"{df}\n") # Outputs the entire data frame "df" for which ever value was pushed through to this function via Header
    return

def AverageAge() -> None:
    print(f"The average age is {df[HeaderAge].aggregate('mean')}\n")
    # Takes the entire data frame and calls aggregate allow us to specify which aggregation function we would like to use on the given header
    # In this function the columns relating to Age (Years)
    return

def AverageWeight() -> None:
    print(f"The average weight is {df[HeaderWeight].aggregate('mean')}\n") # Same as above except with weight
    return

def ExitProgram() -> None:
    print("Exiting program...\n".upper())
    sleep(float(2.0))
    exit()

def ShowIndex() -> None:
    while True:
        MinR = int(1) # Sets minimum row to 1, since some users may not know rows start from 0
        MaxR = int(len(df)) # Sets a max row value based on how many rows there is -> len() = length of data/array/frame but does not start from 0
        try:
            r = int(input("Enter a row number: ")) # Sets r to the users input number
            if r <= MaxR and r >= MinR: # If the number entered is lower than max rows and higher than min rows proceed to the following block
                PrintRow(r - 1) # And is used as both can and must be true before we can print the row, and since rows start from 0 we need to subtract 1
                break
            elif r < MinR or r > MaxR: # If the number entered is lower then min or higher than max cannot use "and" here as its impossible for a number to be both lower than min while also higher than max
                print(f"Row number {r} does not exist, please try a different row number.\nEnter a row number between {MinR} and {MaxR}\n")
                # Since the inputted number is out of bounds of the array, instead of crashing, we use except to output a error
        except ValueError :
            print("Invalid input! Please enter a valid row number.\n")
    return

def ShowFiltered(NewHeader: str) -> None:
    print(f"The following {NewHeader} are available:\n") # Using the entered NewHeader we can use that to label the section before printing possible options
    PrintUnique(NewHeader) # Informs the user which headers they can pick from
    c = str(input(f'Enter a {NewHeader}: ')) # Asks the user to enter one of the printed categories above
    if c.upper() in df[NewHeader].str.upper().str.strip().values: # Checks, if the entered data assigned to "c" is within the values of the columns in the data frame
        ShowFilteredByVar(NewHeader, c) # Since we now know that c is definitely somewhere in the headers, we can call a function to find it
        return
    elif c not in df[NewHeader].str.upper().str.strip().values: #If c is not found in the columns within the data frame values then we can inform the user that no results was found
        print(f"No results found for {c}\nPlease use one of the following:\n")
        PrintUnique(NewHeader) # Prints all the columns of the data frame that match the "NewHeader", to remind the user of the choices they have

def PrintUnique(NewHeader: str) -> None :
    x = int(0)
    HeaderList = str("") # Creates and empty string, so that we have something to fill into it and output to the user
    for i in df[NewHeader].unique(): # Here we loop through all the unique values that match the column and assigns the iteration to "i"
        x += int(1) # Here we track the index that we are on by ints instead of something like Breeds, or Colours
        HeaderList += f"{i}, " # Here we use += to concatenate the string, we add onto itself the new interation
        if x%16 == 1: # If the current iteration index has a remainder then we add a new line to keep the list compact and not too long in either direction
            HeaderList += f"\n"

    print(f"{HeaderList}\n") # Once the loop has finished then we print the entire list to the user

def ShowFilteredByVar(SearchHeader: str, SearchTerm: str) -> None:
    # Here we look for a data frame that is a data frame itself that matches the SearchHeader e.g. df[df[Colour] == Red]
    # We convert conditions to upper to ensure we get a match even if the cases are not correct, resulting in a none case-sensitive search
    # Furthermore we also remove any leading, and trailing whitespaces using strip()
    print(f"{df[df[SearchHeader].str.upper().str.strip().values == SearchTerm.upper()]}\n") # Here we look for a data frame that is a data frame itself that matches the SearchHeader e.g. df[df[Colour] == Red]

def RunOption(Option: int) -> None:
    if Option == 0:
        print(f"Searching Index...".upper())
        ShowIndex()
    elif Option == 1:
        print(f"Searching Dataset By Breed...".upper())
        ShowFiltered(HeaderBreed)
    elif Option == 2:
        print(f"Average Age Of All Cats...".upper())
        AverageAge()
    elif Option == 3:
        print(f"Average Weight Of All Cats...".upper())
        AverageWeight()
    elif Option == 4:
        print(f"Searching Dataset By Color...".upper())
        ShowFiltered(HeaderColor)
    elif Option == 5:
        print(f"Searching Dataset By Gender..".upper())
        ShowFiltered(HeaderGender)
    elif Option == 6:
        print(f"Displaying all entries..".upper())
        PrintHeader()
    elif Option == 7:
        ExitProgram()
    else:
        print("Invalid option!")
    return

def Main(): # This is just to set out a main function that will loop definitely until the user exits the program.
    print(f"Welcome to the Cat Searcher Program!\n".upper())
    print(f"Please select an option from the menu below:\n")
    ShowMenu()
    if SelectedOption == 7: # Checks if the selected option was for exiting the program, if so, asks the user to confirm
        ConfirmSelection() # Checks the input and compares it to Y or N, so the program can decide to either keep running or exit
    RunOption(SelectedOption) # Prints out all the option onto the screen so the user can visibly see what they can do with the application
    print(input("\n Press Enter To Continue...\n"))# After we carry out a task, such as searching for a breed for example
    # We need to prevent the program going straight back to the start so the user can have time to think and read the data
    # Once the user is done with the information on screen they can press enter to end the Main() function.

while True : # Ensures Main() runs indefinitely, since one program loop ends with "Press Enter To Continue" the program would then normally end and close
    # to prevent this closure after just 1 task, we set the main function on an infinite loop, once all the code has run, it will run it again
    # this allows the user to decide when to exit rather than immediately exiting after 1 application feature has run.
    Main()