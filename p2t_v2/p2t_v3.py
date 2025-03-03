import pdfplumber

def extract_text_with_lines(pdf_path):
    """
    PDF에서 본문 텍스트를 줄 단위로 병합하여 추출
    """
    extracted_text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 페이지 내 모든 텍스트 가져오기
            words = page.extract_words()  # 단어별로 추출
            lines = group_words_into_lines(words)  # 단어들을 줄 단위로 병합
            extracted_text.extend(lines)  # 결과 저장

    return "\n".join(extracted_text)

def group_words_into_lines(words):
    """
    단어 리스트를 줄 단위로 병합
    """
    lines = []
    current_line = []
    current_y = None

    for word in words:
        # y 좌표(텍스트 줄 높이) 기준으로 같은 줄인지 확인
        if current_y is None or abs(word['top'] - current_y) < 5:  # 같은 줄이면
            current_line.append(word['text'])
        else:  # 새로운 줄이면
            lines.append(" ".join(current_line))
            current_line = [word['text']]

        current_y = word['top']  # 현재 y 좌표 갱신

    # 마지막 줄 추가
    if current_line:
        lines.append(" ".join(current_line))

    return lines

# PDF 파일 경로 설정
pdf_path = "현대차증권_131031_3.pdf"

# 본문 텍스트 추출
main_text = extract_text_with_lines(pdf_path)

# 결과 출력 또는 저장
print(main_text)

# 파일로 저장 (선택 사항)
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(main_text)
