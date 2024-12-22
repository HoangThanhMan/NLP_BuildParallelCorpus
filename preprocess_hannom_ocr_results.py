import json

input_file_path = "data/HDTGDS_ocr_result.hannom.json"
output_file_path = "data/HDTGDS_clean.hannom.json"

with open(input_file_path, "r", encoding="utf-8") as json_file:
    ocr_data = json.load(json_file)

results = []

for item in ocr_data:
    print(f"[+] Processing file: {item['file_name']}")
    file_name = item["file_name"]
    text_lines = item["data"]['text_lines']

    data = []

    for text_line in text_lines:
        data.append({
            "text": text_line["text"],
            "position": text_line["position"]
        })

    results.append({
        "file_name": file_name,
        "length": len(data),
        "data": data
    })

with open(output_file_path, "w", encoding="utf-8") as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)

