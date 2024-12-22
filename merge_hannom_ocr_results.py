import json 
import os
from natsort import natsorted

folder_path = "data/kandianguji_ocr"

files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

results = []

for file in files:
    print("[+] Processing file: {}".format(file))
    file_path = os.path.join(folder_path, file)

    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        data["file_name"] =file.replace(".json", ".png")
        results.append(data)


new_results = natsorted(results, key=lambda x: x["file_name"])

output_file_path = "data/HDTGDS_ocr_result.hannom.json"
with open(output_file_path, "w", encoding="utf-8") as json_file:
    json.dump(new_results, json_file, ensure_ascii=False, indent=4)
