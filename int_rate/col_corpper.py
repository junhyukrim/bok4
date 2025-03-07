import pandas as pd

# CSV 파일 경로 (사용자가 제공한 파일 이름으로 변경)
input_csv_path = "base_rate.csv"  # 제공된 CSV 파일명을 여기에 입력하세요
output_csv_path = "base_rate_cropped.csv"


try:
    # CSV 파일 읽기
    data = pd.read_csv(input_csv_path)

    # 열 이름 출력
    print("CSV 파일의 열 이름:", data.columns.tolist())
except Exception as e:
    print(f"오류가 발생했습니다: {e}")


try:
    # CSV 파일 읽기
    data = pd.read_csv(input_csv_path)
    
    # 'date'와 'market_rate' 열만 선택
    cropped_data = data[["date", "base_rate"]]

    # 선택된 데이터를 새로운 CSV 파일로 저장
    cropped_data.to_csv(output_csv_path, index=False, encoding="utf-8-sig")

    print(f"결과가 성공적으로 저장되었습니다: {output_csv_path}")

except FileNotFoundError:
    print(f"파일을 찾을 수 없습니다: {input_csv_path}. 올바른 경로를 확인하세요.")
except KeyError as e:
    print(f"필요한 열이 없습니다: {e}. CSV 파일의 열 이름을 확인하세요.")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")
