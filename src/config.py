import json
config = open("node\src\config\config.json")
data = json.load(config)
mongo_host = data["comunication"]["mongo"]["ip"]
mongo_port = data["comunication"]["mongo"]["port"]
flask_host = data["comunication"]["flask"]["ip"]
flask_port = data["comunication"]["flask"]["port"]
address = data["device"]["address"]
mine_status = data["device"]["mining"]