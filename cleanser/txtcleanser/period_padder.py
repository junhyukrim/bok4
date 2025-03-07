import os

def replace_words_in_file(input_file, output_file, word_replacements, additional_replacements):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # 단어 대체
    for key, value in word_replacements.items():
        content = content.replace(key, value)

    # 추가 대체 (예: .. -> .)
    for key, value in additional_replacements.items():
        content = content.replace(key, value)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)

def process_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    word_replacements = {'었음':'었음.', '했음':'했음.', '였음':'였음.', '보임':'보임.','있음':'있음.','없음':'없음음.'}
    additional_replacements = {'..':'.'}

    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            replace_words_in_file(input_path, output_path, word_replacements, additional_replacements)

# 사용 예시
if __name__ == "__main__":
    input_folder = "D:/download/txt_bok_min-20250307T015930Z-001/txt_bok_min/content_only"  # 입력 폴더 경로
    output_folder = "D:/download/txt_bok_min-20250307T015930Z-001/txt_bok_min/content_only/cleansed"  # 출력 폴더 경로

    process_folder(input_folder, output_folder)
