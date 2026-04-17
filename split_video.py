import os
import sys
import whisper
from moviepy import VideoFileClip
import torch
import re
import librosa
import numpy as np

# FFmpeg 경로 강제 설정
ffmpeg_bin = r"C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin"
ffmpeg_exe = os.path.join(ffmpeg_bin, "ffmpeg.exe")
os.environ["PATH"] += os.pathsep + ffmpeg_bin
os.environ["FFMPEG_BINARY"] = ffmpeg_exe

def analyze_audio_raw(video_clip, start, end):
    try:
        sub_audio = video_clip.audio.subclipped(start, end)
        sr = 22050
        y = sub_audio.to_soundarray(fps=sr)
        if len(y.shape) > 1: y = np.mean(y, axis=1)
        if len(y) < sr * 0.5: return 0.5, 0.0
        harmonic, percussive = librosa.effects.hpss(y)
        h_energy = np.mean(librosa.feature.rms(y=harmonic))
        p_energy = np.mean(librosa.feature.rms(y=percussive))
        centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        ratio = h_energy / (p_energy + 1e-6)
        return ratio, centroid
    except:
        return 0.5, 0.0

def process_labels_prioritized_v4(chunks):
    """
    1. 찬양 Ratio 2.0 미만 시 즉시 중단 (6초 이상 지속 조건 반영)
    2. 기도 맥락 20초 제한 및 정밀화
    """
    last_label = "설교"
    
    # 1차 패스: 찬양 판정 (Ratio 중심)
    for c in chunks:
        ratio = c['ratio']
        
        # 찬양 시작 조건 (3.0 이상)
        if ratio >= 3.0:
            c['final_label'] = "찬양"
        # 찬양 유지 조건 (2.0 이상이면서 이전이 찬양)
        elif ratio >= 2.0 and last_label == "찬양":
            c['final_label'] = "찬양"
        # 찬양 중단 조건 (2.0 미만이면 즉시 중단 - 한 조각이 8초 이상이므로 6초 기준 충족)
        else:
            c['final_label'] = "설교"
            
        last_label = c['final_label']

    # 2차 패스: 기도 맥락 (찬양이 아닌 구간 중)
    prayer_start_pattern = r"(기도하시겠|기도합시다|기도하겠|하나님아버지|주님앞에|사랑의주님)"
    prayer_end_pattern = r"(예수|주님).*(이름으로).*(기도).*(합니다|나이다|습니다|아멘)"
    
    in_prayer_stream = False
    for i in range(len(chunks)):
        text = chunks[i]['text'].replace(" ", "").lower()
        
        if chunks[i]['final_label'] != "찬양":
            # 기도 시작
            if re.search(prayer_start_pattern, text):
                in_prayer_stream = True
            
            if in_prayer_stream:
                chunks[i]['final_label'] = "기도"
            
            # 기도 종료 감지
            if re.search(prayer_end_pattern, text) or "아멘" in text:
                chunks[i]['final_label'] = "기도"
                # 소급 적용 (최대 2개 조각으로 제한 - 약 20초 내외)
                if not in_prayer_stream:
                    for j in range(max(0, i-2), i):
                        if chunks[j]['final_label'] == "설교":
                            chunks[j]['final_label'] = "기도"
                in_prayer_stream = False

    # 3차 패스: 말씀봉독 (나머지 설교 중)
    for c in chunks:
        if c['final_label'] == "설교":
            text = c['text'].replace(" ", "").lower()
            if any(k in text for k in ["성경", "봉독", "말씀은", "오늘의말씀"]) and re.search(r'\d', text):
                c['final_label'] = "말씀봉독"

    return chunks

def format_time(seconds):
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}m{s:02d}s"

def process_video_ultimate_v4(video_path, output_root):
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    file_output_dir = os.path.join(output_root, base_name)
    summary_path = os.path.join(file_output_dir, f"{base_name}_summary.txt")
    
    if os.path.exists(summary_path):
        print(f"\n[건너뜀] {base_name}")
        return

    if not os.path.exists(file_output_dir): os.makedirs(file_output_dir)
    
    print(f"\n[V4 정밀 분석 시작] {video_path}")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("medium", device=device)
    
    result = model.transcribe(video_path, language="ko", verbose=False)
    segments = result['segments']
    
    video = VideoFileClip(video_path)
    raw_chunks = []
    last_split = 0.0
    accumulated_text = ""
    
    for seg in segments:
        end = seg['end']
        text = seg['text'].strip()
        accumulated_text += " " + text
        duration = end - last_split
        
        is_sentence_end = any(text.endswith(p) for p in ['.', '?', '!', '요', '다', '죠', '오', '아', '아멘'])
        
        if (8 <= duration <= 15 and is_sentence_end) or duration > 15:
            ratio, _ = analyze_audio_raw(video, last_split, end)
            raw_chunks.append({'start': last_split, 'end': end, 'text': accumulated_text.strip(), 'ratio': ratio})
            last_split = end
            accumulated_text = ""

    if last_split < video.duration - 1:
        raw_chunks.append({'start': last_split, 'end': video.duration, 'text': accumulated_text.strip(), 'ratio': 0.0})

    refined_chunks = process_labels_prioritized_v4(raw_chunks)

    # 요약 저장
    with open(summary_path, "w", encoding="utf-8-sig") as f:
        f.write(f"=== V4 Context-Aware Summary: {base_name} ===\n")
        f.write("(Constraint: Praise Ratio < 2.0 Stops Recognition, Prayer <= 20s Context)\n\n")
        for i, c in enumerate(refined_chunks):
            f.write(f"[{i+1:03d}] {format_time(c['start'])} | {c['final_label']} | Ratio:{c['ratio']:.2f} | {c['text'][:80]}\n")
            
    # 영상 저장
    total = len(refined_chunks)
    for i, c in enumerate(refined_chunks):
        if (c['end'] - c['start']) < 1.5: continue
        time_tag = format_time(c['start'])
        output_filename = os.path.join(file_output_dir, f"{base_name}_{i+1:03d}_{time_tag}_{c['final_label']}.mp4")
        if not os.path.exists(output_filename):
            print(f"  > [{i+1}/{total}] 저장: {c['final_label']} ({time_tag}, Ratio:{c['ratio']:.2f})")
            sub = video.subclipped(c['start'], c['end'])
            sub.write_videofile(output_filename, codec="libx264", audio_codec="aac", logger=None)
            
    video.close()

if __name__ == "__main__":
    media_dir = "media"
    output_dir = os.path.join(media_dir, "output")
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    
    # 작업 전 폴더 초기화
    if os.path.exists(output_dir):
        import shutil
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    files = [f for f in os.listdir(media_dir) if f.lower().endswith(('.mp4', '.mkv', '.mov', '.avi'))]
    for file in files:
        process_video_ultimate_v4(os.path.join(media_dir, file), output_dir)
