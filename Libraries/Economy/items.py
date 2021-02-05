from Libraries.Economy.globals import Waterfall, EconomyHandler
from Libraries.Economy.metareader import Metareader
import json

class ItemHandler:
    class Item(Waterfall):
        def __init__(self, id, name, amount, exclusive, itemtype):
            self.id = str(id)
            self.name = name
            self.amount = amount
            self.exclusive = exclusive
            self.type = itemtype

        def craftable(self):
            if self.id in ItemHandler.metareader().crafts:
                return True
            return False
        
        def get_craft_metadata(self):
            if self.craftable():
                return ItemHandler.metareader().crafts[self.id]
            return None

    class Inventory:
        def __init__(self, content, content_literal):
            self.content = content
            self.deprecated_content_literal = content_literal # // This will be removed soon because I have no clues what it does

        def __add__(self, item):
            for i in self.content:
                if i.id == item.id:
                    i.amount+=item.amount
                    return "Added item"
            self.content.append(item)
            return "Added item"

        def has(self, selectid: str):
            for item in self.content:
                if str(item.id) == selectid:
                    return item
            return False

        def multi_has(self, ids):
            for id in ids:
                if self.has(str(id)) == False:
                    return False
            return True

        # // Returns the item \\ #
        def get(self, selectid: str):
            for item in self.content:
                if str(item.id) == selectid:
                    return item
            return None

    @staticmethod
    def metareader(update=False):
        if update: Metareader.get_instance().update_meta()
        return Metareader.get_instance()

    @staticmethod
    def id_from_name(name: str):
        meta = ItemHandler.metareader()
        name = str.lower(name)
        if name in meta.nametoid:
            return(meta.nametoid[name])
        else:
            return "Not Found"

    @staticmethod
    def get_item(id: str, name=None, amount: int=1,  exclusive=False):
        meta = ItemHandler.metareader()
        amount = int(amount)
        if id in meta.idtoname:
            name = meta.idtoname[id]
        else:
            return None
        return ItemHandler.Item(str(id), str(name), amount=amount, exclusive=exclusive, itemtype=meta.types[id])

