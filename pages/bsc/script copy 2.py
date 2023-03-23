import requests
import json
import math
import os

version_string = '1.19'
url = 'https://raw.githubusercontent.com/misode/mcmeta/' + version_string + '-registries/block/data.json'
# Send a GET request to the URL and get the content
try:
    response = requests.get(url)
    response.raise_for_status()  # This will raise an error if the response status code is not 200
    blocks = json.loads(response.content)
except requests.exceptions.RequestException as e:
    feedback = 'E404: Invalid version, or no internet connection.'

url = 'https://raw.githubusercontent.com/misode/mcmeta/' + version_string + '-summary/blocks/data.json'
# Send a GET request to the URL and get the content
try:
    response = requests.get(url)
    response.raise_for_status()  # This will raise an error if the response status code is not 200
    states = json.loads(response.content)
except requests.exceptions.RequestException as e:
    feedback = 'E404: Invalid version, or no internet connection.'

## Sort blocks by their complexity descending
for i,key in enumerate(states):
    num_states = 0
    for state in states[key][0]:
        num_states += len(states[key][0][state]) - 1
    states[key].append(num_states)

sorted_blocks = sorted(states, key=lambda x: -states[x][-1])
# Add all blocks to the list
for block in blocks:
    if block not in sorted_blocks:
        sorted_blocks.append(block)

# Group size
branches = 8
levels = math.ceil(math.log(len(sorted_blocks),branches))
#for l in range(0,levels):
N = len(sorted_blocks) // branches
groups = [sorted_blocks[i:i+N] for i in range(0, len(sorted_blocks), N)]

for i in range(0,10):
    print(sorted_blocks[i])
    print(states[sorted_blocks[i]][-1])

