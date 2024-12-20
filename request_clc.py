import requests
import os
import json
from time import sleep

API_IMG_UPLOAD_URL = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-upload" # Upload image
API_IMG_DOWNLOAD_URL = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-download" # Download image
API_IMG_CLASSIFICATION_URL = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-classification" # Classification image
API_IMG_OCR_URL = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-ocr" # OCR image

# Hàm gửi yêu cầu POST
def send_post_request(api_url, files=None, json_data=None, headers=None):
    if headers is None:
        headers = {"User-Agent": "Custom-Agent/1.0"}
    
    try:
        if files:
            # Gửi yêu cầu với file (form-data)
            response = requests.post(api_url, headers=headers, files=files)
        elif json_data:
            # Gửi yêu cầu với JSON
            headers["Content-Type"] = "application/json"
            response = requests.post(api_url, headers=headers, json=json_data)
        else:
            return {"is_success": False, "message": "No files or JSON data provided"}
        
        # Xử lý phản hồi
        if response.status_code == 200:
            try:
                return response.json() 
            except ValueError:
                return {"is_success": False, "message": "Invalid JSON response"}
        else:
            return {
                "is_success": False,
                "message": f"HTTP Error {response.status_code}: {response.text}",
            }
    except Exception as e:
        return {"is_success": False, "message": str(e)}

# Hàm upload hình ảnh lên
def upload_image(api_url, image_path):
    try:
        with open(image_path, "rb") as image_file:
            files = {"image_file": image_file}
            return send_post_request(api_url, files=files) # file_name
    except FileNotFoundError:
        return {"is_success": False, "message": "Image file not found"}

# Hàm tải hình ảnh xuống
def download_image(api_url, file_name):
    """Tải hình ảnh từ API bằng phương thức GET với tham số file_name"""
    try:
        # Tạo URL với tham số file_name trong query string
        response = requests.get(f"{api_url}?file_name={file_name}")
        
        # Kiểm tra xem yêu cầu có thành công không
        if response.status_code == 200:
            return {
                "is_success": True,
                "image_data": response.content  # Lấy dữ liệu hình ảnh
            }
        else:
            return {
                "is_success": False,
                "message": f"HTTP Error {response.status_code}: {response.text}"
            }
    except Exception as e:
        return {"is_success": False, "message": str(e)}

# Hàm phân loại hình ảnh
def classification_image(api_url, file_name):
    json_classification = {
        "file_name": file_name
    }
    return send_post_request(api_url, json_data=json_classification) # ocr_id, ocr_name

# Hàm nhận dạng văn bản trong hình ảnh
def ocr_image(api_url, ocr_id, file_name):
    json_ocr = {
        "ocr_id": ocr_id,
        "file_name": file_name
    }
    return send_post_request(api_url, json_data=json_ocr) # result_file_name, result_ocr_text, result_bbox


folder_path = "data/hannom_images"
ocr_folder_path = "data/clc_ocr"
output_file_path = "data/clc_ocr_result.hannom.json"
results = []
# Tạo danh sách các file trong thư mục
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
files_ocr = [f.replace(".json", "") for f in os.listdir(ocr_folder_path) if os.path.isfile(os.path.join(ocr_folder_path, f))]

print(files_ocr)

cnt = 1

for file in files:
    print("[+] Processing file: {}".format(file))

    if file.split(".")[0].replace("HoiDongTuGiaoDanhSu_page","") in files_ocr:
        cnt+=1
        continue

    # Upload image
    image_file_path = os.path.join(folder_path, file)
    ocr_save_file_path = os.path.join(ocr_folder_path, f"{cnt:03}.json")
    upload_result = upload_image(API_IMG_UPLOAD_URL, image_file_path)
    file_name = upload_result['data']['file_name']

    # OCR image
    ocr_result = ocr_image(API_IMG_OCR_URL, 1 , file_name)

    results.append(ocr_result)

    with open(ocr_save_file_path, "w", encoding="utf-8") as json_file:
        json.dump(ocr_result, json_file, ensure_ascii=False, indent=4)

    if cnt % 2 == 0:
        sleep(60)

    cnt += 1

# Lưu kết quả vào tệp JSON
with open(output_file_path, "w", encoding="utf-8") as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)
    


