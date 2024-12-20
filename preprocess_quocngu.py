import json
import re

dir_path = "data"
quocngu_file_name = "quocngu_text.json"
output_file_name = "HDTGDS_clean.quocngu.json"

with open(f"{dir_path}/{quocngu_file_name}", "r", encoding = 'utf-8') as quocngu_file:
    quocngu_list = json.load(quocngu_file)

def is_quocngu(text):
    vietnamese_pattern = re.compile(r'[a-zA-ZàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ]')
    return bool(vietnamese_pattern.search(text))

def clean_text_with_re(text):
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text).lower()
    text = re.sub(r'\s+', ' ', text).strip()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

def clean_hannom_text(text):
    han_nom_pattern = re.compile(r'[\u4E00-\u9FFF\u3400-\u4DBF\u20000-\u2A6DF\u2A700-\u2B73F\u2B740-\u2B81F\u2B820-\u2CEAF\uF900-\uFAFF\u2F800-\u2FA1F]+')
    han_nom_text = han_nom_pattern.findall(text)
    return ''.join(han_nom_text)

cnt = 0

results = []

for quocngu_dict in quocngu_list:
    print(f"[+] Processing page {cnt + 1}")
    quocngu_texts = []
    hannom_texts = []
    cleaned_texts = []
    last_text = {}
    tmp_hannom = ""
    tmp_quocngu = ""
    for idx, text_line in enumerate(quocngu_dict['text']):
        if is_quocngu(text_line):
            # cleaned_text = clean_text_with_re(text_line)
            # if cleaned_text:
            #     tmp_quocngu += " " + cleaned_text
            
            tmp_quocngu += " " + text_line
        elif re.match(r"^\d+$", text_line):
            if idx == 0:
                continue
            if '\t' in tmp_hannom:
                last_text['hannom'] = clean_hannom_text(tmp_hannom.split('\t')[1])
                hannom_texts.append(clean_hannom_text(tmp_hannom.split('\t')[0]))
            else:
                hannom_texts.append(clean_hannom_text(tmp_hannom))
            # hannom_texts.append(tmp_hannom)
            if '\t' in tmp_quocngu:
                last_text['quocngu'] = clean_text_with_re(tmp_quocngu.split('\t')[1])
                quocngu_texts.append(clean_text_with_re(tmp_quocngu.split('\t')[0]))
            else:
                quocngu_texts.append(clean_text_with_re(tmp_quocngu))
            tmp_quocngu = ""
            tmp_hannom = ""
        else:
            tmp_hannom += " " + text_line

    for hannom_text, quocngu_text in zip(hannom_texts, quocngu_texts):
        cleaned_texts.append({
            "hannom": hannom_text,
            "quocngu": quocngu_text
        })

    if last_text:
        cleaned_texts.append(last_text)
        
    results.append({
        "file_name": f"HoiDongTuGiaoDanhSu_page{cnt + 1:03}.png",
        "length": len(cleaned_texts),
        "data": cleaned_texts,
    })
    cnt += 1

with open(f"{dir_path}/{output_file_name}", "w", encoding = 'utf-8') as output_file:
    json.dump(results, output_file, ensure_ascii=False, indent=4)