# Programmer: Benjamin Wilkinson
# Date: 04/03/2024
# Description: Textbook GUI search and rate

# imports
import csv
import PySimpleGUI as sg

sg.theme("BrightColors")  # Set the theme

# Creating empty lists ready to be appended to
purchasePrices = []
salePrices = []
textbooks = []
subjects = []
seller = []
purchaser = []
rating = []

# Creating empty lists related to searching ready to be appended to
searchData = []
searchParts = []

# Creating empty lists for displaying data on to GUI
tableData = []
allData = []

isSearched = True  # this boolean will be used to check if searched data is currently presented on the GUI

with open('newdata.csv') as file:  # Read data from CSV file
    reader = csv.DictReader(file)  # setting the reader to be a csv dictionary reader

    for col in reader:  # going through each column
        # Taking all the data in each column with the corresponding name and appending it to the list
        purchasePrices.append(col['Purchase price'])
        salePrices.append(col['Sale price'])
        textbooks.append(col['Textbook'])
        subjects.append(col['Subject'])
        seller.append(col['Seller'])
        purchaser.append(col['Purchaser'])
        rating.append(col['Rating'])

# Append the all data into list of lists
for textbook, subject, seller, purchase, purchaser, sale, rating in zip(textbooks, subjects, seller, purchasePrices, purchaser, salePrices, rating):
    allData.append([textbook, subject, seller, purchase, purchaser, sale, rating])

headers = ['Textbook', 'Subject', 'Seller', 'Purchase price', 'Purchaser', 'Sale price',
           'Rating']  # create list of CORRECTLY named headers

# Create the table separate from the layout
tbl1 = sg.Table(values=allData, headings=headers,
                auto_size_columns=True,
                display_row_numbers=False,
                justification='left', key='table',
                enable_click_events=True, expand_y=False, expand_x=True)

# Create the layout
layout = [[tbl1],
          [[sg.Button("Display All"), sg.Push(), sg.Button("Exit"), ],
           [sg.Text("Rate a textbook: ")],
           [sg.Text("Textbook: "), sg.Input(key="txt_search1")],
           [sg.Text("Purchaser: "), sg.Input(key="txt_search2")],
           [sg.Button("Search")],
           [sg.Text("New Rating (1-5): "), sg.Input(key="txt_rating")],
           [sg.Button("Rate & Save", key='save')]]]

window = sg.Window("Prac Sac", layout, icon='', size=(1200, 400), resizable=True)  # Create window

while True:  # while loop to enable button functionality.
    event, values = window.read()

    # if statement to check if EXIT button has been pressed if so the loop breaks and the window is exited
    if event in (None, "Exit"):
        break

    # if statement to check if display all button is pressed and if so the table is updated with a variable that is the list of lists of all data from the CSV.
    if event == "Display All":
        window["table"].update(values=allData)
        isSearched = False

    if event == "Search":  # if statement to check if search button is pressed.

        searchData.clear()  # Search data list is cleared of all data inside
        tableData.clear()   # Table data is cleared of all data inside
                            # Table data is the list of lists of just searched data

        # set strings as data entered into text boxes
        textbooktxt = str(values["txt_search1"].lower)
        purchasertxt = str(values["txt_search2"].lower)
        searchParts = [str(values["txt_search1"]),str(values["txt_search2"])]  # create list of both text boxes entered data

        with open('newdata.csv','r') as file:  # Open dataset in read mode to go through each row to find both text
            for row in file:
                if all([x in row for x in searchParts]):  # checks whether each element (x) in search_parts is present in the iterable row
                    searchData.append(row)  # adds that row to search data

        for value in searchData:
            tableData.append(value.strip().split(','))  # .split splits the modified string (after stripping) into a list of substrings using the comma
                                                        # .strip removes any leading and trailing whitespace characters

        window["table"].update(values=tableData)  # updates table with searched data
        isSearched = True

    if event == "save":  # if save button is pressed
        allowedvalues = ['1', '2', '3', '4', '5']  # list of values that you are allowed

        # set strings as data entered into text boxes
        selected_textbook = str(values["txt_search1"])
        selected_purchaser = str(values["txt_search2"])
        enteredRating = str(values["txt_rating"])

        if enteredRating not in allowedvalues:  # check to see if the entered rating is not in the allowed values list
            sg.popup_error("Please rate 1-5")  # give the user an error saying to stop being dumb
            continue  # restart the loop to belay the rating

        for i, row in enumerate(allData):  #
            if selected_textbook in row[0] and selected_purchaser in row[4]:  # if statement to check if the selected book and purchaser is in the same row
                allData[i][-1] = enteredRating  # if it is in the same row ([i]) it using ([-1]) selects the last column of the row and sets it to the rating

        with open('newdata.csv', 'w', newline='') as file:  # open / make the new csv file in write mode
            # newline='' ensures that the file object does not perform any newline translation

            writer = csv.writer(file)  # set the csv writer
            writer.writerow(headers)  # write the headings as the CORRECT headings
            writer.writerows(allData)  # write the data to the new csv file

        if isSearched == True:  # THIS IS TO CHECK IF THE GUI IS SHOWING SEARCHED DATA CURRENTLY
            searchData.clear()  # Search data list is cleared of all data inside
            tableData.clear()   # Table data is cleared of all data inside
                                # Table data is the list of lists of just searched data

            searchParts = [str(values["txt_search1"]),str(values["txt_search2"])]  # create list of both text boxes entered data

            with open('newdata.csv','r') as file:  # Open dataset in read mode to go through each row to find both text
                for row in file:
                    if all([x in row for x in searchParts]):  # checks whether each element (x) in search_parts is present in the iterable row
                        searchData.append(row)  # adds that row to search data

            for value in searchData:
                tableData.append(value.strip().split(','))  # .split splits the modified string (after stripping) into a list of substrings using the comma
                                                            # .strip removes any leading and trailing whitespace characters

            window["table"].update(values=tableData)  # updates table with searched data

        else:
            window["table"].update(values=allData)  # updates table with searched data


window.close() # Close the window
