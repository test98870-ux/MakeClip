import os
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, vfx, ColorClip
import numpy as np

# FFmpeg 경로 설정 (OS에 따라 분기 처리)
import platform
if platform.system() == "Windows":
    ffmpeg_bin = r"C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin"
    os.environ["PATH"] += os.pathsep + ffmpeg_bin
    os.environ["FFMPEG_BINARY"] = os.path.join(ffmpeg_bin, "ffmpeg.exe")
else:
    # Linux/Mac의 경우 시스템 경로의 ffmpeg 사용
    import shutil
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        os.environ["FFMPEG_BINARY"] = ffmpeg_path

def create_final_video():
    output_base = "media/output"
    result_dir = "media/result/GeminiCLI"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    # 선택 클립 리스트 (스토리보드 기반)
    # 형식: (폴더명, 파일명 키워드, 시작 오프셋, 길이)
    clips_config = [
        # 1. 오프닝
        ("소유사랑(1)", "_001_", 0, 10),
        
        # 2. 찬양의 고백
        ("우진아인(1)", "_005_", 0, 15),
        ("해준해나(2)", "_001_", 0, 15),
        ("이안이서(1)", "_001_", 0, 10),
        ("지호리호(8)", "_001_", 0, 10),
        
        # 3. 말씀의 깊이 (수혁은 오디오 파일이므로 검은 배경 처리)
        ("수혁(1)", "_001_", 0, 15),
        ("이안이서(2)", "_001_", 0, 15),
        ("지호리호(5)", "_007_", 0, 10),
        
        # 4. 나눔과 은혜
        ("이안이서(3)", "_011_", 0, 15),
        ("우진아인(1)", "_028_", 0, 15),
        ("소유사랑(1)", "_038_", 0, 15),
        ("지호리호(9)", "_002_", 0, 5),
        
        # 5. 합심 기도와 아멘
        ("해준해나(2)", "_007_", 0, 10),
        ("소유사랑(1)", "_029_", 0, 10),
        ("우진아인(1)", "_053_", 0, 5), # 아멘
        ("이안이서(3)", "_030_", 0, 5), # 아멘
        
        # 6. 클로징
        ("해준해나(2)", "_008_", 0, 5)
    ]

    final_clips = []
    
    for folder, keyword, offset, duration in clips_config:
        folder_path = os.path.join(output_base, folder)
        if not os.path.exists(folder_path):
            print(f"폴더 없음: {folder_path}")
            continue
            
        # 키워드에 맞는 파일 찾기
        target_file = None
        for f in os.listdir(folder_path):
            if keyword in f and f.endswith(('.mp4', '.m4a')):
                target_file = os.path.join(folder_path, f)
                break
        
        if not target_file:
            print(f"파일 없음: {folder} / {keyword}")
            continue

        print(f"처리 중: {target_file}")
        
        if target_file.endswith('.mp4'):
            clip = VideoFileClip(target_file)
            actual_duration = min(duration, clip.duration - offset)
            if actual_duration <= 0: continue
            print(f"  > 길이: {clip.duration:.2f}s (사용: {actual_duration:.2f}s)")
            clip = clip.subclipped(offset, offset + actual_duration)
            # 화면 크기 통일 (1280x720)
            clip = clip.resized(height=720)
            final_clips.append(clip)
        else:
            # 오디오 파일인 경우
            audio = AudioFileClip(target_file)
            actual_duration = min(duration, audio.duration - offset)
            if actual_duration <= 0: continue
            print(f"  > 길이: {audio.duration:.2f}s (사용: {actual_duration:.2f}s)")
            audio = audio.subclipped(offset, offset + actual_duration)
            black_clip = ColorClip(size=(1280, 720), color=(255, 255, 255), duration=actual_duration)
            black_clip = black_clip.with_audio(audio)
            final_clips.append(black_clip)

    if not final_clips:
        print("생성할 클립이 없습니다.")
        return

    # 클립 연결 (부드러운 전환을 위해 crossfade 적용 가능하나 여기서는 단순 연결)
    print("영상 병합 중...")
    final_video = concatenate_videoclips(final_clips, method="compose")
    
    # 결과 저장
    output_path = os.path.join(result_dir, "Worship_Gathering_3min_v2.mp4")
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24)
    
    print(f"최종 영상 생성 완료: {output_path}")

if __name__ == "__main__":
    create_final_video()
