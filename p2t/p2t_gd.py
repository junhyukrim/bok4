from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials
import pdfplumber
import io
import os
import re

# 서비스 계정 키 파일 경로와 인증 범위 설정
SERVICE_ACCOUNT_FILE = './articulate-rain-435514-s3-77ad08a27bb3.json'  # 실제 JSON 키 파일 경로로 변경
SCOPES = ['https://www.googleapis.com/auth/drive']

# 서비스 계정 인증 설정
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

def list_files_in_folder(folder_id):
    """Google Drive 폴더 내 모든 PDF 파일 ID와 이름 가져오기"""
    query = f"'{folder_id}' in parents and mimeType='application/pdf'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    print("list_files_in_folder complete")
    return files

def download_pdf_as_stream(file_id):
    request = service.files().get_media(fileId=file_id)
    file_stream = io.BytesIO()
    downloader = MediaIoBaseDownload(file_stream, request)
    done = False
    while not done:
        try:
            status, done = downloader.next_chunk()
            print(f"Download progress: {int(status.progress() * 100)}%")
        except Exception as e:
            print(f"Error downloading file: {e}")
            return None
    file_stream.seek(0)
    print("Download complete")
    return file_stream

def pdf_to_text(file_stream):
    """PDF 파일을 텍스트로 변환"""
    with pdfplumber.open(file_stream) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    print("pdf__to_text")
    return text

def rename_file_on_drive(file_id, new_name):
    """Google Drive에서 파일 이름 변경"""
    file_metadata = {'name': new_name}
    updated_file = service.files().update(fileId=file_id, body=file_metadata).execute()
    print(f"파일 이름이 '{updated_file['name']}'으로 변경되었습니다.")

def extract_date_and_rename(txt_content, original_name):
    """텍스트 내용에서 날짜 추출 후 새로운 이름 생성"""
    match = re.search(r'(\d{4})년 (\d{1,2})월 (\d{1,2})일', txt_content)
    if match:
        year, month, day = match.groups()
        date_str = f"{year}{int(month):02d}{int(day):02d}"
        new_name = f"{date_str}_bok_min.txt"
        return new_name
    else:
        print(f"날짜를 찾을 수 없습니다. 원래 이름 유지: {original_name}")
        return original_name

# Google Drive 폴더 ID (폴더 공유 링크에서 확인 가능)
folder_id = '1Co0qm-hS5wDyAsc4hfOSF99xXvf4uEyy'

# 폴더 내 모든 PDF 파일 처리
files = list_files_in_folder(folder_id)
for file in files:
    print(f"Processing file: {file['name']}")

    # PDF 다운로드 및 텍스트 추출
    pdf_stream = download_pdf_as_stream(file['id'])
    text_content = pdf_to_text(pdf_stream)

    # 날짜 기반 새 이름 생성 및 Google Drive에서 이름 변경
    new_name = extract_date_and_rename(text_content, file['name'])
    rename_file_on_drive(file['id'], new_name)
