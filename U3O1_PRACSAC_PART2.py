# Programmer: Benjamin Wilkinson
# Date: 22/02/2024
# Description: Calculation of Profits GUI

# imports
import csv
import PySimpleGUI as sg

def calculate_profits(purchase_prices, sale_prices):  # profit calculation function
    profits = []  # list of profits
    for purchase, sale in zip(purchase_prices, sale_prices): # zip function pairs numbers from 2 lists into a single list together
        if sale == 'NA': # if entries in sale prices column are NA it registers them as a float 0.0 so it can be used in operations
            sale = 0.0
        profit = float(sale) - float(purchase) # calculation to get profit
        rounded_profits = round(profit, 1) #round the profit to 1 decimal place
        profits.append(rounded_profits) #add the rounded profits to profits and then returns them
    return profits

def calculatetotalprofit(profits): # function to get total profit
    totalprofit = round(sum(profits)) # rounds the sum of profits list
    return totalprofit # returns the total profits

# Set the theme
sg.theme("BrightColors")

# Read data from CSV file
purchase_prices = []
sale_prices = []
textbooks = []
with open('Data/data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        purchase_prices.append(row['Purchase price'])
        sale_prices.append(row['Sale price'])
        textbooks.append(row['Textbook'])

# Calculate profits
profits = calculate_profits(purchase_prices, sale_prices)

# Prepare data for the table
data_for_table = [['textbook', 'purchased', 'sale price', 'profit']]
for textbook, purchase, sale, profit in zip(textbooks, purchase_prices, sale_prices, profits):
    data_for_table.append([textbook, purchase, sale, profit])

# Create the table
tbl1 = sg.Table(values=data_for_table[1:], headings=data_for_table[0],
                auto_size_columns=True,
                display_row_numbers=False,
                justification='left', key='table',
                enable_click_events=True, expand_y=True, expand_x=True)

layout = [[tbl1],
          [[sg.Button("Calculate Profit"), sg.Push(),sg.Button("Close")], sg.Text("Total Profit: ", key="TotalProfit")]]

# Create window
window = sg.Window("Prac Sac", layout, icon='', size=(800, 800), resizable=True)

while True:
    event, values = window.read()
    if event in (None, "Close"):
        break
    if event == "Calculate Profit":
        window["TotalProfit"].update(f"Total Profit:  {calculatetotalprofit(profits)}")

window.close()
