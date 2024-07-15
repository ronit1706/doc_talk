import os
import cv2
import numpy as np
from pdf2image import convert_from_path

def filter_vertical_lines(lines, min_line_gap):
    lines.sort(key=lambda x: x[0][0])
    filtered_lines = [lines[0]]
    for i in range(1, len(lines)):
        if lines[i][0][0] - filtered_lines[-1][0][0] > min_line_gap:
            filtered_lines.append(lines[i])
    return filtered_lines

def split_image_at_line(image, line, path, file):
    x1, y1, x2, y2 = line[0]
    if y1 > y2:
        y1, y2 = y2, y1
    x = x1

    roi1 = image[y1:y2, :x]
    roi2 = image[y1:y2, x:]

    if not os.path.exists(f"temp_images/{file}/extracted_images/split_images"):
        os.makedirs(f"temp_images/{file}/extracted_images/split_images")

    if not os.path.exists(f"temp_images/{file}/extracted_images/split_images/{path}"):
        os.makedirs(f"temp_images/{file}/extracted_images/split_images/{path}/")
    cv2.imwrite(f"temp_images/{file}/extracted_images/split_images/{path}/roi1.png", roi1)
    cv2.imwrite(f"temp_images/{file}/extracted_images/split_images/{path}/roi2.png", roi2)

def process_pdf(pdf_path, file):
    loc = {}

    if not os.path.exists(f"temp_images/{file}"):
        os.makedirs(f"temp_images/{file}")

    images = convert_from_path(pdf_path, output_folder=f"temp_images/{file}", fmt="png")

    for image in sorted(os.listdir(f"temp_images/{file}")):
        img = cv2.imread(f"temp_images/{file}/{image}")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        p_width = img.shape[1]
        p_height = img.shape[0]
        uniq = 1000
        masks = []

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if p_width * p_height * 0.05 < w * h < p_width * p_height * 0.8:
                uniq -= 1
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                roi = img[y:y + h, x:x + w]
                if not os.path.exists(f"temp_images/{file}/extracted_images"):
                    os.makedirs(f"temp_images/{file}/extracted_images")
                cv2.imwrite(f"temp_images/{file}/extracted_images/{image}{uniq}.png", roi)
                img = cv2.imread(f"temp_images/{file}/{image}")
                mask = np.zeros(img.shape[:2], dtype="uint8")
                cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)
                masks.append(cv2.bitwise_not(mask))
                if image in loc:
                    loc[image][uniq] = (x, y)
                else:
                    loc[image] = {uniq:(x,y)}


        for mask in masks:
            img = cv2.imread(f"temp_images/{file}/{image}")
            result = cv2.bitwise_and(img, img, mask=mask)
            cv2.imwrite(f"temp_images/{file}/{image}", result)

    if os.path.exists(f"temp_images/{file}/extracted_images"):

        for path in os.listdir(f"temp_images/{file}/extracted_images"):
            extimage = cv2.imread(f"temp_images/{file}/extracted_images/{path}")
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
                filtered_lines.pop(0)
                filtered_lines.pop(-1)

                for line in filtered_lines:
                    split_image_at_line(extimage, line, path, file)
                    if not os.path.exists(f"temp_images/{file}/extracted_images/line"):
                        os.makedirs(f"temp_images/{file}/extracted_images/line")
                    cv2.imwrite(f"temp_images/{file}/extracted_images/line/{path}", extimage)

    return loc

if __name__ == "__main__":
    all_loc = {}
    for file in os.listdir("flattened_pdfs"):
        pdf_path = "flattened_pdfs/" + file
        loc = process_pdf(pdf_path, file)
        all_loc[file] = loc
        print(all_loc)
