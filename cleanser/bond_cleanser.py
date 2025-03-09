import re
import os
import glob

def process_text_file(file_path, output_path, word_list):
    """
    텍스트 파일을 주어진 규칙에 따라 수정하여 저장합니다.

    Args:
        file_path (str): 원본 텍스트 파일 경로.
        output_path (str): 수정된 텍스트 파일 저장 경로.
        word_list (list): 빈 줄로 만들 단어들의 리스트.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 먼저 규칙 1~12, 14를 적용하여 1차 처리
        intermediate_lines = []
        for line in lines:
            # 1. 한 줄에 한글이 포함되어 있지 않다면
            if not re.search(r'[가-힣]', line):
                intermediate_lines.append('\n')
                continue

            # 2. 한 줄에 전화번호(숫자-숫자-숫자)가 있다면 해당 줄 삭제
            if re.search(r'\d{2,4}-\d{3,4}-\d{4}', line):
                continue  # 삭제 (append하지 않음)

            # 3. 한 줄에 이메일 주소가 있다면 해당 줄 삭제
            if re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', line):
                continue  # 삭제 (append하지 않음)

            # 4. 한 줄에 '.'이 세 번 이상 연속된다면 빈 줄로 변경
            if re.search(r'\.{3,}', line):
                intermediate_lines.append('\n')
                continue

            # 5. '그림 1.'과 같이 '그림' + 숫자 + '.' 패턴이 있다면 빈 줄로 변경
            if re.search(r'그림\s*\d+\.', line):
                intermediate_lines.append('\n')
                continue

            # 8. 한자로 되어 있는 텍스트 제거
            line = re.sub(r'[\u4e00-\u9fff]+', '', line)

            # 11. '자료:'으로 시작하는 줄은 빈 줄로 변경
            if re.match(r'^자료:', line.strip()):  
                intermediate_lines.append('\n')
                continue
        
            # 12. 리스트 안의 단어들로만 이루어진 줄은 빈 줄로 변경
            stripped_line = line.strip()  # 앞뒤 공백 제거 후 검사
            if stripped_line in word_list:  
                intermediate_lines.append('\n')
                continue

            # # 14. 'ABX-HE-AAA'로 시작하고 '년'으로 끝나는 줄은 빈 줄로 변경
            # if re.match(r'^ABX-HE-AAA.*년$', line.strip()):
            #     intermediate_lines.append('\n')
                continue

            # 위 조건에 해당하지 않으면 원래 줄 유지
            intermediate_lines.append(line)

        # ===== 개선된 규칙 13 적용: 전체 파일에 대해 두 번째 패스로 적용 =====
        # 빈 줄(또는 공백 라인)에 둘러싸인 단일 라인을 빈 줄로 변경
        processed_lines = []
        for i, line in enumerate(intermediate_lines):
            # 비어있지 않은 라인에 대해서만 확인
            if line.strip():
                # 첫 줄이거나 마지막 줄이 아니고, 전후 라인이 모두 비어있으면
                if (i > 0 and i < len(intermediate_lines) - 1 and 
                    not intermediate_lines[i-1].strip() and 
                    not intermediate_lines[i+1].strip()):
                    processed_lines.append('\n')  # 빈 줄로 변경
                else:
                    processed_lines.append(line)  # 원래 내용 유지
            else:
                processed_lines.append(line)  # 이미 빈 줄이면 유지

        # # ===== 추가 규칙 1: 마지막 5줄 제거 =====
        # if len(processed_lines) > 5:
        #     processed_lines = processed_lines[:-5]
        # else:
        #     processed_lines = []  # 파일이 5줄 이하인 경우 모든 줄 제거

        # ===== 추가 규칙 2: 모든 \n 제거 =====
        # 줄바꿈 문자(\n)를 제거하고 공백으로 대체
        # processed_text = ''.join(processed_lines)
        # processed_text = processed_text.replace('\n', ' ')
        
        # 여러 개의 공백을 하나의 공백으로 치환
        processed_text = re.sub(r'\s+', ' ', processed_text)
        
        # 결과를 새로운 파일에 저장 (단일 문자열로)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(processed_text)

        return True

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return False


def process_folder(input_folder, output_folder, word_list, file_extensions=None):
    """
    입력 폴더의 모든 텍스트 파일을 처리하여 출력 폴더에 저장합니다.
    
    Args:
        input_folder (str): 원본 텍스트 파일들이 있는 폴더 경로
        output_folder (str): 처리된 파일들을 저장할 폴더 경로
        word_list (list): 빈 줄로 만들 단어들의 리스트
        file_extensions (list, optional): 처리할 파일 확장자 목록. 기본값은 ['.txt']
    """
    if file_extensions is None:
        file_extensions = ['.txt']
    
    # 출력 폴더가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output directory: {output_folder}")
    
    # 처리된 파일 수와 실패한 파일 수를 추적
    processed_count = 0
    failed_count = 0
    
    # 입력 폴더의 모든 파일을 순회
    for ext in file_extensions:
        file_pattern = os.path.join(input_folder, f"*{ext}")
        for file_path in glob.glob(file_pattern):
            # 출력 파일 경로 생성
            file_name = os.path.basename(file_path)
            output_path = os.path.join(output_folder, file_name)
            
            print(f"Processing: {file_name}")
            
            # 파일 처리
            success = process_text_file(file_path, output_path, word_list)
            
            if success:
                processed_count += 1
            else:
                failed_count += 1
    
    # 처리 결과 요약 출력
    print(f"\nProcessing complete!")
    print(f"Files processed successfully: {processed_count}")
    print(f"Files failed: {failed_count}")


# Example Usage
input_folder = "C:/Users/hp/Desktop/채권리포트/하이투자증권/p2t_bond"  # 원본 텍스트 파일들이 있는 폴더
output_folder = "C:/Users/hp/Desktop/채권리포트/하이투자증권/새 폴더"  # 처리된 파일들을 저장할 폴더

# 리스트에 포함된 단어들 (빈줄로 만들 대상)
word_list = ['Key takeaways', 'Key Chart', '[Bond Insight]', '[Bond Strategy]', 'Check Point',
             'Fixed Income Brief',' 채권브리프', 'HI Weekly Credit', 'Credit Brief', 'Monetary Policy' ]

# 폴더 내 모든 텍스트 파일 처리
process_folder(input_folder, output_folder, word_list)