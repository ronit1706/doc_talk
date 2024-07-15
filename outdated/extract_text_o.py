import os
import pytesseract
import table_mgmt


for folder in os.listdir("temp_images"):

    if folder == ".DS_Store":
        continue

    elif os.path.isdir(f"temp_images/{folder}"):
        file = open(f"extracted_text/{folder}.txt", "a")
        for image in (sorted(os.listdir(f"temp_images/{folder}/"))):
            if os.path.isfile(f"temp_images/{folder}/{image}"):
                print(f"{image}")
                text = pytesseract.image_to_string(f"temp_images/{folder}/{image}")
                file.write(text)

    dict= {}
    if os.path.exists(f"temp_images/{folder}/extracted_images/split_images"):
        for image in sorted(os.listdir(f"temp_images/{folder}/extracted_images/split_images")):
            if os.path.isdir(f"temp_images/{folder}/extracted_images/split_images/" + image):
                for split_image in sorted(os.listdir(f"temp_images/{folder}/extracted_images/split_images/" + image)):
                    if os.path.isfile(f"temp_images/{folder}/extracted_images/split_images/{image}/" + split_image):
                        print(f"{split_image}")
                        if split_image not in dict:
                            dict[split_image] = pytesseract.image_to_string(f"temp_images/{folder}/extracted_images/split_images/{image}/{split_image}")
                        else:
                            dict[split_image] += pytesseract.image_to_string(f"temp_images/{folder}/extracted_images/split_images/{image}/{split_image}")

    for key in dict:
        file.write(dict[key])

    os.system(f"rm -rf \"temp_images/{folder}\"")