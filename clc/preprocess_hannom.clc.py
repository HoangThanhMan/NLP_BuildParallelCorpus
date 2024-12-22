import json
import re

input_file_path = "data/clc_ocr_result.hannom.json"
output_file_path = "data/HDTGDS_clean.hannom.clc.json"

with open(input_file_path, "r", encoding="utf-8") as json_file:
    ocr_data = json.load(json_file)

results = []

for item in ocr_data:
    print(f"[+] Processing file: {item['data']['details']['file_name']}")
    file_name = item["data"]['details']['file_name']
    details = item["data"]['details']['details']

    data = []
    for detail in details:
        data.append({
            "text": detail["transcription"],
            "position": detail["points"]
        })
    
    results.append({
        "file_name": file_name,
        "length": len(data),
        "data": data
    })

with open(output_file_path, "w", encoding="utf-8") as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)