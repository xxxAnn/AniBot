class ItemHandler:
    class Item:
        def __init__(self, id, name, amount, exclusive):
            self.id = str(id)
            self.name = name
            self.amount = amount
            self.exclusive = exclusive

    class Food(Item):
        def _type(self):
            return "Food"

    class Tool(Item):
        pass

    class Weapon(Tool):
        def _type(self):
            return "Weapon"

    class Resource(Item):
        def _type(self):
            return "Resource"

    class FisherRod(Tool):
        def _type(self):
            return "FisherRod"

    class Animal(Item):
        def _type(self):
            return "Animal"

    class Inventory:
        def __init__(self, content, content_literal):
            self.content = content
            self.deprecated_content_literal = content_literal # // This will be removed soon because I only use it for 1 thing

        # // Adds item to inventory \\ #
        def __add__(self, item):
            for i in self.content:
                if i.id == item.id:
                    i.amount+=item.amount
                    return "Added item"
            self.content.append(item)
            return "Added item"
        # // Checks if the item is in the inventory and returns the item if it is \\ #
        def has(self, selectid: str):
            for item in self.content:
                if str(item.id) == selectid:
                    return item
            return False
        # // Returns the item \\ #
        def get(self, selectid: str):
            for item in self.content:
                if str(item.id) == selectid:
                    return item
            return None

    @staticmethod
    def id_from_name(name: str):
        id_dict = {
        "oil": "1",
        "bronze_ore": "2",
        "frog": "3",
        "diamond_ore": "4",
        "gold_ore": "5",
        "iron_ore": "6",
        "silver_ore": "7",
        "wood": "8",
        "bread": "9",
        "carp": "10",
        "meat": "17",
        "bronze_knife": "100",
        "plastic": "101",
        "toy_knife": "103",
        "diamond_sword": "104",
        "silver_sword": "105"}
        name = str.lower(name)
        if name in id_dict:
            return(id_dict[name])
        else:
            return "Not Found"

    @staticmethod
    def get_item(id: str, name=None, amount: int=1,  exclusive=False):
        amount = int(amount)
        dict_name = {
        "1": "Oil",
        "2": "Bronze Ore",
        "3": "Frog",
        "4": "Diamond Ore",
        "5": "Gold Ore",
        "6": "Iron Ore",
        "7": "Silver Ore",
        "8": "Wood",
        "9": "Bread",
        "10": "Carp",
        "17": "Meat",
        "100": "Bronze Knife",
        "101": "Plastic",
        "103": "Toy Knife",
        "104": "Diamond Sword",
        "105": "Silver Sword"
        }
        food = ["9", "10", "17"]
        resource = ["1", "2", "4", "5", "6", "7", "8", "101"]
        weapon = ["100", "103", "104", "105"]
        animal = ["3"]
        if name == None:
            if id in dict_name:
                name = dict_name[id]
                if id in food:
                    return ItemHandler.Food(id, name, amount, exclusive)
                elif id in resource:
                    return ItemHandler.Resource(id, name, amount, exclusive)
                elif id in weapon:
                    return ItemHandler.Weapon(id, name, amount, exclusive)
                elif id in animal:
                    return ItemHandler.Animal(id, name, amount, exclusive)
                else:
                    return ItemHandler.Item(id, name, amount, exclusive)
            else:
                return "Not found"
        else:
            if id in food:
                return ItemHandler.Food(id, name, amount, exclusive)
            elif id in resource:
                return ItemHandler.Resource(id, name, amount, exclusive)
            elif id in weapon:
                return ItemHandler.Weapon(id, name, amount, exclusive)
            elif id in animal:
                return ItemHandler.Animal(id, name, amount, exclusive)
            else:
                return ItemHandler.Item(id, name, amount, exclusive)
