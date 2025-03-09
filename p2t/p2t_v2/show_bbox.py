import pdfplumber
from PIL import Image, ImageDraw

def visualize_bbox_on_pdf(pdf_path, page_number, bbox, output_image_path="bbox_visualized.png"):
    """
    지정된 PDF 페이지에서 bbox 영역을 시각적으로 표시하여 이미지로 저장.

    :param pdf_path: PDF 파일 경로
    :param page_number: 확인할 페이지 번호 (0부터 시작)
    :param bbox: 강조할 영역 좌표 (x0, y0, x1, y1)
    :param output_image_path: bbox가 표시된 이미지 저장 경로
    """
    with pdfplumber.open(pdf_path) as pdf:
        if page_number < 0 or page_number >= len(pdf.pages):
            print(f"페이지 번호 {page_number}는 유효하지 않습니다.")
            return None

        # 특정 페이지 선택
        page = pdf.pages[page_number]

        # pdf 페이지 크기 가져오기
        pdf_width = page.width
        pdf_height = page.height

        # PDF 페이지를 이미지로 변환 (Pillow Image 객체)
        img = page.to_image(resolution=300).original
        img_width, img_height = img.size  # 변환된 이미지 크기

        # PDF 좌표계를 이미지 좌표계로 변환 (y축 변환 필요)
        scale_x = img_width / pdf_width
        scale_y = img_height / pdf_height

        x0, y0, x1, y1 = bbox
        new_x0 = x0 * scale_x
        new_y0 = img_height - (y1 * scale_y)  # PDF 좌표계를 이미지 좌표계로 변환
        new_x1 = x1 * scale_x
        new_y1 = img_height - (y0 * scale_y)

        new_bbox = (new_x0, new_y0, new_x1, new_y1)

        # bbox를 빨간색 테두리로 강조
        draw = ImageDraw.Draw(img)
        draw.rectangle(new_bbox, outline="red", width=5)  # 빨간색 테두리

        # bbox가 강조된 이미지 저장
        img.save(output_image_path)
        print(f"📌 bbox가 강조된 페이지 이미지 저장 완료: {output_image_path}")

# PDF 파일 경로
pdf_path = "160912_LIG투자증권_1.pdf"

# 확인할 페이지 번호 (0부터 시작)
page_number = 0

# 강조할 bbox 영역 좌표 (x0, y0, x1, y1) - PDF 좌표계 기준 (텍스트 영역)
bbox = (50, 500, 540, 650)  # 좌표는 PDF 레이아웃에 따라 조정 필요

# bbox 영역을 시각적으로 강조하여 이미지 저장
visualize_bbox_on_pdf(pdf_path, page_number, bbox)