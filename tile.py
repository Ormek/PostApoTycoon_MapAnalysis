from tiler import Tiler

class Tile:
    tiles=None
    smallestX=0
    smallextY=0
    tilePerHash={}

    def init(tiles, smallestX=0, smallestY=0):
        Tile.tiles=tiles
        Tile.smallestX=smallestX
        Tile.smallestY=smallestY
        Tile.tilePerHash={} # Reset

    def __init__(self, hashcode, representation):
        self.hash=hashcode
        self.usedAt=set()
        self.representationTile=representation
        self.addTileIndex(representation)
        Tile.tilePerHash[self.hash]=self

    def addTileIndex(self, index):
        self.usedAt.add(index)

    def getX(self) -> int:
        return Tile.tiles.get_tile_mosaic_position(self.representationTile)[1]+Tile.smallestX
    
    def getY(self) -> int:
        return Tile.tiles.get_tile_mosaic_position(self.representationTile)[0]+Tile.smallestY
        
    def getCount(self) -> int:
        return len(self.usedAt)
    
    def getHash(self) -> int:
        return self.hash
    
    def getRepresentation(self) -> int:
        return self.representationTile