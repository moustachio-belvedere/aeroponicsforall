from os import walk, path
import json

def populateimagelist():
    imfoldir = 'public/images_lores/'
    imagefilenames = []
    for dirpath, dirnames, filenames in walk(imfoldir):
        for filename in filenames:
            if filename.endswith("jpg"):
                imagefilenames.append(filename)
    
    fildir = path.join(imfoldir, "listofimages.json")
    with open(fildir, "w") as f:
        json.dump(imagefilenames, f)
        
def appendtoJSON(jsonpath, data):
    try:
        with open(jsonpath, 'r') as f:
            array = json.load(f)
    except FileNotFoundError:
        array = []

    array.append(data)

    with open(jsonpath, "w") as f:
        json.dump(array, f)     
    
