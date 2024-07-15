from pdf2image import convert_from_path
from tabula import read_pdf
from img2table.document import Image as im
from tabulate import tabulate
import pytesseract
import os
import cv2
from PIL import Image
import tabula

from img2table.document import PDF
from img2table.ocr import TesseractOCR




n = len([name for name in os.listdir("flattened_pdfs") if os.path.isfile(os.path.join("flattened_pdfs",name))])

for file in os.listdir("flattened_pdfs"):
    pdf_path = "flattened_pdfs/" + file
    if not os.path.exists(f"temp_images/{file}"):
        os.mkdir(f"temp_images/{file}")

    pdf = PDF(src=pdf_path)
    p = pdf.pages[0]
    print(p.width)
    tables = pdf.extract_tables(ocr = TesseractOCR(lang="eng"))

    print(tables)
    # for id_row, row in enumerate(table.content.values()):
    #     for id_col, cell in enumerate(row):
    #         x1 = cell.bbox.x1
    #         y1 = cell.bbox.y1
    #         x2 = cell.bbox.x2
    #         y2 = cell.bbox.y2
    #         value = cell.value



    # images = convert_from_path(pdf_path, output_folder=f"temp_images/{file}", fmt="png")
    #
    # for image in os.listdir(f"temp_images/{file}"):
    #     img = cv2.imread(f"temp_images/{file}/{image}")
    #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #     _, img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    #     contours,hierarchy = cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    #     for cnt in contours:
    #         x,y,w,h = cv2.boundingRect(cnt)
    #         if w*h > 100000 and w<1656:
    #             cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    #             roi = img[y:y+h, x:x+w]
    #             if not os.path.exists(f"temp_images/{file}/extracted_images"):
    #                 os.mkdir(f"temp_images/{file}/extracted_images")
    #             cv2.imwrite(f"temp_images/{file}/extracted_images/{image}", roi)
    #
    # for path in os.listdir(f"temp_images/{file}/extracted_images"):
    #     extimage = im(src = f"temp_images/{file}/extracted_images/{path}")
    #     image_tables = extimage.extract_tables()
    #
    #     print(image_tables)
    #     # for image in os.listdir(f"temp_images/{file}/extracted_images"):
    #     #     img = Image.open(f"temp_images/{file}/extracted_images/{image}")
    #     #     tabula.convert_into(f"temp_images/{file}/extracted_images/{image}", f"extracted_text/{file}.csv", output_format="csv")
    #     # #
    #     # for page_num, img in enumerate(images):
    #     #     text = pytesseract.image_to_string(img)
    #     #     f = open("extracted_text/"+file+".txt","a")
    #     #     f.write(f"Page {page_num + 1}:\n{text}\n")
