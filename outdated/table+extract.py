import os
import cv2
import numpy as np
from pdf2image import convert_from_path
import pytesseract

def filter_vertical_lines(lines, min_line_gap):
    lines.sort(key=lambda x: x[0][0])
    filtered_lines = [lines[0]]
    for i in range(1, len(lines)):
        if lines[i][0][0] - filtered_lines[-1][0][0] > min_line_gap:
            filtered_lines.append(lines[i])
    return filtered_lines

def split_image_at_line(image, line):
    x1, y1, x2, y2 = line[0]
    if y1 > y2:
        y1, y2 = y2, y1
    x = x1

    roi1 = image[:, :x]
    roi2 = image[:, x:]

    text1 = pytesseract.image_to_string(roi1)
    text2 = pytesseract.image_to_string(roi2)

    return text1, text2

def process_pdf(pdf_path, file):
    if not os.path.exists(f"temp_images/{file}"):
        os.makedirs(f"temp_images/{file}")

    images = convert_from_path(pdf_path, output_folder=f"temp_images/{file}", fmt="png")
    full_text = ""

    for image in sorted(os.listdir(f"temp_images/{file}")):
        img_path = f"temp_images/{file}/{image}"
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img_bin = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(img_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        p_width = img.shape[1]
        p_height = img.shape[0]
        masks = []

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if p_width * p_height * 0.05 < w * h < p_width * p_height * 0.9:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                roi = img[y:y + h, x:x + w]
                if not os.path.exists(f"temp_images/{file}/extracted_images"):
                    os.makedirs(f"temp_images/{file}/extracted_images")
                cv2.imwrite(f"temp_images/{file}/extracted_images/{image}.png", roi)
                mask = np.zeros(img.shape[:2], dtype="uint8")
                cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)
                masks.append(cv2.bitwise_not(mask))

        for mask in masks:
            result = cv2.bitwise_and(img, img, mask=mask)
            cv2.imwrite(f"temp_images/{file}/{image}", result)

        text_from_image = pytesseract.image_to_string(img_path)
        full_text += text_from_image

        if os.path.exists(f"temp_images/{file}/extracted_images"):
            for path in os.listdir(f"temp_images/{file}/extracted_images"):
                extimage_path = f"temp_images/{file}/extracted_images/{path}"
                extimage = cv2.imread(extimage_path)
                gray = cv2.cvtColor(extimage, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray, 50, 150, apertureSize=3)
                lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

                if lines is None:
                    continue

                vertical_lines = []
                for line in lines:
                    for x1, y1, x2, y2 in line:
                        angle = np.abs(np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi)
                        if 85 < angle < 95:
                            vertical_lines.append(line)

                if len(vertical_lines) > 0:
                    filtered_lines = filter_vertical_lines(vertical_lines, min_line_gap=20)
                    if len(filtered_lines) > 2:
                        filtered_lines = filtered_lines[1:-1]

                    for line in filtered_lines:
                        text1, text2 = split_image_at_line(extimage, line)
                        full_text += "\n--- Table Start ---\n"
                        full_text += text1 + "\n"
                        full_text += text2 + "\n"
                        full_text += "--- Table End ---\n"

    return full_text

if __name__ == "__main__":
    output_texts = {}
    for file in os.listdir("flattened_pdfs"):
        pdf_path = os.path.join("flattened_pdfs", file)
        full_text = process_pdf(pdf_path, file)
        output_texts[file] = full_text
        print(full_text)

    if not os.path.exists("extracted_text"):
        os.makedirs("extracted_text")

    for file, text in output_texts.items():
        with open(f"extracted_text/{file}.txt", "w", encoding="utf-8") as f:
            f.write(text)