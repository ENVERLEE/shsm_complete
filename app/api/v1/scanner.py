import os
from datetime import datetime
import chardet

def detect_encoding(file_path):
    """파일의 인코딩을 감지합니다."""
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def format_size(size):
    """파일 크기를 읽기 쉬운 형식으로 변환합니다."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

def scan_directory(start_path, output_file, exclude_dirs=None, exclude_files=None):
    """
    지정된 경로의 모든 폴더와 파일을 깊이 우선 탐색으로 스캔하여 구조를 텍스트 파일로 저장합니다.
    
    Args:
        start_path (str): 스캔을 시작할 루트 디렉토리 경로
        output_file (str): 결과를 저장할 텍스트 파일 경로
        exclude_dirs (list): 제외할 디렉토리 목록 (예: ['.git', 'node_modules'])
        exclude_files (list): 제외할 파일 패턴 목록 (예: ['.pyc', '.pyo'])
    """
    if exclude_dirs is None:
        exclude_dirs = ['.git', 'node_modules', '__pycache__', 'venv', '.idea']
    if exclude_files is None:
        exclude_files = ['.pyc', '.pyo', '.pyd', '.so', '.dll']
    
    start_time = datetime.now()
    total_files = 0
    total_dirs = 0
    total_size = 0
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # 헤더 정보 작성
        f.write(f"프로젝트 폴더 구조 상세 스캔 결과\n")
        f.write(f"스캔 시작 시간: {start_time}\n")
        f.write(f"루트 경로: {os.path.abspath(start_path)}\n")
        f.write("="*80 + "\n\n")
        
        for root, dirs, files in os.walk(start_path):
            # 제외할 디렉토리 필터링
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            # 현재 디렉토리 레벨 계산
            level = root.replace(start_path, '').count(os.sep)
            indent = '  ' * level
            
            # 현재 디렉토리 정보 작성
            folder = os.path.basename(root)
            dir_size = sum(os.path.getsize(os.path.join(root, name)) for name in files)
            total_size += dir_size
            total_dirs += 1
            
            f.write(f"\n{indent}📁 {folder}/ ({format_size(dir_size)})\n")
            f.write(f"{indent}   경로: {os.path.abspath(root)}\n")
            
            # 하위 파일 정보 작성
            sub_indent = '  ' * (level + 1)
            files.sort()  # 파일 이름 알파벳순 정렬
            
            for file in files:
                if any(file.endswith(ext) for ext in exclude_files):
                    continue
                    
                file_path = os.path.join(root, file)
                try:
                    # 파일 기본 정보 수집
                    size = os.path.getsize(file_path)
                    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    create_time = datetime.fromtimestamp(os.path.getctime(file_path))
                    total_files += 1
                    
                    # 파일 확장자 확인
                    _, ext = os.path.splitext(file)
                    
                    # 파일 정보 작성
                    f.write(f"\n{sub_indent}📄 {file}\n")
                    f.write(f"{sub_indent}   크기: {format_size(size)}\n")
                    f.write(f"{sub_indent}   생성: {create_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"{sub_indent}   수정: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    
                    # 텍스트 파일 내용 읽기
                    text_extensions = [
                        '.txt', '.py', '.js', '.html', '.css', '.md', '.json', 
                        '.xml', '.yaml', '.yml', '.ini', '.conf', '.cfg', 
                        '.properties', '.env', '.sql', '.sh', '.bat', '.ps1',
                        '.java', '.cpp', '.hpp', '.h', '.c', '.cs', '.php',
                        '.rb', '.pl', '.swift', '.kt', '.ts', '.jsx', '.tsx'
                    ]
                    
                    if ext.lower() in text_extensions and size < 1024 * 1024:  # 1MB 미만 파일만
                        try:
                            # 파일 인코딩 감지
                            encoding = detect_encoding(file_path)
                            if not encoding:
                                encoding = 'utf-8'
                            
                            with open(file_path, 'r', encoding=encoding) as content_file:
                                content = content_file.read()
                                f.write(f"{sub_indent}   내용:\n")
                                f.write(f"{sub_indent}   {'='*40}\n")
                                for line_num, line in enumerate(content.splitlines(), 1):
                                    f.write(f"{sub_indent}   {line_num:4d} | {line}\n")
                                f.write(f"{sub_indent}   {'='*40}\n")
                        except Exception as e:
                            f.write(f"{sub_indent}   파일 읽기 실패: {str(e)}\n")
                
                except Exception as e:
                    f.write(f"{sub_indent}❌ {file} (접근 오류: {str(e)})\n")
            
            f.write("\n")
        
        # 스캔 완료 정보 및 통계 작성
        end_time = datetime.now()
        duration = end_time - start_time
        f.write("\n" + "="*80 + "\n")
        f.write("스캔 완료 통계:\n")
        f.write(f"총 디렉토리 수: {total_dirs:,}개\n")
        f.write(f"총 파일 수: {total_files:,}개\n")
        f.write(f"총 크기: {format_size(total_size)}\n")
        f.write(f"스캔 완료 시간: {end_time}\n")
        f.write(f"소요 시간: {duration}\n")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='디렉토리 구조를 상세하게 스캔하여 텍스트 파일로 저장합니다.')
    parser.add_argument('--path', default=".", help='스캔할 디렉토리 경로 (기본값: 현재 디렉토리)')
    parser.add_argument('--output', default="folder_structure_detailed.txt", help='결과를 저장할 파일 경로')
    parser.add_argument('--exclude-dirs', nargs='*', help='제외할 디렉토리 목록')
    parser.add_argument('--exclude-files', nargs='*', help='제외할 파일 확장자 목록')
    
    args = parser.parse_args()
    
    # chardet 라이브러리 설치 확인
    try:
        import chardet
    except ImportError:
        print("chardet 라이브러리가 필요합니다. 다음 명령어로 설치하세요:")
        print("pip install chardet")
        exit(1)
    
    scan_directory(
        args.path, 
        args.output,
        exclude_dirs=args.exclude_dirs,
        exclude_files=args.exclude_files
    )
    print(f"폴더 구조가 {args.output}에 저장되었습니다.")