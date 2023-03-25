import requests
import json
import math
import os
import ast

class ScoresScript():
    def __init__(self, root):
        self.root = root

    
    def generate(self,page,root):
        code = page.txt_code.get("1.0", "end")
        # safely evaluate input string (automatic escapes)
        parsed_code = ast.parse(code)
        compiled_code = compile(parsed_code, "<string>", "exec")

        end = int(page.ent_end.get())
        start = int(page.ent_start.get())
        
        player    = str(page.ent_player.get())
        objective = str(page.ent_objective.get())
        namespace = str(page.ent_namespace.get())
        folder    = str(page.ent_folder.get())

        path = f"{self.root.output_path}/{namespace}/functions/{folder}"

        n = end-start+1
        b = 8

        progress = 0
        progress_max = math.ceil(n / (b-1)) # file count


        # create folder for tree
        levels = math.floor(math.log(n)/math.log(b)) + 1
        os.makedirs(path, exist_ok=True)
        for l in range(1,levels+1):
            size = pow(b,l)
            size_p = pow(b,l-1)
            for i in range(0,size*math.ceil(n / size) - 1, size):
                if(l != levels):
                    with open(f"{path}/l{l-1}_{i + start}.mcfunction", "w") as file:
                        progress += 1
                        page.pb.update(100*progress/progress_max)
                        root.update_idletasks()
                        for j in range(i,i+size,size_p):
                            if(j < n):
                                if(l==1):
                                    inputs = {'score': int(j + start)}
                                    try:
                                        exec(compiled_code, globals(), inputs)
                                        file.write(f"execute if score {player} {objective} matches {j + start} run {inputs.get('out')}\n")
                                    except (SyntaxError, ValueError):
                                        print('ERROR')
                                else:
                                    file.write(f"execute if score {player} {objective} matches {j + start}..{j + size_p - 1 + start} run function {namespace}:{folder}/l{str(l-2)}_{str(j + start)}\n")
                else:
                    with open(f"{path}/root.mcfunction", "w") as file:
                        for j in range(i,i+size-1,size_p):
                            if(j < n):
                                file.write(f"execute if score {player} {objective} matches {j + start}..{j + size_p - 1 + start} run function {namespace}:{folder}/l{str(l-2)}_{str(j + start)}\n") 

