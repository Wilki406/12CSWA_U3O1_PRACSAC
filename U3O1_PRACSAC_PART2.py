# Programmer: Benjamin Wilkinson
# Date: 22/02/2024
# Description: Calculation of Profits GUI

# imports
import csv
import PySimpleGUI as sg

# Function: Calculates the profit of each iteration in both lists and changes NA values to 0.0
# Input: Purchase Prices and Sale Prices
# Output: List of profits in same order
def calculateProfits(purchase_prices, sale_prices):  # profit calculation function
    # list of profits
    profits = []
    # zip function pairs numbers from 2 lists into a single list together
    for purchase, sale in zip(purchase_prices, sale_prices):
        # if entries in sale prices column are NA it registers them as a float 0.0 so it can be used in operations
        if sale == 'NA':
            # set NA values to 0.0
            sale = 0.0
        # calculation to get profit
        profit = float(sale) - float(purchase)
        # round the profit to 1 decimal place
        rounded_profits = round(profit, 1)
        # add the rounded profits to profits and then returns them
        profits.append(rounded_profits)
    #return the profits
    return profits

# Function: Calculates the total sum of profits
# Input: List of Profits
# Output: Total profit as a rounded integer
def calculatetotalprofit(profits):
    # rounds the sum of profits list
    totalprofit = round(sum(profits), 2)
    # returns the total profits
    return totalprofit

# Set the theme
sg.theme("BrightColors")


# Creating empty lists ready to be appended to
purchasePrices = []
salePrices = []
textbooks = []

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


# Calculate profits
profits = calculateProfits(purchasePrices, salePrices)

# the list that will house all the data columns has other lists inside of it
tabledata = [['textbook', 'purchased', 'sale price', 'profit']] ### DOUBLE SQUARE BRACKETS BECAUSE LIST INSIDE OF LIST
# for loop to merge each iteration in the 4 lists together and then append them to the list that will be put into the table
for textbook, purchase, sale, profit in zip(textbooks, purchasePrices, salePrices, profits):
    tabledata.append([textbook, purchase, sale, profit])

# Create the table seperate from the layout
tbl1 = sg.Table(values=tabledata[1:], headings=tabledata[0], ### [1:] to skip first row.
                                                             ### [0] to set the headers as the first list/row in the list
                auto_size_columns=True,
                display_row_numbers=False,
                justification='left', key='table',
                enable_click_events=True, expand_y=True, expand_x=True)

# Create the layout
layout = [[tbl1],
          [[sg.Button("Calculate Profit"), sg.Push(),sg.Button("Exit")], sg.Text("Total Profit: ", key="TotalProfit")]]

# Create window
window = sg.Window("Prac Sac", layout, icon='', size=(800, 800), resizable=True)

# while loop to enable button functionality.
while True:
    event, values = window.read()
    if event in (None, "Exit"):
        break
    if event == "Calculate Profit":
        window["TotalProfit"].update(f"Total Profit:  ${calculatetotalprofit(profits)}")

# Close the window
window.close()
