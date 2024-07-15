import os
import cv2
import numpy as np
from pdf2image import convert_from_path
import pytesseract


def convert_pdf_to_images(pdf_path, output_folder):
    images = convert_from_path(pdf_path, output_folder=output_folder, fmt='png')
    return images


def ocr_image(image_path):
    return pytesseract.image_to_string(image_path)


def detect_tables(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

    # Detect horizontal and vertical lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    detect_horizontal = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    detect_vertical = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel, iterations=2)

    # Combine horizontal and vertical lines
    table_structure = cv2.add(detect_horizontal, detect_vertical)

    contours, _ = cv2.findContours(table_structure, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    table_bboxes = [cv2.boundingRect(contour) for contour in contours]

    return table_bboxes


def extract_table(image, bbox):
    x, y, w, h = bbox
    return image[y:y + h, x:x + w]


def save_extracted_text(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)


def process_pdf(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    images = convert_pdf_to_images(pdf_path, output_folder)
    text_with_tables = ""
    tables_info = []

    for i, image in enumerate(images):
        image_path = f"{output_folder}/page_{i + 1}.png"
        image.save(image_path)
        text = ocr_image(image_path)

        img = cv2.imread(image_path)
        table_bboxes = detect_tables(img)
        for j, bbox in enumerate(table_bboxes):
            table_img = extract_table(img, bbox)
            table_img_path = f"{output_folder}/table_{i + 1}_{j + 1}.png"
            cv2.imwrite(table_img_path, table_img)
            table_text = ocr_image(table_img_path)
            tables_info.append((i + 1, bbox, table_text))

        # Insert markers for table positions
        for j, bbox in enumerate(table_bboxes):
            x, y, w, h = bbox
            text_with_tables += f"\n--- Table Start (Page {i + 1}, Table {j + 1}) ---\n{table_text}\n--- Table End (Page {i + 1}, Table {j + 1}) ---\n"

        # Add the main text
        text_with_tables += text + "\n"

    # Combine main text with tables
    final_text = ""
    for page_num, bbox, table_text in tables_info:
        # Insert table text at the appropriate location in the main text
        table_marker = f"\n--- Table Start (Page {page_num}) ---\n"
        table_marker += table_text
        table_marker += f"\n--- Table End (Page {page_num}) ---\n"

        # Insert table content at the placeholder location
        text_with_tables = text_with_tables.replace("--- Table Placeholder ---", table_marker, 1)

    return text_with_tables


if __name__ == "__main__":
    pdf_folder = "flattened_pdfs"
    output_folder = "extracted_text"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            temp_output_folder = os.path.join(output_folder, os.path.splitext(pdf_file)[0])
            extracted_text = process_pdf(pdf_path, temp_output_folder)
            output_path = os.path.join(output_folder, f"{os.path.splitext(pdf_file)[0]}.txt")
            save_extracted_text(extracted_text, output_path)
            print(f"Extracted and saved: {output_path}")