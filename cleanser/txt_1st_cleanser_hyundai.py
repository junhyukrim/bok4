import os
import re
import glob

def clean_text(content, words_to_remove, onlyword_list, startword_list):
    """
    텍스트 정리 규칙을 적용하는 함수:
    1. 한글이 포함되어 있지 않은 줄은 삭제
    2. 숫자 삭제
    3. 메일주소 형식 삭제
    4. 괄호와 괄호 안 내용 삭제
    5. 전화번호 형식 삭제
    6. 특수문자 삭제
    7. 지정된 단어 리스트에 있는 단어들 삭제
    8. 영어 제거
    9. onlyword_list에 있는 단어들로만 구성된 줄 삭제
    10. startword_list의 단어로 시작하는 줄 삭제
    """
    # 줄 단위로 처리
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # 1. 한글이 포함되어 있는지 확인
        if not re.search('[가-힣]', line):
            continue
        
        
        # 2. 메일주소 형식 삭제
        line = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '', line)
        
        # 3. 괄호와 괄호 안 내용 삭제 (중첩된 괄호 처리를 위해 여러 번 적용)
        while re.search(r'[\(\[\{].*?[\)\]\}]', line):
            line = re.sub(r'\([^()]*\)', '', line)  # 소괄호 () 제거
            line = re.sub(r'\[[^\[\]]*\]', '', line)  # 대괄호 [] 제거
            line = re.sub(r'\{[^\{\}]*\}', '', line)  # 중괄호 {} 제거
        
        # 4. 전화번호 형식 삭제 (다양한 전화번호 패턴 처리)
        line = re.sub(r'\d{2,4}[-\s]?\d{3,4}[-\s]?\d{4}', '', line)  # 일반 전화번호
        line = re.sub(r'\+\d{1,3}[-\s]?\d{2,4}[-\s]?\d{3,4}[-\s]?\d{4}', '', line)  # 국제 전화번호
        
        # 5. 숫자 삭제
        line = re.sub(r'\d+', '', line)
        
        # 6. 영어 제거 (대소문자 포함)
        line = re.sub(r'[a-zA-Z]+', '', line)
        
        # 7. 특수문자 삭제 (한글, 공백 외 모두 제거)
        line = re.sub(r'[^\w\s가-힣\.]', '', line) 
        
        # 8. 공백 정리 (연속된 공백을 하나로)
        line = re.sub(r'\s+', ' ', line).strip()
        
        # 9. 지정된 단어 리스트에 있는 단어들 삭제
        for word in words_to_remove:
            line = line.replace(word, '')
        
        # 10. onlyword_list에 있는 단어들로만 구성된 줄 삭제
        if line:
            # 줄을 단어로 분리
            words_in_line = line.split()
            
            # 모든 단어가 onlyword_list에 있는지 확인
            all_words_in_list = all(word in onlyword_list for word in words_in_line)
            
            # 모든 단어가 리스트에 있으면 건너뛰기
            if all_words_in_list:
                continue
        
        # 11. startword_list의 단어로 시작하는 줄 삭제
        if any(line.strip().startswith(word) for word in startword_list):
            continue
        
        # 내용이 있는 줄만 추가
        if line:
            cleaned_lines.append(line)
    
    # 12. '본 조사자료는'으로 시작하는 부분 이후를 모두 삭제
    final_text = '\n'.join(cleaned_lines)
    disclaimer_index = final_text.find('본 조사자료는')
    if disclaimer_index != -1:
        final_text = final_text[:disclaimer_index]
    
    return final_text

    

def process_files():
    # 제거할 단어 리스트 정의
    words_to_remove = [
        "이정준", "이정준 연구위원", "자료제공일", "년 월 일", "황원화"
    ]
    
    # onlyword_list 정의 (해당 단어들로만 구성된 줄 삭제)
    onlyword_list = [
        "국고채년", "통안년", "특수채년", "한전채년", "산금채년", "회사채년", "한국", "미국", "영국", "일본", "독일", "은행채", "회사채", "국고채", "통안", "자료", "투자증권", "스프레드", 
        "현대백화점", "주간 시장 동향 및 전망", "황원하", "전주대비", "특수채", "여전채", "국민종년", "예보년", "크레딧", "스프레드", "연평균", "신계열", "구계열","년","월","일일", "국고","국고국고",
        "국고년","국종년","특수년","한전년","산금년","회사년","전월말대비", "중국", "홍콩", "선물", "선물가격", "저평가폭"
    ]
    
    # startword_list 정의 (해당 단어로 시작하는 줄 삭제)
    startword_list = ['도표 ', '종목 ', '자료 ', '그림 ']
    
    # input_folder 내의 모든 txt 파일 찾기
    input_folder = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_txt/bond_txt/test/input"  # 원본 텍스트 파일들이 있는 폴더
    output_folder = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_txt/bond_txt/test/output"  # 처리된 파일들을 저장할 폴더
    
    # 출력 폴더가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 모든 txt 파일 처리
    for file_path in glob.glob(os.path.join(input_folder, '*.txt')):
        file_name = os.path.basename(file_path)
        
        # 파일 내용 읽기
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except UnicodeDecodeError:
            # UTF-8로 읽기 실패 시 다른 인코딩 시도
            try:
                with open(file_path, 'r', encoding='cp949') as file:
                    content = file.read()
            except:
                print(f"인코딩 오류: {file_name} - 파일을 건너뜁니다.")
                continue
        
        # 텍스트 정리 규칙 적용
        cleaned_content = clean_text(content, words_to_remove, onlyword_list, startword_list)
        
        # 처리된 내용 저장
        output_path = os.path.join(output_folder, file_name)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_content)
        
        print(f"처리 완료: {file_name}")

if __name__ == "__main__":
    process_files()
    print("모든 파일 처리가 완료되었습니다.")
