import json



def sort():
    with open("mappings.json","r") as f:
        content = json.load(f)

    sort_content =  dict(sorted(content.items(),key=lambda item: float(item[0])))

    with open ("mappings_sort.json","w") as f:
        json.dump(sort_content,f,indent=4)
    
def remove_empty():
    with open("mappings.json") as f:
        content = json.load(f)
        cop = content.copy()
        
        for entry in cop.items():
            if entry[1] == "":
                content.pop(entry[0])
    
    with open("mappings.json","w") as f:
        json.dump(content,f,indent=3)

sort()