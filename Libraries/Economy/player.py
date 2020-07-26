from Libraries.Economy.items import ItemHandler
from Libraries.Library import sqlClient
import time
import json

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
            data[id] = {"Money": 0, "Inventory": [], "Energy": {"Val": 10, "Recover": int(time.time())}}
        listContent = []
        for i in data[id]["Inventory"]:
            x = ItemHandler.get_item(id=i["Id"], name=i["Name"], amount=i["Amount"], exclusive=i["Exclusive"])
            listContent.append(x)
        inventoryObject = ItemHandler.Inventory(listContent, data[id]["Inventory"])
        playerObject = PlayerHandler.Player(inventoryObject, data[id]["Money"], data[id]["Energy"], id=id)
        playerObject.save()
        return playerObject

    class Player:

        def __init__(self, inventory, money, energy, id):
            self.inventory = inventory
            self.money = money
            self.energy = energy
            self.id = str(id)

        def save(self):
            data = PlayerHandler.jsonLoad()
            if self.id not in data:
                data[self.id] = {"Energy": None, "Money": None, "Inventory": None}
            data[self.id]["Energy"] = self.energy
            data[self.id]["Money"] = self.money
            content_literal = PlayerHandler.toContentLiteral(self.inventory.content)
            data[self.id]["Inventory"] = content_literal
            PlayerHandler.jsonUpdate(data)
