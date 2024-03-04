# Programmer: Benjamin Wilkinson
# Date: 04/03/2024
# Description: Textbook GUI search and rate

# imports
import csv
import PySimpleGUI as sg

# Set the theme
sg.theme("BrightColors")


# Creating empty lists ready to be appended to
purchasePrices = []
salePrices = []
textbooks = []
subjects = []
seller = []
purchaser = []
rating = []

searchdata = []
search_parts = []

tabledata = []
alldata = []


# Read data from CSV file
with open('Data/newdata.csv') as file:
    # setting the reader to be a csv dictionary reader
    reader = csv.DictReader(file)
    # going through each column
    for col in reader:
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
    alldata.append([textbook, subject, seller, purchase, purchaser, sale, rating])


# create list of CORRECTLY named headers
headers = ['Textbook', 'Subject', 'Seller', 'Purchase price', 'Purchaser', 'Sale price', 'Rating']
# Create the table separate from the layout
tbl1 = sg.Table(values=alldata, headings=headers,
                auto_size_columns=True,
                display_row_numbers=False,
                justification='left', key='table',
                enable_click_events=True, expand_y=False, expand_x=True)

# Create the layout
layout = [[tbl1],
          [[sg.Button("Display All"), sg.Push(), sg.Button("Exit"),],
           [sg.Text("Rate a textbook: ")],
           [sg.Text("Textbook: "), sg.Input(key="txt_search1")],
           [sg.Text("Purchaser: "), sg.Input(key="txt_search2")],
           [sg.Button("Search")],
           [sg.Text("New Rating (1-5): "), sg.Input(key="txt_rating")],
           [sg.Button("Rate & Save", key='save')]]]



# Create window
window = sg.Window("Prac Sac", layout, icon='', size=(1200, 400), resizable=True)

# while loop to enable button functionality.
while True:
    event, values = window.read()

    # if statement to check if EXIT button has been pressed if so the loop breaks and the window is exited
    if event in (None, "Exit"):
        break

    # if statement to check if display all button is pressed and if so the table is updated with a variable that is the list of lists of all data from the CSV.
    if event == "Display All":
        window["table"].update(values=alldata)
    
    # if statement to check if search button is pressed.
    if event == "Search":
        # Search data list is cleared of all data inside
        searchdata.clear()
        # Table data is cleared of all data inside
        # Table data is the list of lists of just searched data
        tabledata.clear()

        # set strings as entered data into text boxes
        textbooktxt = str(values["txt_search1"])
        purchasertxt = str(values["txt_search2"])
        #create list of both text boxes entered data
        search_parts = [str(values["txt_search1"]), str(values["txt_search2"])]
        # Open dataset in read mode to go through each row to find both text
        with open('Data/newdata.csv', 'r') as file:
            for row in file:
                if all([x in row for x in search_parts]):
                    searchdata.append(row)

        for value in searchdata:
            tabledata.append(value.strip().split(','))

        window["table"].update(values=tabledata)
        print()

    if event == "save":
        allowedvalues = ['1','2','3','4','5']
        selected_textbook = str(values["txt_search1"])
        selected_purchaser = str(values["txt_search2"])
        enteredRating = str(values["txt_rating"])
        if enteredRating not in allowedvalues:
            sg.popup_error("Please rate 1-5")
            continue

        for i, row in enumerate(alldata):
            print(row[0])
            if selected_textbook in row[0] and selected_purchaser in row[4]:
                alldata[i][-1] = enteredRating

        with open('Data/newdata.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(alldata)

        # for alldata in alldata:

        print(alldata)
        window["table"].update(values=alldata)


# Close the window
window.close()
