import pandas as pd
import os

def count_unique_docs(df):
    """
    doc_id를 기준으로 unique doc_id의 개수를 반환하는 함수
    """
    return df['doc_id'].nunique()

def count_docs_with_label(df, label):
    """
    특정 market_label 값을 가지는 unique doc_id의 개수를 반환하는 함수
    """
    return df[df['market_label'] == label]['doc_id'].nunique()


input_folder = "작업할 폴더명 입력하세요"
output_folder = "결과물이 들어갈 폴더명을 입력하세요"
os.makedirs(output_folder, exist_ok=True)

for file_name in os.listdir(input_folder):
    if file_name.endswith(".csv"):
        file_path = os.path.join(input_folder, file_name)
        df = pd.read_csv(file_path)

        unique_doc_count = count_unique_docs(df)
        negative_doc_count = count_docs_with_label(df, -1)
        positive_doc_count = count_docs_with_label(df, 1)

        output_data = {
            "Unique doc_id count": [unique_doc_count],
            "Dovish_count": [negative_doc_count],
            "Hawkish_count": [positive_doc_count]
        }

        output_df = pd.DataFrame(output_data)

        output_file_name = f"output_counts_{file_name}"
        output_file_path = os.path.join(output_folder, output_file_name)
        output_df.to_csv(output_file_path, index=False)

        print(f"Results saved to {output_file_path}")