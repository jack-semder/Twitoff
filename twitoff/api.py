"""
API -- Application Programming Interface
"""

import requests
import json


status = requests.get('https://pokeapi.co/api/v2/pokemon/pikachu')
py_obj = json.loads(status.text)