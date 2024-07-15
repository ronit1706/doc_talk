from unstructured.partition.pdf import partition_pdf
from tabula import read_pdf

fname = "flattened_pdfs/Jan Swasthaya Beema Yojana Policy Wording.pdf"

elements = partition_pdf(filename=fname,
                         infer_table_structure=True,
                         strategy='hi_res',)

tables = [el for el in elements if el.category == "Table"]


dictionary = tables[0].to_dict()

print(dictionary, tables[1].to_dict())

