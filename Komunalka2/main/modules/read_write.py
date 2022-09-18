import json

def write_to_json(p, ob):
    with open( p, 'w') as f:
        j = json.dumps(ob)
        f.write(j)

def read_json(p):
    with open( p, 'r') as f:
        return json.load(f)