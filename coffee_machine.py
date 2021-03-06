# This class simulates a Coffee Machine in Python for solution to
# the problem posed by HumIt as a part of their interview process.

import threading
import time

class CoffeeMachine:
    """ Class for simulating a coffee machine. Stores inherent attributes
    of the coffee machine like recipes, number of outlets, and quantity of
    raw material.

    Attributes
    ----------

    num_outlets : int
        Number of outlets in the coffee machine.
    
    beverages : dict
        Recipes for the various drinks the machine makes.

    raw_material_qty : dict
        Stores quantity of raw material in the coffee machine.

    menu : list
        Stores names of all drinks that can be made by the machine

    """


    def __init__(self, num_outlets=1, beverages={}, raw_material_qty={}):
        """Initialized the CoffeeMachine class.

        Paramaters
        ----------

        num_outlets : int
            Number of outlets in the coffee machine.
    
        beverages : dict
            Recipes for the various drinks the machine makes.
            Dictionary with name as key, and a dictionary as value.
            Value dict has ingredients and required quantities.

        raw_material_qty : dict
            Stores quantity of raw material in the coffee machine.
            Dictionary with ingredient as key, and current amount as value.

        Returns
        -------

        """

        # Check if input is supplied in the correct format
        self.__checkFormat(num_outlets, beverages, raw_material_qty)

        # Check if values make sense semantically
        self.__checkSemantics(num_outlets, beverages, raw_material_qty)

        # If no error, continue onwards and assign values
        self.num_outlets = num_outlets
        self.beverages = beverages
        self.raw_material_qty = raw_material_qty
        self.menu = list(beverages.keys())

        # lock for multithreading
        self.lock = threading.Lock()

        # list of running threads
        self.running_threads = []


    def __checkFormat(self, num_outlets, beverages, raw_material_qty):
        """ Method to check if input is supplied in the correct format to the
        constructor.
        
        Parameters
        ----------

        num_outlets : int
            Number of outlets in the coffee machine.
    
        beverages : dict
            Recipes for the various drinks the machine makes.

        raw_material_qty : dict
            Stores quantity of raw material in the coffee machine.

        Returns
        -------

        """

        # Basic type checks
        if not isinstance(num_outlets, int):
            raise ValueError("Number of outlets is not an integer.")

        if not isinstance(beverages, dict):
            raise ValueError("Beverage list is not a dict.")

        if not isinstance(raw_material_qty, dict):
            raise ValueError("Raw material list is not a dict.")

        # Beverages type checks
        for drink in beverages:

            if not isinstance(drink, str):
                raise ValueError("Name of drink in beverage list not a string.")

            if not isinstance(beverages[drink], dict):
                raise ValueError("Ingredients for drink in beverage list is " + 
                    "not dict.")

            reqd_ingredients = beverages[drink]

            # check if each ingredient dict is well formed
            for raw_material in reqd_ingredients:
                if not isinstance(raw_material, str):
                    raise ValueError("Name of ingredient for drink in "+
                        "beverage list is not a string.")

                if not isinstance(reqd_ingredients[raw_material], int):
                    raise ValueError("Required quantity of ingredient for "+
                        "drink in beverage list is not an integer.")


        # Raw Material Qty type checks
        for ingredient in raw_material_qty:
            if not isinstance(ingredient, str):
                raise ValueError("Name of ingredient in raw material list "+
                    "is not a string.")

            if not isinstance(raw_material_qty[ingredient], int):
                raise ValueError("Quantity of ingredient in raw material"+
                    " list is not an integer.")



    def __checkSemantics(self, num_outlets, beverages, raw_material_qty):
        """ Method to check if supplied input makes semantic sense, i.e,
        if values are positive etc.

        Assumes that correct input format is already checked for.
        
        Parameters
        ----------

        num_outlets : int
            Number of outlets in the coffee machine.
    
        beverages : dict
            Recipes for the various drinks the machine makes.

        raw_material_qty : dict
            Stores quantity of raw material in the coffee machine.

        Returns
        -------

        """

        if num_outlets <= 0:
            raise ValueError("Number of outlets must be more than 0.")

        # Beverages type checks
        for drink in beverages:
            for ingredient in beverages[drink]:
                if beverages[drink][ingredient] < 0:
                    raise ValueError("Quantity of ingredient in drink "+
                        "cannot be less than 0.")

        # Raw Material Qty type checks
        for ingredient in raw_material_qty:
            if raw_material_qty[ingredient] < 0:
                raise ValueError("Quantity of a raw material cannot "+
                    "be less than 0.")


    def refill(self, ingredient, qty):
        """ Method to refill certain ingredient by given amount.
        Assumes populated coffee machine.
        
        Parameters
        ----------

        ingredient : str
            Name of ingredient to be refilled

        qty : int
            Quantity to be added

        Returns
        -------

        """

        # type checks
        if not isinstance(ingredient, str):
            raise ValueError("Ingredient is not a string.")

        if not isinstance(qty, int):
            raise ValueError("Quantity is not an integer.")

        # check if ingredient found in dictionary
        if ingredient not in self.raw_material_qty :
            raise ValueError("Ingredient not in coffee machine.")

        # semantic check : refilling should not leave the coffee maachine
        # with negative value
        if self.raw_material_qty[ingredient] + qty < 0 :
            raise ValueError("Cannot add because final quantity of "+
                "ingredient after refilling becomes negative")

        # add to coffee machine
        self.raw_material_qty[ingredient] += qty


    def __canMakeDrink(self, drink_name):
        """Method to check if a certain drink can be made with the current
        contents of the machine. Assumes populated coffee machine.

        Parameters
        ----------
        drink_name : str
            Name of drink to be made

        Returns
        -------
        status : int
            Returns if it is possible to make drink.
            Casewise, returns:
                1, if drink can be made
                0, if insufficient ingredients
                -1, if ingredient not found

        """
        if not isinstance(drink_name, str):
            raise ValueError("Drink name is not a string in canMake.")

        if drink_name not in self.beverages:
            raise ValueError("Drink recipe is not known in canMake.")

        # get recipe from coffee machine
        recipe = self.beverages[drink_name]

        # first check if all ingredients even exist
        for ingredient in recipe:
            if ingredient not in self.raw_material_qty:
                return -1
        
        # then check if quantities are sufficient
        for ingredient in recipe:
            if self.raw_material_qty[ingredient] < recipe[ingredient]:
                return 0

        return 1


    def __pourDrink(self, drink_name):
        """Method to subtract contents of drink. 
        Only used after it is known that a drink can be made. 
        Assumes populated coffee machine.

        Parameters
        ----------
        drink_name : str
            Name of drink to be made

        Returns
        -------

        """
        recipe = self.beverages[drink_name]

        for ingredient in recipe:
            self.raw_material_qty[ingredient] -= recipe[ingredient]


    def __makeDrink(self, drink_name, drink_ID):
        """Method to make a drink order.

        Parameters
        ----------
        drink_name : str
            String of drink name.

        drink_ID : int
            Drink ID for determining which process it is.

        Returns
        -------

        """

        # check if drink has known recipe, and is a string
        if not isinstance(drink_name, str):
            raise ValueError("Drink name is not a string.")

        if drink_name not in self.beverages:
            raise ValueError("Drink recipe is not known.")

        with self.lock:
            status = self.__canMakeDrink(drink_name)

            print("Currently preparing drink number " + str(drink_ID) + ".")
            print()

            # if drink can be made
            if status == 1:
                # make it
                self.__pourDrink(drink_name)
                print(drink_name + " can be made.")
                print("Now pouring the ingredients ...")
                # time.sleep(2)
                print("Done!")
                print()
                print("###########")

            # if drink can't be made due to insufficiency
            elif status == 0:
                insuff_ing_list = []
                insuff_ing_qty = []

                # find which ingredients are insufficient
                recipe = self.beverages[drink_name]
                for ingredient in recipe:
                    if self.raw_material_qty[ingredient] < recipe[ingredient]:
                        insuff_ing_list.append(ingredient)
                        insuff_ing_qty.append(recipe[ingredient] - 
                            self.raw_material_qty[ingredient])

                print(drink_name + " will not be made because some ingredients "+
                    "are not sufficient, which are: ")
                print(insuff_ing_list)

                # Refill and make the drink

                print("Extra amount of these ingredients required is :")
                print(insuff_ing_qty)

                # refill these ingredients using the method
                for i in range(len(insuff_ing_list)):
                    self.refill(insuff_ing_list[i], insuff_ing_qty[i])

                print("Refilled the ingredients, now they are sufficient "+
                    "for making the drink.")
                print("Making the drink now.")
                self.__pourDrink(drink_name)
                print("Now pouring the ingredients ...")
                # time.sleep(2)
                print("Done!")
                print()
                print("###########")
                
            # if machine doesn't have required ingredients
            else:  
                recipe = self.beverages[drink_name]
                nonex_ing_list = []

                # find which ingredients don't exist
                for ingredient in recipe:
                    if ingredient not in self.raw_material_qty:
                        nonex_ing_list.append(ingredient)

                print(drink_name + " cannot be made because some ingredients "+
                    "are not available, which are : ")
                print(nonex_ing_list)
                print()
                print("###########")
                # time.sleep(2)

            self.running_threads.remove(drink_ID)

    def makeOrder(self, orders=[]):
        """Class method exposed to the user. Makes 'n' drinks in parallel, 
        based on the order list supplied by the user.

        Parameters
        ----------
        orders : list
            List of user requested drinks

        Returns
        -------

        """

        # check if single order
        if isinstance(orders, str):
            orders = [orders]

        # check if user supplies a list
        if not isinstance(orders, list):
            raise ValueError("Orders were expected in a list.")

        # Orders type checks
        for drink in orders:

            if not isinstance(drink, str):
                raise ValueError("Drink name in order is not a string.")

            if drink not in self.beverages:
                raise ValueError("Drink recipe for ordered drink is not known.")

        if len(orders) == 0:
            print("No orders were given, please give orders.")
            return

        self.orders = orders

        # list of threads containing tasks
        threads = []

        # iterate over orders drink wise, spawn parallel processes
        # but only do this if more processes are allowed
        for i in range(len(self.orders)):

            while (len(self.running_threads) >= self.num_outlets):
                time.sleep(3)

            self.running_threads.append(i)

            drink_task = threading.Thread(target=self.__makeDrink, 
                args=(self.orders[i], i))

            threads.append(drink_task)
            drink_task.start()

        for thread in threads:
            thread.join()

        return
    
    def returnIngredientLevel(self):
        """Returns amount of each ingredient left.

        Parameters
        ----------
        None

        Returns
        -------
        ingredients_level : dict
            Returns a dict of all ingredients, where the value is the amount of
            ingredient that is left in the machine.
        """
        return self.raw_material_qty