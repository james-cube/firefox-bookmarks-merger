import json

def load_bookmarks_file(filename):
    with open(filename) as json_data:
        return { "name" : filename, "json" : json.load(json_data) }

def load_bookmarks_files(filenames):
    for filename in filenames:
        yield load_bookmarks_file(filename)

def write_to_file(filename, output):
    with open(filename, "w") as out:
        out.write(output) 
