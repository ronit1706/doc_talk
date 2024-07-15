import os
import pytesseract
from table_mgmt import process_pdf
import glob
import cv2

all_loc = {}

for file in os.listdir("flattened_pdfs"):
    pdf_path = "flattened_pdfs/" + file
    if file + ".txt" not in os.listdir("extracted_text"):

        loc = process_pdf(pdf_path, file)
        all_loc[file] = loc
        print(all_loc)

print("---------------------------------------------")

def split_image_at_y(y, path, file):
    img = cv2.imread(f"temp_images/{file}/{path}")
    roi1 = img[:y]
    roi2 = img[y:]
    if not os.path.exists(f"temp_images/{file}/extracted_images/upper_lower"):
        os.makedirs(f"temp_images/{file}/extracted_images/upper_lower")
    if not os.path.exists(f"temp_images/{file}/extracted_images/upper_lower/{path}"):
        os.makedirs(f"temp_images/{file}/extracted_images/upper_lower/{path}/")
    cv2.imwrite(f"temp_images/{file}/extracted_images/upper_lower/{path}/roi1.png", roi1)
    cv2.imwrite(f"temp_images/{file}/extracted_images/upper_lower/{path}/roi2.png", roi2)




for folder in os.listdir("temp_images"):

    if folder == ".DS_Store":
        continue
    elif os.path.exists(f"extracted_text/{folder}.txt"):
        continue
    elif os.path.isdir(f"temp_images/{folder}"):
        table_pages = all_loc[folder].keys()
        loc = all_loc[folder]
        file = open(f"extracted_text/{folder}.txt", "a")
        for image in (sorted(os.listdir(f"temp_images/{folder}/"))):
            if os.path.isfile(f"temp_images/{folder}/{image}"):
                for path in sorted(glob.glob(f"temp_images/{folder}/extracted_images/split_images/{image}*")):
                    if os.path.exists(path):
                        path = path.replace(f"temp_images/{folder}/extracted_images/split_images/{image}", "")
                        uniq = path.replace(".png", "")
                        page = image[-6:-4]
                        x, y = loc[image][int(uniq)]
                        print(f"page: {page} uniq: {uniq} loc: {x} {y}")
                        split_image_at_y(y, image, folder)
                        print(f"Image = {image}")
                        print(f"Path = {path}")
                        upper = cv2.imread(f"temp_images/{folder}/extracted_images/upper_lower/{image}/roi1.png")
                        lower = cv2.imread(f"temp_images/{folder}/extracted_images/upper_lower/{image}/roi2.png")
                        table_part1 = cv2.imread(f"temp_images/{folder}/extracted_images/split_images/{image}{uniq}.png/roi1.png")
                        table_part2 = cv2.imread(f"temp_images/{folder}/extracted_images/split_images/{image}{uniq}.png/roi2.png")
                        upper_text = pytesseract.image_to_string(upper)
                        table_text = pytesseract.image_to_string(table_part1)
                        table_text += pytesseract.image_to_string(table_part2)
                        lower_text = pytesseract.image_to_string(lower)

                        file.write(upper_text+table_text+lower_text)

                if image not in table_pages:
                    img = cv2.imread(f"temp_images/{folder}/{image}")
                    text = pytesseract.image_to_string(img)
                    file.write(text)
