import json
def load():
    with open("devices.json", "r") as file:
            return json.load(file)
        except FileNotFoundError:
            data = {"devices": []}
            
            with open("devices.json", "w") as file:
                json.dump(data, file, indent=4)
            return data

def add():
    data = load()

    exist = any(
            d["username"] == device["username"]
            and d["host"] == device["host"]
            and d["port"] == device["port"]
            for d in data["devices"]
            )
    if exist:
        return False

    data["devices"].append(device)

    with open("devices.json", "w") as file: 
        json.dump(data, file, ident=4)
    return True



