import json
import random

from Libraries.Library import sqlClient

class TheWorld:
    def __init__(self):
        self.tiles = {}
        self.load()

    def load(self):
        try: 
            client = sqlClient()
            result = client.select("data", "id", "2")
            client.end()
            print(result)
            temp = json.loads(result[1]) 
        except:
            client = sqlClient()
            client.update("data", "jsonColumn", "id", "2", json.dumps([{"Position": (1, 4), "Feature": "Forest"}]))
            client.end()
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
        client = sqlClient()
        client.update("data", "jsonColumn", "id", "2", json.dumps(datastruct))
        client.end()

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


        
