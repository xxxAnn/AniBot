import json

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
        self.exploitable = [k for k in data.keys() if data[k]["Exploit"] != False]
        self.fishable = [k for k in data.keys() if data[k]["Fishing"] != False]
        self.fishweights = [data[k]["Fishing"] for k in data.keys() if data[k]["Fishing"] != False]
        self.exploitweights = [data[k]["Exploit"] for k in data.keys() if data[k]["Exploit"] != False]
        self.fishable.append(0)
        self.exploitable.append(0)
        self.exploitweights.append(1-sum(self.exploitweights))
        self.fishweights.append(1-sum(self.fishweights))


    @staticmethod
    def get_instance():
        if Metareader._instance == None:
            Metareader()
        return Metareader._instance