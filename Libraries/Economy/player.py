import json
import time
from random import randint

from Libraries.Economy.items import ItemHandler
from Libraries.Library import sqlClient
from Libraries.Economy.globals import Waterfall, EconomyHandler

class PlayerHandler:
    # // loads data from the database
    @staticmethod
    def jsonLoad():
        client = sqlClient()
        result = client.select("data", "id", "1")
        client.end()
        return json.loads(result[1])

    @staticmethod
    def toContentLiteral(inventoryContentItem):
        literal_list = []
        for item in inventoryContentItem:
            if item == None: continue
            x = {"Id": item.id, "Name": item.name, "Amount": item.amount, "Exclusive": item.exclusive}
            literal_list.append(x)
        return literal_list

    # // Saves data into the database
    @staticmethod
    def jsonUpdate(data):
        client = sqlClient()
        client.update("data", "jsonColumn", "id", "1", json.dumps(data))
        client.end()

    @staticmethod
    def constructPlayer(id):
        id = str(id)
        data = PlayerHandler.jsonLoad()
        if id not in data:
            data[id] = {"Money": 0, "Inventory": [], "Position": (randint(10, 100), randint(10, 100)), "Energy": {"Val": 10, "Recover": int(time.time())}}
        listContent = []
        for i in data[id]["Inventory"]:
            if i["Amount"] != 0:
                x = ItemHandler.get_item(id=i["Id"], name=i["Name"], amount=i["Amount"], exclusive=i["Exclusive"])
                listContent.append(x)
        inventoryObject = ItemHandler.Inventory(listContent, data[id]["Inventory"])
        if not "Position" in data[id]:
            data[id]["Position"] = (randint(10, 100), randint(10, 100))
        playerObject = PlayerHandler.Player(inventoryObject, data[id]["Money"], data[id]["Energy"], id=id, position=data[id]["Position"])
        playerObject.save()
        return playerObject

    class Player(Waterfall):

        def __init__(self, inventory, money, energy, id, position):
            self.inventory = inventory
            self.money = money
            self.energy = energy
            self.id = str(id)
            self.position = list(position)

        def save(self):
            data = PlayerHandler.jsonLoad()
            if self.id not in data:
                data[self.id] = {"Energy": None, "Money": None, "Inventory": None, "Position": None}
            data[self.id]["Energy"] = self.energy
            data[self.id]["Money"] = self.money
            data[self.id]["Position"] = self.position
            content_literal = PlayerHandler.toContentLiteral(self.inventory.content)
            data[self.id]["Inventory"] = content_literal
            PlayerHandler.jsonUpdate(data)

        def craft(self, item_name, amount):
            item = ItemHandler.get_item(ItemHandler.id_from_name(item_name))
            if item.craftable():
                craft_data = item.get_craft_metadata()
                # Applying multipliers
                for i in range(0,2):
                    craft_data["requireditemsamount"][i]*=amount
                craft_data["ResultAmount"]*=amount
                # Checking if craft is legal
                if not self.inventory.multi_has(craft_data["requireditems"]): return 2
                for i in range(0,2):
                    item = self.inventory.get(str(craft_data["requireditems"][i]))
                    if not item.amount >= craft_data["requireditemsamount"][i]: return 3
                    item.amount -= craft_data["requireditemsamount"][i]
                result = ItemHandler.get_item(ItemHandler.id_from_name(item_name))
                result.amount = craft_data["ResultAmount"]
                self.inventory + result
                self.save() 
                return 20 
            else:
                return 1

        def __eq__(self, other):
            if isinstance(other, PlayerHandler.Player):
                if self.id == other.id:
                    return True
                else:
                    return False
            else:
                raise TypeError
