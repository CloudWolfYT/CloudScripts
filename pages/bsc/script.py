import requests
import json
import math
import os

class BSCScript():
    def __init__(self, root):
        self.blocks = []
        self.states = dict()
        self.root = root
    
    def fetchBlocks(self,version_string):
        feedback = ''
        url = 'https://raw.githubusercontent.com/misode/mcmeta/' + version_string + '-registries/block/data.json'
        # Send a GET request to the URL and get the content
        try:
            response = requests.get(url)
            response.raise_for_status()  # This will raise an error if the response status code is not 200
            self.blocks = json.loads(response.content)
            feedback += 'Loaded '+str(len(self.blocks))+' Blocks'
        except requests.exceptions.RequestException as e:
            feedback = 'E404: Invalid version, or no internet connection.'

        url = 'https://raw.githubusercontent.com/misode/mcmeta/' + version_string + '-summary/blocks/data.json'
        # Send a GET request to the URL and get the content
        try:
            response = requests.get(url)
            response.raise_for_status()  # This will raise an error if the response status code is not 200
            self.states = json.loads(response.content)
            feedback += ' and ' + str(len(self.states)) + ' Block State holding blocks.'
        except requests.exceptions.RequestException as e:
            feedback = 'E404: Invalid version, or no internet connection.'

        return feedback

    def generate(self,pb,master):
        # Group size
        branches = 8

        next_level = self.blocks

        levels = math.ceil(math.log(len(next_level),branches))
        progress_max = levels
        progress = 0
        next_block = next_level
        fcnID = 0
        for l in range(0,levels):
            progress += 1
            pb.update(100*progress/progress_max)
            master.update_idletasks()

            # Create a list to store the grouped block types
            groups = [next_level[i:i+branches] for i in range(0, len(next_level), branches)]
            group_block = [next_block[i:i+branches] for i in range(0, len(next_block), branches)]
            next_level = []
            next_block = []
            # Create the first tags
            for i, group in enumerate(groups):
                next_level.append(f"l{l}_{i}")
                next_block.append(group[0])

                ## TAGS
                self._group_tags(l,i,group)

                ## Block -> NBT
                fcnID = self._group_block_to_nbt(l,i,group,self.states,fcnID)
                
    def _group_tags(self,l,i,group):
        os.makedirs(f"{self.root.output_path}/bsc/tags/blocks", exist_ok=True)
        if(l==0):
            group_dict = {"values": group}
        else:
            group_dict = {"values": [f"#bsc:{i}" for i in group]}
        with open(f"{self.root.output_path}/bsc/tags/blocks/l{l}_{i}.json", "w") as file:
            json.dump(group_dict, file, indent=4)

    def _group_block_to_nbt(self,l,i,group,all_states,fcnID):
        name = "get_nbt"
        path = f"{self.root.output_path}/bsc/functions/{name}"

        os.makedirs(f"{path}/block_states", exist_ok=True)
        with open(f"{path}/l{l}_{i}.mcfunction", "w") as file:
            for item in group:
                if(l == 0):
                    if item in all_states:
                        properties = all_states[item][0]
                        default = all_states[item][1]

                        fcnID += 1
                        file.write(f"execute if block ~ ~ ~ {item} run function bsc:{name}/block_states/id{fcnID}\n")
                        with open(f"{path}/block_states/id{fcnID}.mcfunction", "w") as file1:
                            file1.write(f"data modify storage bsc out set value {{\"Name\":\"{item}\"}}\n")
                            for x in reversed(properties):
                                for y in properties[x]:
                                    if default[x] != y:
                                        file1.write(f"execute if block ~ ~ ~ {item}[{x}={y}] run data modify storage bsc out.Properties merge value {{{x}:\"{y}\"}}\n")

                    else:
                        file.write(f"execute if block ~ ~ ~ {item} run data modify storage bsc out set value {{\"Name\":\"{item}\"}}\n")
                else:
                    file.write(f"execute if block ~ ~ ~ #bsc:{item} run function bsc:{name}/{item}\n")
        
        return fcnID