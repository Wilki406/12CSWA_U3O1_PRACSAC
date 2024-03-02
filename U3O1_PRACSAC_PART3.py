# Programmer: Benjamin Wilkinson
# Date: 22/02/2024
# Description: Calculation of Profits GUI

# imports
import csv
import PySimpleGUI as sg
import itertools

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
with open('Data/data.csv', 'r') as file:
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



for textbook, subject, seller, purchase, purchaser, sale, rating in zip(textbooks, subjects, seller, purchasePrices, purchaser, salePrices, rating):
    alldata.append([textbook, subject, seller, purchase, purchaser, sale, rating])

headers = ['textbook', 'subject', 'seller', 'purchased', 'purchaser', 'sale price', 'rating']
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
print(tabledata)
# while loop to enable button functionality.
while True:
    event, values = window.read()
    if event in (None, "Exit"):
        break

    if event == "Display All":
        window["table"].update(values=alldata)
        print(tabledata)

    if event == "Search":
        searchdata.clear()
        tabledata.clear()

        textbooktxt = str(values["txt_search1"])
        purchasertxt = str(values["txt_search2"])
        search_parts = [str(values["txt_search1"]), str(values["txt_search2"])]
        with open('Data/data.csv', 'r') as file:
            for row in file:
                if all([x in row for x in search_parts]):
                    searchdata.append(row)

        for value in searchdata:
            tabledata.append(value.strip().split(','))

        window["table"].update(values=tabledata)  # No need to skip headers in the update
        print()
# Close the window
window.close()
