from coffee_machine import CoffeeMachine
import json

# load data from the sample JSON file
input_file = open("test_data/standard_input.json")
data = json.load(input_file)

# assign data to lists and dicts pass to coffee machine
num_outlets = data['machine']['outlets']['count_n']
beverages = data['machine']['beverages']
total_items_qty = data['machine']['total_items_quantity']

# orders = ['hot_tea', 'black_tea', 'green_tea', 'hot_coffee']
# orders = ['hot_tea', 'hot_tea','hot_tea', 'hot_tea']

# Read orders from file
filename = "test_data/temp_orders.txt"
f = open(filename, "r")
orders = f.readlines()

# Remove line breaks from orders
for i in range(len(orders)):
    orders[i] = orders[i][:-1]

# Instantiate the Coffee Machine
CM = CoffeeMachine(num_outlets, beverages, total_items_qty)

# Check the menu of the coffee machine
menu = CM.menu

print()
print("-------------------------------------------------")  
print("The drinks available in the machine are : ")
print(menu)

print()
print("-------------------------------------------------")  

# See which drinks can be made concurrently from the menu

# for element in menu:
#   CM.makeDrink(element)

CM.makeOrder(orders)

print("-------------------------------------------------")
print()