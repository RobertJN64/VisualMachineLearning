import json

def run():
    file = ""
    with open("ReportSettings/defconfig.json") as f:
        defconfig = json.load(f)
    running = True
    while running:
        block = input("Add block (/finish, /help): ")
        if block == "/finish":
            running = False

        elif block == "/help":
            print("Choose a block from one of the following: ")
            print(list(defconfig.keys()))

        elif block in defconfig:
            config = {}
            print("Block has following config options: ")
            print(list(defconfig[block].keys()))
            yn = input("Edit? y/n ")
            if yn == "y":
                for item in defconfig[block]:
                    newsetting = input(item + ": " + str(defconfig[block][item]) + " -> ")
                    if newsetting != "":
                        config[item] = newsetting
            file += block
            if config != {}:
                #TODO - handle json dump properly
                file += " | " + json.dumps(config)
            file += "\n"

        elif block not in defconfig:
            print("Block ", str(block), " not found. Try /help")
    print(file)
    with open("ReportSettings/CustomTemplate.txt", "w") as f:
        f.writelines(file)