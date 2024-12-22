# import libraries
import fitz  # PyMuPDF
import json

from PIL import Image

# file path you want to extract images from
file_path = "raw_data/HoiDongTuGiaoDanhSu.pdf"
image_dir = "data/hannom_images"
quocngu_file_name = "data/HDTGDS_extract_results.json"

# open the file
pdf_file = fitz.open(file_path)

quocngu_list = []

image_index = 1
text_index = 1

# iterate over PDF pages
for page_index in range(len(pdf_file)):

    if page_index not in range(13,171):
        continue

    # get the page itself
    page = pdf_file.load_page(page_index)  # load the page
    image_list = page.get_images(full=True)  # get images on the page

    # printing number of images found in this page
    if image_list:
        print(f"[+] Found a total of {len(image_list)} images on page {page_index}")

        # get the XREF of the image
        xref = image_list[0][0]

        # extract the image bytes
        base_image = pdf_file.extract_image(xref)
        image_bytes = base_image["image"]

        # get the image extension
        image_ext = base_image["ext"]

        # save the image
        image_name = f"{image_dir}/HoiDongTuGiaoDanhSu_page{image_index:03}.png"
        with open(image_name, "wb") as image_file:
            image_file.write(image_bytes)
            print(f"[+] Image saved as {image_name}")

        # increment the image index
        image_index += 1

    else:
        # if no images are found
        print("[!] No images found on page", page_index)
        page_text = page.get_text() + chr(12)
        
        lines = []

        dictionary_elements = page.get_text('dict')

        blocks = dictionary_elements['blocks'].copy()
        blocks.sort(key=lambda x: x['bbox'][1])

        for block in blocks:
            line_text = ''
            for line in block['lines']:
                for span in line['spans']:
                    line_text += ' ' + span['text']
                    lines.append(span['text'])

        quocngu_list.append({
            "page": page_index,
            "text": lines
        })

        text_index += 1

# save the quocngu_list to a json file
with open(quocngu_file_name, "w", encoding="utf-8") as quocngu_file:
    json.dump(quocngu_list, quocngu_file, ensure_ascii=False, indent=4)
