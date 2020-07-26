from Libraries.Economy.items import ItemHandler
from Libraries.Library import sqlClient
import json
from Libraries.Economy.globals import Waterfall, EconomyHandler
from random import randint

class ShopHandler:
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
            x = {"Id": item.id, "Name": item.name, "Amount": item.amount, "Exclusive": item.exclusive, "Price": item.price}
            literal_list.append(x)
        return literal_list

    # // Saves data into the database
    @staticmethod
    def jsonUpdate(data):
        client = sqlClient()
        client.update("data", "jsonColumn", "id", "1", json.dumps(data))
        client.end()

    class shopItem(ItemHandler.Item):
        def __init__(self, id, name, amount, exclusive, price):
            self.id = str(id)
            self.name = name
            self.amount = amount
            self.exclusive = exclusive
            self.price = price

    class Shop(Waterfall):
        def __init__(self, owner, inv, name, level, id):
            self.owner = int(owner)
            self.inv = inv
            self.name = name
            self.id = str(id)
            self.level = level

        def save(self):
            data = ShopHandler.jsonLoad()
            content_literal = ShopHandler.toContentLiteral(self.inv.content)
            data["Shops"][self.id]["Inventory"] = content_literal
            ShopHandler.jsonUpdate(data)

        def add_item(self, item, amount, price):
            new_item = ShopHandler.shopItem(id=item.id, name=item.name, amount=amount, exclusive=item.exclusive, price=price)
            for i in self.inv.content:
                if i.id == new_item.id:
                    i.amount+=new_item.amount
                    return EconomyHandler.Success()
            if len(self.inv.content) >= self.level*5:
                return EconomyHandler.Errors.ShopItemLimitReached()
            self.inv.content.append(new_item)
            return EconomyHandler.Success()

        def __eq__(self, other):
            if isinstance(other, ShopHandler.Shop):
                raise NotImplementedError
            else:
                return False

        def __str__(self):
            return self.name

    @staticmethod
    def constructShop(shopId):
        data = ShopHandler.jsonLoad()
        listContent = []
        for i in data["Shops"][shopId]["Inventory"]:
            if "Price" not in i:
                i["Price"] = 500
            if not i["Amount"] == 0:
                x = ShopHandler.shopItem(i["Id"], i["Name"], i["Amount"], i["Exclusive"], i["Price"])
                listContent.append(x)
        inventoryObject = ItemHandler.Inventory(listContent, data["Shops"][shopId]["Inventory"])
        shopObject = ShopHandler.Shop(owner=data["Shops"][shopId]["Owner"], inv=inventoryObject, level=data["Shops"][shopId]["Level"], name =data["Shops"][shopId]["Name"], id=shopId)
        return shopObject


    @staticmethod
    def findShopFromName(shopName: str):
        data = ShopHandler.jsonLoad()
        for i in data["Shops"].keys():
            if str.lower(data["Shops"][i]["Name"]) == str.lower(shopName):
                id = data["Shops"][i]["Id"]
                return ShopHandler.constructShop(str(id))
        return "Not Found"

    @staticmethod
    def createShop(name: str, ownerId: str):
        ownerId = str(ownerId)
        data = ShopHandler.jsonLoad()
        inventory_literal = []
        shopId = randint(100000000, 999999999)
        while str(shopId) in data["Shops"]:
            shopId = randint(100000000, 999999999)
        shopId = str(shopId)
        for i in data["Shops"].keys():
            thingy = data["Shops"][i]
            if str.lower(thingy["Name"]) == str.lower(name):
                return EconomyHandler.Errors.ShopAlreadyExists(), 0
        data["Shops"][shopId] = {"Id": shopId, "Name": name, "Owner": ownerId, "Level": 1, "Inventory": inventory_literal}
        ShopHandler.jsonUpdate(data)
        return EconomyHandler.Success(), str(shopId)
