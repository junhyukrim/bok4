import os

def modify_text_file(file_path, output_path, target_list):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    start_index = 0
    for i, line in enumerate(lines):
        if any(target in line for target in target_list):
            start_index = i
            break

    modified_lines = lines[:start_index]

    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(modified_lines)

def process_folder(input_folder, output_folder, target_list):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_tail_removed.txt")
            modify_text_file(input_path, output_path, target_list)

if __name__ == "__main__":
    input_folder = "D:/download/txt_bok_min-20250307T015930Z-001/txt_bok_min/content_only/토의결론O"
    output_folder = "D:/download/txt_bok_min-20250307T015930Z-001/txt_bok_min/content_only/토의결론O/tail_remove"
    target_characters = [") 토의결론"]

    process_folder(input_folder, output_folder, target_characters)
