# read in png image and convert to numpy array

from email.mime import image
import hashlib # to get a STABLE hash of the tile content, we can use this as a key to identify unique tiles.

from tiler import Tiler   
from tile  import Tile

import numpy as np
from PIL import Image

def parse_image(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Convert the image to RGB (in case it's in a different mode)
        img = img.convert('RGB')
        # Convert the image to a numpy array
        img_array = np.array(img)
    return img_array

def tile_image(image_array, smallestY=0, smallestX=0):
    # Setup tiling parameters
    tiles = Tiler(data_shape=image_array.shape,
            tile_shape=(7, 7, 3),
            channel_dimension=-1)
    Tile.init(tiles, smallestX, smallestY)
        
    # create a hashmap of tile-type (content) to tile-id
    tile_content_to_ids = {}
    ## Access tiles:
    height, width = tiles.get_mosaic_shape()
    print(f'Height in Tiles: {height}, Width in Tiles: {width}')
    print(f'Image top    left  corner: ({smallestX},{smallestY})')
    print(f'Image bottom right corner: ({smallestX+width-1},{smallestY+height-1})')

    tilearray  = []
    # 1b. Iterate the tiles
    for tile_id, tile in tiles(image_array):
        if tile_id%width==0:
            row=[]
            tilearray.append(row)
        tileHash=int(hashlib.md5(tile.tobytes()).hexdigest()[0:8],16)
        tileObj = tile_content_to_ids.get(tileHash)
        if tileObj != None:
            tileObj.addTileIndex(tile_id)
        else:
            tile_content_to_ids[tileHash]=Tile(tileHash, tile_id) 

        row.append(tileObj)

    print (f'Unique tiles: {len(tile_content_to_ids)}')

    ## Create images for each tile and store it.
    index=0
    for content_hash, tileObj in tile_content_to_ids.items():
        representation = tileObj.getRepresentation() 
        x=tileObj.getX()
        y=tileObj.getY()  
        tile=Tile.tiles.get_tile(image_array, representation, copy_data=False)
        Image.fromarray(tile).save(f'tiles/tile_{x:+04d}_{y:+04d}_{int(content_hash):010d}.png') 
        print(f'{index:4d}/{len(tile_content_to_ids)} Tile id: {representation}, Representation: ({x},{y})), count: {len(tile_content_to_ids)}      ',end="\r")
        index += 1
    print (" "*90)
    print (f'Unique tiles: {len(tile_content_to_ids)}')
    return tiles, tile_content_to_ids, tilearray

def writeTiles(filename, tilearray):
    ## output tiles as csv by their representation id
    with open(filename, 'w') as f:
        for row in tilearray:
            f.write(','.join(map(str, row)) + '\n') 
            
def writeTileData(filename, tilecontent):
    ## output tile content as csv by their representation id
    with open(filename  , 'w') as f:
        f.write('content_hash,rep_x, rep_y, count\n')
        for content_hash, tileObj in tilecontent.items():
            f.write(f'{content_hash},{tileObj.getX()},{tileObj.getY()},{tileObj.getCount()}\n')
            
# Example usage
if __name__ == "__main__":  
    image_path = 'myMap_1777713062244.png'  # Replace with your image path
    image_array = parse_image(image_path)
    
    print("Loaded image with shape: (height, width, depth)",image_array.shape)
    tiles, tilecontent, tilearray = tile_image(image_array, smallestY=-214, smallestX=-184)
    
    writeTiles("tiles.csv", tilearray)
    
    writeTileData("entries.csv", tilecontent)

        
        