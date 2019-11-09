import json


def load_json(json_file):
    with open(json_file) as data:
        return json.load(data)


def dump_json(data, json_file):
    print("Dumping", json_file)
    with open(json_file, 'w') as handler:
        json.dump(data, handler)
