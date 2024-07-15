from pdf2image import convert_from_path
from tabula import read_pdf
from img2table.document import Image as im
from tabulate import tabulate
import pytesseract
import os
import cv2
import numpy as np
from PIL import Image
import tabula
from img2table.document import Image
from img2table.ocr import TesseractOCR



n = len([name for name in os.listdir("flattened_pdfs") if os.path.isfile(os.path.join("flattened_pdfs",name))])

for file in os.listdir("flattened_pdfs"):
    pdf_path = "flattened_pdfs/" + file
    if not os.path.exists(f"temp_images/{file}"):
        os.mkdir(f"temp_images/{file}")



    images = convert_from_path(pdf_path, output_folder=f"temp_images/{file}", fmt="png")

    for image in os.listdir(f"temp_images/{file}"):
        img = cv2.imread(f"temp_images/{file}/{image}")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours,hierarchy = cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            if w*h > 100000 and w<1656:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                roi = img[y:y+h, x:x+w]
                if not os.path.exists(f"temp_images/{file}/extracted_images"):
                    os.mkdir(f"temp_images/{file}/extracted_images")
                cv2.imwrite(f"temp_images/{file}/extracted_images/{image}", roi)

    for path in os.listdir(f"temp_images/{file}/extracted_images"):
        extimage = cv2.imread(f"temp_images/{file}/extracted_images/{path}")
        gray = cv2.cvtColor(extimage, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 2, 400, None, 10, 100);
        for line in lines[0]:
            pt1 = (line[0], line[1])
            pt2 = (line[2], line[3])
            cv2.line(extimage, pt1, pt2, (0, 0, 255), 3)
        if not os.path.exists(f"temp_images/{file}/extracted_images/line"):
            os.mkdir(f"temp_images/{file}/extracted_images/line")
        cv2.imwrite(f"temp_images/{file}/extracted_images/line/{path}", extimage)

