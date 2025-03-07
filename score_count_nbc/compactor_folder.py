import os
import pandas as pd

def process_columns(input_path, output_path):
    """
    특정 열 필터링 및 순서 변경 후 CSV 파일 저장.

    :param input_path: 원본 CSV 파일 경로
    :param output_path: 수정된 CSV 파일 저장 경로
    """
    # CSV 파일 로드
    df = pd.read_csv(input_path)

    # 필요한 열만 남기기
    columns_to_keep = [
        'doc_id', 'date', 'original_sentence'
    ]
    df_filtered = df[columns_to_keep]

    # 열 순서 변경
    columns_order = [
        'date', 'doc_id', 'original_sentence'
    ]
    df_reordered = df_filtered[columns_order]

    # 결과 저장
    df_reordered.to_csv(output_path, index=False)
    print(f"결과가 {output_path}에 저장되었습니다.")

def process_folder(input_folder, output_folder):
    """
    폴더 내 모든 CSV 파일에 대해 열 필터링 및 순서 변경 작업 수행.

    :param input_folder: 입력 폴더 경로
    :param output_folder: 출력 폴더 경로
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            process_columns(input_path, output_path)

# 사용 예시
if __name__ == "__main__":
    input_folder = "D:/bok4_resource/news_labeled/파이낸셜최종라벨"  # 입력 폴더 경로
    output_folder = "D:/bok4_resource/news_labeled/파이낸셜최종라벨compact"  # 출력 폴더 경로

    process_folder(input_folder, output_folder)
