import os
complete = ""

for file in sorted(os.listdir("extracted_text")):
    if file == ".DS_Store":
        continue
    with open(f"extracted_text/{file}", "r") as f:
        text = f.read()
        complete += text


with open("extracted_text/complete_text.txt", "a") as f:
    f.write(complete)
