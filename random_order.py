import json
import random

random.seed(696969)

# load data from the sample JSON file
input_file = open("test_data/standard_input.json")
data = json.load(input_file)

# assign data to lists and dicts pass to coffee machine
beverages = data['machine']['beverages']
menu = list(beverages.keys())

# Number ot orders to be generated
NUM_ORDERS = 100
n = len(menu) - 1

# write to file
filename = "test_data/temp_orders.txt"
f = open(filename, "a")

for i in range(NUM_ORDERS):
	idx = random.randint(0, n)
	f.write(menu[idx])
	f.write("\n")

f.close()
