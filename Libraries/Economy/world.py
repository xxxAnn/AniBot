import json
import random

from Libraries.Library import sqlClient

class TheWorld:
    def __init__(self):
        self.tiles = {}
        self.load()

    def load(self):
        try: 
            with open("data/supermap.json", "r") as f:
                temp = json.loads(f.read())
        except:
            with open("data/supermap.json", "w") as f:
                f.write(json.dumps([]))
            self.load()
            return
        for tile in temp:
            self.tiles[tuple(tile["Position"])] = Tile(pos=tile["Position"], feature=tile["Feature"])
        
    def new_tile(self, destination):
        self.tiles[destination] = Tile(destination)
        return self.tiles[destination]
    
    def save(self):
        datastruct = []
        for pos, tile in self.tiles.items():
            datastruct.append({"Position": pos, "Feature": tile.feature})
        with open("data/supermap.json", "w") as f:
                f.write(json.dumps(datastruct))

    def move_to(self, position: tuple, vector: tuple):
        destination = tuple(map(sum, zip(position, vector)))
        return self.get_tile(destination)
    
    def get_tile(self, destination):
        if self.tiles[destination]: return self.tiles[destination]
        return self.new_tile(destination)
        

class Tile:
    def __init__(self, pos, feature=None):
        self.position = pos
        if not feature:
            lch = ["Forest", "Mine", "Mountain", "Lake", "Village", "Plain", "Waterfall"]
            lchw = [0.1, 0.1, 0.1, 0.1, 0.05, 0.449, 0.001]
            feature = random.choices(lch, lchw, k=1)[0]
        self.feature = feature


        
