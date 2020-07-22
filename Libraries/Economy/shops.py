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
            x = {"Id": item.id, "Name": item.name, "Amount": item.amount, "Exclusive": item.exclusive}
            literal_list.append(x)
        return literal_list

    # // Saves data into the database
    @staticmethod
    def jsonUpdate(data):
        client = sqlClient()
        client.update("data", "jsonColumn", "id", "1", json.dumps(data))
        client.end()

    class Shop:
        def __init__(self, owner, inv, name):
            self.owner = owner
            self.inv = inv
            self.name = name
            self.id = str(id)

        def save(self):
            data = ShopHandler.jsonLoad()
            content_literal = toContentLiteral(self.inv.content)
            data["Shops"][self.id]["Inventory"] = content_literal
            ShopHandler.jsonUpdate(data)

    @staticmethod
    def constructShop(shopId):
        data = ShopHandler.jsonLoad()
        listContent = []
        for i in data["Shops"][shopId]["Inventory"]:
            x = ItemHandler.get_item(i["Id"], i["Name"], i["Amount"], i["Exclusive"])
            listContent.append(x)
        inventoryObject = ItemHandler.Inventory(listContent, data[id]["Inventory"])
        shopObject = ShopHandler.Shop(data["Shops"][shopId]["Owner"], inventoryObject, data["Shops"][shopId], shopId)
        return shopObject
