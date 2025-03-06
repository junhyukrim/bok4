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


input_folder = "인풋폴더"
output_folder = "아웃풋폴더"
os.makedirs(output_folder, exist_ok=True)

total_unique_doc_ids = set()
total_negative_doc_ids = set()
total_positive_doc_ids = set()
total_neutral_doc_ids = set()

for file_name in os.listdir(input_folder):
    if file_name.endswith(".csv"):
        file_path = os.path.join(input_folder, file_name)
        df = pd.read_csv(file_path)

        total_unique_doc_ids.update(df['doc_id'].unique())
        total_negative_doc_ids.update(df[df['market_label'] == -1]['doc_id'].unique())
        total_positive_doc_ids.update(df[df['market_label'] == 1]['doc_id'].unique())
        total_neutral_doc_ids.update(df[df['market_label'] == 0]['doc_id'].unique())

        output_data = {
            "Unique doc_id count": [len(total_unique_doc_ids)],
            "Dovish_count": [len(total_negative_doc_ids)],
            "Hawkish_count": [len(total_positive_doc_ids)],
            "Netural_count": [len(total_neutral_doc_ids)]
        }

        output_df = pd.DataFrame(output_data)

        output_file_path = os.path.join(output_folder, "total_output_counts.csv")
        output_df.to_csv(output_file_path, index=False)

        print(f"Results saved to {output_file_path}")