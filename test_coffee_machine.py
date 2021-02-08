# Test basic functionality of the Coffee Machine Class, method by method

from coffee_machine import CoffeeMachine
import json
import pytest

def test_basic_CoffeeMachine():
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


def test_checkFormat_num_type():
    """ Test to check if non integer num outlets is handled correctly. 
    """

    # assign data to pass to coffee machine
    num_outlets = "hello"
    beverages = {}
    total_items_qty = {}

    with pytest.raises(ValueError, match="Number of outlets is not"):
        CM = CoffeeMachine(num_outlets, beverages, total_items_qty)


def test_checkFormat_bevs_type():
    """ Test to check if non dict beverages is handled correctly. 
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = "hello"
    total_items_qty = {}

    with pytest.raises(ValueError, match="Beverage list is not a dict."):
        CM = CoffeeMachine(num_outlets, beverages, total_items_qty)


def test_checkFormat_raw_mat_type():
    """ Test to check if non dict raw_material_qty is handled correctly. 
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {}
    total_items_qty = "hello"

    with pytest.raises(ValueError, match="Raw material list is not a dict."):
        CM = CoffeeMachine(num_outlets, beverages, total_items_qty)


def test_checkFormat_beverage_drink_not_str():
    """ Test to check if a drink name in beverages dict is not a string. 
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {1:{}}
    total_items_qty = {}

    with pytest.raises(ValueError, match="Name of drink in beverage list not"):
        CM = CoffeeMachine(num_outlets, beverages, total_items_qty)


def test_checkFormat_beverage_drink_ingredient_not_dict():
    """ Test to check if a drink's ingredients in beverages dict is
    not passed as a dict. 
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {"hot_tea":"hello"}
    total_items_qty = {}

    with pytest.raises(ValueError, match="Ingredients for drink in beverage"):
        CM = CoffeeMachine(num_outlets, beverages, total_items_qty)


def test_checkFormat_beverage_drink_ingredient_not_str():
    """ Test to check if a drink's ingredients (key) in beverages dict is
    not a string. 
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {"hot_tea":{1:52}}
    total_items_qty = {}

    with pytest.raises(ValueError, match="Name of ingredient for drink in"):
        CM = CoffeeMachine(num_outlets, beverages, total_items_qty)


def test_checkFormat_beverage_drink_ingredient_qty_not_int():
    """ Test to check if a drink's ingredients quantity (value) in 
    beverages dict is not an int. 
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {"hot_tea":{"milk": "hello"}}
    total_items_qty = {}

    with pytest.raises(ValueError, match="Required quantity of ingredient for"):
        CM = CoffeeMachine(num_outlets, beverages, total_items_qty)


def test_checkFormat_raw_mat_qty_ingredient_type():
    """ Test to check if a raw material quantity key in raw_material_qty 
    dict is not a string. 
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {}
    total_items_qty = {1:52}

    with pytest.raises(ValueError, match="Name of ingredient in raw material"):
        CM = CoffeeMachine(num_outlets, beverages, total_items_qty)


def test_checkFormat_raw_mat_qty_amount_type():
    """ Test to check if a raw material quantity value in raw_material_qty 
    dict is not an integer. 
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {}
    total_items_qty = {"milk":"hello"}

    with pytest.raises(ValueError, match="Quantity of ingredient in raw"):
        CM = CoffeeMachine(num_outlets, beverages, total_items_qty)


def test_checkSemantics_num_outlets():
    """ Test to check if number of outlets supplied makes semantic sense. 
    """

    # assign data to pass to coffee machine
    num_outlets = -1
    beverages = {}
    total_items_qty = {}

    with pytest.raises(ValueError, match="outlets must be more than 0"):
        CM = CoffeeMachine(num_outlets, beverages, total_items_qty)


def test_checkSemantics_beverages():
    """ Test to check if beverages ingredient quantity 
    supplied makes semantic sense. 
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {"hot_tea":{"milk":-1}}
    total_items_qty = {}

    with pytest.raises(ValueError, match="Quantity of ingredient in drink"):
        CM = CoffeeMachine(num_outlets, beverages, total_items_qty)


def test_checkSemantics_raw_material_qty():
    """ Test to check if raw materials ingredient quantity 
    supplied makes semantic sense. 
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {}
    total_items_qty = {"hot_tea":-1}

    with pytest.raises(ValueError, match="Quantity of a raw material cannot"):
        CM = CoffeeMachine(num_outlets, beverages, total_items_qty)


