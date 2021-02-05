import json
import random

class Metareader:
    _instance = None
    def __init__(self):
        Metareader._instance = self
        self.update_meta()

    def update_meta(self):
        with open("data/gamemeta.json", "r") as f:
            x = f.read()
            data = json.loads(x)["itemdata"]
        self.crafts = {k: v["Recipe"] for k, v in data.items() if v["Recipe"] != False}
        self.idtoname = {k: v["Name"] for k, v in data.items()}
        self.nametoid = {str.lower(v.replace(" ", "_")): k for k, v in self.idtoname.items()}
        self.types = {k: v["Type"] for k, v in data.items()}
        self.edible = [k for k in data.keys() if data[k]["Edible"] != False]
        self.fishable = [k for k in data.keys() if data[k]["Fishing"] != False]
        self.fishweights = [data[k]["Fishing"] for k in data.keys() if data[k]["Fishing"] != False]
        self.rolls = ItemRoller(data, json.loads(x)["features"])


    @staticmethod
    def get_instance():
        if Metareader._instance == None:
            Metareader()
        return Metareader._instance

class ItemRoller:
    def __init__(self, basedata, abovedata):
        self.exploitable = {}
        for featurename in abovedata.keys():
            self.exploitable[featurename] = [(k, self.findmultiplier(basedata[k], abovedata[featurename])) for k in basedata.keys() if basedata[k]["Exploit"] != False]
    
    def findmultiplier(self, x, y):
        if x["Type"] in y: return x["Exploit"]*y[x["Type"]] 
        else: return x["Exploit"]

    def exploit(self, currenttile):
        feature = currenttile.feature
        if feature in self.exploitable:
            temp_items = [element[0] for element in self.exploitable]
            temp_weighs = [element[1] for element in self.exploitable]
            return random.choices(temp_items, temp_weighs)[0]
        else:
            return 0