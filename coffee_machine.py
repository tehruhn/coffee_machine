# This class simulates a Coffee Machine in Python for solution to
# the problem posed by HumIt as a part of their interview process.

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

        # Check if input is supplied in the correct format
        self.__checkFormat(num_outlets, beverages, raw_material_qty)

        # Check if values make sense semantically
        self.__checkSemantics(num_outlets, beverages, raw_material_qty)

        # If no error, continue onwards and assign values
        self.num_outlets = num_outlets
        self.beverages = beverages
        self.raw_material_qty = raw_material_qty
        self.menu = list(beverages.keys())


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

        None

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

        None

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

        None

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
        if self.raw_material_qty + qty < 0 :
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
            raise ValueError("Drink name is not a string.")

        if drink_name not in self.beverages:
            raise ValueError("Drink recipe is not known.")

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


    def __makeDrink(self, drink_name):
        """Method to subtract contents of drink. 
        Only used after it is known that a drink can be made. 
        Assumes populated coffee machine.

        Parameters
        ----------
        drink_name : str
            Name of drink to be made

        Returns
        -------
        None

        """
        recipe = self.beverages[drink_name]

        for ingredient in recipe:
            self.raw_material_qty[ingredient] -= recipe[ingredient]


    def __unmakeDrink(self, drink_name):
        """Method to add back contents of a drink.
        Only used after it is known that a drink can be made.
        Assumes populated coffee machine.

        Parameters
        ----------
        drink_name : str
            Name of drink to be made

        Returns
        -------
        None
        """
        recipe = self.beverages[drink_name]

        for ingredient in recipe:
            self.raw_material_qty[ingredient] += recipe[ingredient]


    def __canMakeDrinksList(self, drinks_list):
        """Method to check which drinks can be made out of a list of drinks
        requested by the user.

        Parameters
        ----------
        drinks_list : list
            List of strings of drink names.

        Returns
        -------
        possible_drinks : dict
            Returns a dict of all drinks that can be made. 
            Values are empty lists, for consistency.

        insufficient_drinks : dict
            Returns a dict of all drinks with insufficient ingredients.
            Values are list of insufficient ingredients.

        impossible_drinks : dict
            Returns a dict of drinks with ingredients that don't exist.
            Values are list of ingredients not in coffee machine.

        status_list : list
            Ordered list showing if a drink will be made, or not made due to 
            impossible ingredient/ insufficient ingredient. Has an integer flag 
            corresponding to each value in the drinks list.
            Statuses returned are :
                1, if drink can be made
                0, if insufficient ingredients
                -1, if ingredient not found

        """

        # check if all drinks have known recipes, and are strings
        for drink_name in drinks_list:
            if not isinstance(drink_name, str):
                raise ValueError("Drink name is not a string.")

            if drink_name not in self.beverages:
                raise ValueError("Drink recipe is not known.")


        possible_drinks = {}
        insufficient_drinks = {}
        impossible_drinks = {}

        # maintain list of statuses of drinks in the list, to undo later
        status_list = []

        # find status for each drink in drinks list
        for drink in drinks_list:

            status = self.__canMakeDrink(drink)
            status_list.append(status)

            # if drink can be made
            if status == 1:
                # make it
                self.__makeDrink(drink)
                possible_drinks[drink] = []

            # if drink can't be made due to insufficiency
            elif status == 0:
                insuff_ing_list = []

                # find which ingredients are insufficient
                recipe = self.beverages[drink]
                for ingredient in recipe:
                    if self.raw_material_qty[ingredient] < recipe[ingredient]:
                        insuff_ing_list.append(ingredient)

                # append to dict
                insufficient_drinks[drink] = insuff_ing_list

            # if machine doesn't have required ingredients
            else:  
                recipe = self.beverages[drink]
                nonex_ing_list = []

                # find which ingredients don't exist
                for ingredient in recipe:
                    if ingredient not in self.raw_material_qty:
                        nonex_ing_list.append(ingredient)

                # append to dict
                impossible_drinks[drink] = nonex_ing_list


        # undo all drinks, unmade all made drinks

        for i in range(len(status_list)):
            if status_list[i] == 1:
                self.__unmakeDrink(drinks_list[i])

        return possible_drinks, insufficient_drinks, impossible_drinks, \
        status_list



    
    def giveIndicatorStatus(self):
        """Implements an indicator for the coffee machine.
        Indicator checks if sufficient quantities of each ingredient exist to 
        make all possible drinks in the current menu of the coffee machine.
        The idea is to see if all possible drinks can be made at least once
        using the current contents of the coffee machine. If any drink cannot
        be made due to insufficient ingredients (not inclusing cases where 
        ingredient is not in coffee machine), we must refill that.

        Assumes populated coffee machine.

        Parameters
        ----------
        None

        Returns
        -------
        ingredients_reqd : dict
            Returns a dict of all ingredients, where the value is the amount of
            ingredient that needs to be filled to make all drinks once.

            E.g.
            'hot_water' : 30
            Means that 30 units of hot water needs to be refilled.
            In case the value is zero, this means the ingredient is sufficient.
        """
        menu = self.menu
        curr_qty = self.raw_material_qty.copy()
        ingredients_reqd = self.raw_material_qty.copy()

        # set all ingredients to 0
        ingredients_reqd = ingredients_reqd.fromkeys(ingredients_reqd, 0)

        # make changes based on each drink in menu
        for drink in menu:

            status = self.__canMakeDrink(drink)

            # if drink cannot be made due to insufficient ingredients
            # find how much ingredient is needed
            if status == 0:
                drink_recipe = self.beverages[drink]
                for ingredient in drink_recipe:

                    #if drink requires more ingredient than machine has
                    if drink_recipe[ingredient] > curr_qty[ingredient]:
                        ingredients_reqd[ingredient] = \
                        max(ingredients_reqd[ingredient], 
                            drink_recipe[ingredient] - curr_qty[ingredient])

        return ingredients_reqd


    def asManyDrinksAsPossible(self, verbose=False):
        """Method to make as many drinks as possible, given the coffee machine,
        and outlets.

        Parameters
        ----------
        verbose : True
            Flag set to true for verbose output.

        Returns
        -------
        possible_drinks : dict
            Returns a dict of all drinks that can be made. 
            Values are empty lists, for consistency.

        no_outlet_drinks : dict
            Returns a list of all drinks that can be made, but there aren't
            sufficient outlets. Values are empty lists for consistency.

        insufficient_drinks : dict
            Returns a dict of all drinks with insufficient ingredients.
            Values are list of insufficient ingredients.

        impossible_drinks : dict
            Returns a dict of drinks with ingredients that don't exist.
            Values are list of ingredients not in coffee machine.

        status_list : list
            Ordered list showing if a drink will be made, or not made due to 
            impossible ingredient/ insufficient ingredient. Has an integer flag 
            corresponding to each value in the drinks list.
            Statuses returned are :
                1, if drink can be made
                0, if insufficient ingredients
                -1, if ingredient not found
                -2, if drink can be made but not enough outlets
        """

        menu = self.menu
        num_outlets = self.num_outlets
        possible, insufficient, impossible, statuses = \
        self.__canMakeDrinksList(menu)

        no_outlet= {}

        # check if number of possible drinks is greater than outlets
        if len(possible) > num_outlets :
            no_outlet = dict(possible.items()[num_outlets:])
            possible = dict(possible.items()[0:num_outlets])

        # Update status for drinks that can be made but have no outlet
        for i in range(len(statuses)):
            if menu[i] in no_outlet:
                status[i] = -2

        if verbose:
            print()
            self.__verboseOutput(possible, no_outlet, insufficient, 
                impossible, statuses)
        return possible, no_outlet, insufficient, impossible, statuses


    def __verboseOutput(self, possible, no_outlet, insufficient, impossible, 
        statuses):
        """Method to print verbose output for which drinks can be made
        concurrently.

        Parameters
        ----------
        possible_drinks : dict
            Returns a dict of all drinks that can be made. 
            Values are empty lists, for consistency.

        no_outlet_drinks : dict
            Returns a list of all drinks that can be made, but there aren't
            sufficient outlets. Values are empty lists for consistency.

        insufficient_drinks : dict
            Returns a dict of all drinks with insufficient ingredients.
            Values are list of insufficient ingredients.

        impossible_drinks : dict
            Returns a dict of drinks with ingredients that don't exist.
            Values are list of ingredients not in coffee machine.

        status_list : list
            Ordered list showing if a drink will be made, or not made due to 
            impossible ingredient/ insufficient ingredient. Has an integer flag 
            corresponding to each value in the drinks list.
            Statuses returned are :
                1, if drink can be made
                0, if insufficient ingredients
                -1, if ingredient not found
                -2, if drink can be made but not enough outlets

        Returns
        -------

        None

        """

        menu = self.menu

        for i in range(len(menu)):

            status = statuses[i]
            # if drink can be made
            if status == 1:
                print(menu[i] + " can be made.")
                print()

            # if insufficient ingredients
            elif status == 0:
                print(menu[i] + " cannot be made because some ingredients "+
                    "are not sufficient, which are: ")
                print(insufficient[menu[i]])
                print()

            # if impossible
            elif status == -1:
                print(menu[i] + " cannot be made because some ingredients "+
                    "are not available, which are : ")
                print(impossible[menu[i]])
                print()

            else :
                print(menu[i] + "cannot be made even though all ingredients "+
                    "are sufficient and available, but the machine does"+
                    " not have enough outlets.")
                print()