def test_refill_ingredient_type():
    """ Test to check if refill method works if ingredient given is not a 
    string.
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {}
    total_items_qty = {}

    with pytest.raises(ValueError, match="Ingredient is not a string."):
        CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
        CM.refill(1, 1)


def test_refill_qty_type():
    """ Test to check if refill method works if ingredient quantity given 
    is not an int.
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {}
    total_items_qty = {}

    with pytest.raises(ValueError, match="Quantity is not an integer."):
        CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
        CM.refill("milk", "hello")


def test_refill_unknown_ingredient():
    """ Test to check if refill method works if ingredient is not in 
    coffee machine.
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {}
    total_items_qty = {}

    with pytest.raises(ValueError, match="Ingredient not in coffee machine."):
        CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
        CM.refill("milk", 1)


def test_refill_positive_value():
    """ Test to check if refill method works if final value after 
    adding ingredient becomes negative.
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {}
    total_items_qty = {"milk":1}

    with pytest.raises(ValueError, match="Cannot add because final quantity"):
        CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
        CM.refill("milk", -2)


def test_refill_functionality():
    """ Test if the refill function works properly
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {}
    total_items_qty = {"milk":1}

    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
    CM.refill("milk", 1)

    assert CM.raw_material_qty["milk"] == 2


def test_canMakeDrink_drink_type():
    """ Test to see if canMakeDrink works when drink name is not a string.
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {}
    total_items_qty = {}

    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
    
    with pytest.raises(ValueError, match="Drink name is not a string"+
        " in canMake."):
        CM._CoffeeMachine__canMakeDrink(1)


def test_canMakeDrink_recipe_unkown():
    """ Test to see if canMakeDrink works when drink recipe is not known.
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {}
    total_items_qty = {}

    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
    
    with pytest.raises(ValueError, match="Drink recipe is not known"+
        " in canMake."):
        CM._CoffeeMachine__canMakeDrink("hot_tea")


def test_canMakeDrink_functionality_possible():
    """ Test to see if canMake works if drink is possible to make. 
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {"hot_tea":{"milk":1}}
    total_items_qty = {"milk":2}

    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
    
    assert CM._CoffeeMachine__canMakeDrink("hot_tea") == 1


def test_canMakeDrink_functionality_insufficient():
    """ Test to see if canMake works if drink is not possible to make
    because of insufficient ingredient. 
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {"hot_tea":{"milk":2}}
    total_items_qty = {"milk":1}

    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
    
    assert CM._CoffeeMachine__canMakeDrink("hot_tea") == 0


def test_canMakeDrink_functionality_impossible():
    """ Test to see if canMake works if drink is not possible to make
    because of non-existent ingredient. 
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {"hot_tea":{"cocoa":2}}
    total_items_qty = {"milk":1}

    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
    
    assert CM._CoffeeMachine__canMakeDrink("hot_tea") == -1


def test_pourDrink_functionality():
    """ Test to see if pourDrink works correctly. 
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {"hot_tea":{"milk":1}}
    total_items_qty = {"milk":2}

    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
    CM._CoffeeMachine__pourDrink("hot_tea")
    
    assert CM.raw_material_qty["milk"] == 1


def test_makeDrink_drink_type():
    """ Test to see if makeDrink works when drink name is not a string.
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {}
    total_items_qty = {}

    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
    
    with pytest.raises(ValueError, match="Drink name is not a string."):
        CM._CoffeeMachine__makeDrink(1, 1)


def test_makeDrink_recipe_unkown():
    """ Test to see if makeDrink works when drink recipe is not known.
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {}
    total_items_qty = {}

    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
    CM.running_threads = [1]

    with pytest.raises(ValueError, match="Drink recipe is not known."):
        CM._CoffeeMachine__makeDrink("hot_tea", 1)


def test_makeDrink_functionality_possible():
    """ Test to see if makeDrink works if drink is possible to make. 
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {"hot_tea":{"milk":1}}
    total_items_qty = {"milk":2}

    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
    CM.running_threads = [1]
    CM._CoffeeMachine__makeDrink("hot_tea", 1)

    assert CM.raw_material_qty["milk"] == 1


