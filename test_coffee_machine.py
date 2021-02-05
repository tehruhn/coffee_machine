# Test basic functionality of the Coffee Machine Class, method by method

from coffee_machine import CoffeeMachine
import json

def test_basic_input():
    """Test to check basic input functionality of the class for simple
    test case.
    """

    # load data
    input_file = open("test_data/standard_input.json")
    data = json.load(input_file)

    # assign data to pass to coffee machine
    num_outlets = data['machine']['outlets']['count_n']
    beverages = data['machine']['beverages']
    total_items_qty = data['machine']['total_items_quantity']

    # instantiate coffee machine
    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
    expected_menu = ['hot_tea', 'black_tea', 'green_tea', 'hot_coffee']

    assert(CM.menu == expected_menu)


def test_checkFormat():

    # load data
    input_file = open("test_data/standard_input.json")
    data = json.load(input_file)

    # assign data to pass to coffee machine
    num_outlets = data['machine']['outlets']['count_n']
    beverages = data['machine']['beverages']
    total_items_qty = data['machine']['total_items_quantity']

    # instantiate coffee machine
    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
    [r]