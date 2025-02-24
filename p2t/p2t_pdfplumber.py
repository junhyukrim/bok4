import pdfplumber

def pdf_to_txt_with_pdfplumber(pdf_path, txt_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"  # per page
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

# path
pdf_path = "제26차 금통위 의사록.pdf"
txt_path = "bok_minute_pdfplumber.txt"

# exe
pdf_to_txt_with_pdfplumber(pdf_path, txt_path)