def test_makeDrink_functionality_insufficient():
    """ Test to see if makeDrink works if drink is not possible to make
    because of insufficient ingredient. 
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {"hot_tea":{"milk":2}}
    total_items_qty = {"milk":1}

    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
    CM.running_threads = [1]
    CM._CoffeeMachine__makeDrink("hot_tea", 1)

    assert CM.raw_material_qty["milk"] == 0


def test_makeDrink_functionality_impossible():
    """ Test to see if makeDrink works if drink is not possible to make
    because of non-existent ingredient. 
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {"hot_tea":{"cocoa":2}}
    total_items_qty = {"milk":1}

    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
    CM.running_threads = [1]
    CM._CoffeeMachine__makeDrink("hot_tea", 1)

    assert CM.raw_material_qty["milk"] == 1


def test_makeOrder_order_type():
    """ Test to see if makeOrder works with wrong order type.
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {"hot_tea":{"milk":1}}
    total_items_qty = {"milk":2}
    orders = {}

    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)

    with pytest.raises(ValueError, match="Orders were expected in a list."):
        CM.makeOrder(orders)


def test_makeOrder_order_drink_type():
    """ Test to see if makeOrder works with wrong drink type in order.
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {"hot_tea":{"milk":1}}
    total_items_qty = {"milk":2}
    orders = [1]

    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)

    with pytest.raises(ValueError, match="Drink name in order is"):
        CM.makeOrder(orders)


def test_makeOrder_order_unknown_drink():
    """ Test to see if makeOrder works with wrong drink type in order.
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {"hot_tea":{"milk":1}}
    total_items_qty = {"milk":2}
    orders = ["coffee"]

    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)

    with pytest.raises(ValueError, match="for ordered drink is not known."):
        CM.makeOrder(orders)


def test_makeOrder_zero_len():
    """ Test to see if makeOrder works with zero length order.
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {"hot_tea":{"milk":1}}
    total_items_qty = {"milk":2}
    orders = []

    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
    CM.makeOrder(orders)

    assert CM.raw_material_qty["milk"] == 2


def test_makeOrder_functionality():
    """ Test to see if makeOrder works.
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {"hot_tea":{"milk":1}}
    total_items_qty = {"milk":2}
    orders = ["hot_tea"]

    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
    CM.makeOrder(orders)

    assert CM.raw_material_qty["milk"] == 1


def test_makeOrder_functionality_str_input():
    """ Test to see if makeOrder works for single string input.
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {"hot_tea":{"milk":1}}
    total_items_qty = {"milk":2}
    orders = "hot_tea"

    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
    CM.makeOrder(orders)

    assert CM.raw_material_qty["milk"] == 1


def test_makeOrder_functionality_multiple_orders():
    """ Test to see if makeOrder works for multiple orders.
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {"hot_tea":{"milk":1}}
    total_items_qty = {"milk":2}
    orders = ["hot_tea", "hot_tea"]

    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
    CM.makeOrder(orders)

    assert CM.raw_material_qty["milk"] == 0


def test_makeOrder_functionality_multiple_orders_with_wait():
    """ Test to see if makeOrder works for multiple orders.
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {"hot_tea":{"milk":1}}
    total_items_qty = {"milk":2}
    orders = ["hot_tea", "hot_tea", "hot_tea", "hot_tea", 
    "hot_tea", "hot_tea"]

    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)
    CM.makeOrder(orders)

    assert CM.raw_material_qty["milk"] == 0


def test_returnIngredientLevel():
    """ Test to see if returning ingredient level works.
    """

    # assign data to pass to coffee machine
    num_outlets = 1
    beverages = {"hot_tea":{"milk":1}}
    total_items_qty = {"milk":2}

    CM = CoffeeMachine(num_outlets, beverages, total_items_qty)

    assert CM.returnIngredientLevel() == total_items_qty


