import json
from pprint import pprint

data = json.load(open('contributors.json'))

pprint([a for a in data if a["author"]["login"]=="torvalds"])