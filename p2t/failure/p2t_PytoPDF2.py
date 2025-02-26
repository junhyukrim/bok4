from PyPDF2 import PdfReader

def pdf_to_txt(pdf_path, txt_path):
    # open PDF
    reader = PdfReader(pdf_path)
    
    # text var
    text = ""
    
    # text extract
    for page in reader.pages:
        text += page.extract_text()
    
    # text var to .txt
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

# PDF 파일 경로와 저장할 TXT 파일 경로
pdf_path = "제26차 금통위 의사록.pdf"
txt_path = "bok_minute_001.txt"

# 함수 실행
pdf_to_txt(pdf_path, txt_path)
