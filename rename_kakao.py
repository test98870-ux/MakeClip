
import os
import shutil

# Kakao 파일 매핑 정보
mapping = {
    "kakaotalk_1774763661015": "수혁(1)",
    "kakaotalk_1774763666978": "수혁(2)"
}

output_dir = r"media/output"

if not os.path.exists(output_dir):
    print("Output 폴더를 찾을 수 없습니다.")
else:
    for old_base, new_prefix in mapping.items():
        old_folder_path = os.path.join(output_dir, old_base)
        
        if os.path.exists(old_folder_path) and os.path.isdir(old_folder_path):
            print(f"변경 중: {old_base} -> {new_prefix}")
            
            # 1. 폴더 내 파일들의 이름 변경
            for filename in os.listdir(old_folder_path):
                if old_base in filename:
                    new_filename = filename.replace(old_base, new_prefix)
                    os.rename(
                        os.path.join(old_folder_path, filename),
                        os.path.join(old_folder_path, new_filename)
                    )
            
            # 2. 폴더명 변경
            new_folder_path = os.path.join(output_dir, new_prefix)
            if os.path.exists(new_folder_path):
                # 이미 존재할 경우 내용물 이동 후 삭제
                for f in os.listdir(old_folder_path):
                    shutil.move(os.path.join(old_folder_path, f), os.path.join(new_folder_path, f))
                os.rmdir(old_folder_path)
            else:
                os.rename(old_folder_path, new_folder_path)

print("\n[완료] Kakao 파일들의 이름이 '수혁' 프리픽스로 변경되었습니다.")
