
import os
import shutil

mapping = {
    "2026_03_29 14_46": "소유사랑(1)",
    "2026_03_29 14_48": "소유사랑(2)",
    "2026_03_29 14_48 (1)": "이안이서(1)",
    "2026_03_29 14_48 (10)": "지호리호(1)",
    "2026_03_29 14_48 (11)": "지호리호(2)",
    "2026_03_29 14_48 (2)": "이안이서(2)",
    "2026_03_29 14_48 (3)": "이안이서(3)",
    "2026_03_29 14_48 (4)": "지호리호(3)",
    "2026_03_29 14_48 (5)": "지호리호(4)",
    "2026_03_29 14_48 (6)": "지호리호(5)",
    "2026_03_29 14_48 (7)": "지호리호(6)",
    "2026_03_29 14_48 (8)": "지호리호(7)",
    "2026_03_29 14_48 (9)": "지호리호(8)",
    "2026_03_29 14_49": "지호리호(9)",
    "2026_03_29 14_49 (2)": "해준해나(1)",
    "2026_03_29 14_49 (3)": "해준해나(2)",
    "2026_03_29 14_49 (4)": "해준해나(3)",
    "20260316_185455-001": "우진아인(1)",
    "20260321_104357": "우진아인(2)"
}

output_dir = r"media/output"

if not os.path.exists(output_dir):
    print("Output 폴더를 찾을 수 없습니다.")
else:
    # 1. 파일명부터 변경 (폴더를 먼저 바꾸면 내부 파일 경로가 깨짐)
    for old_base, new_prefix in mapping.items():
        old_folder_path = os.path.join(output_dir, old_base)
        
        if os.path.exists(old_folder_path) and os.path.isdir(old_folder_path):
            print(f"변경 중: {old_base} -> {new_prefix}")
            
            # 폴더 내 파일들 변경
            for filename in os.listdir(old_folder_path):
                if old_base in filename:
                    new_filename = filename.replace(old_base, new_prefix)
                    os.rename(
                        os.path.join(old_folder_path, filename),
                        os.path.join(old_folder_path, new_filename)
                    )
            
            # 2. 마지막으로 폴더명 변경
            new_folder_path = os.path.join(output_dir, new_prefix)
            if os.path.exists(new_folder_path):
                # 이미 존재할 경우 내용물 이동
                for f in os.listdir(old_folder_path):
                    shutil.move(os.path.join(old_folder_path, f), os.path.join(new_folder_path, f))
                os.rmdir(old_folder_path)
            else:
                os.rename(old_folder_path, new_folder_path)

print("\n[완료] 모든 폴더와 파일의 이름이 프리픽스 문구로 변경되었습니다.")
