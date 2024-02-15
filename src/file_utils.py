import json


class FileUtils():

    def read_json(current_directory):
        file_path = current_directory + "/data/leaders.json"
        with open(file_path, "r") as file:
            data = json.load(file)
        print(data)