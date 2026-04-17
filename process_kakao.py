import os
import sys
import whisper
from moviepy import VideoFileClip, AudioFileClip
import torch
import re
import librosa
import numpy as np

# FFmpeg 경로 강제 설정
ffmpeg_bin = r"C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin"
ffmpeg_exe = os.path.join(ffmpeg_bin, "ffmpeg.exe")
os.environ["PATH"] += os.pathsep + ffmpeg_bin
os.environ["FFMPEG_BINARY"] = ffmpeg_exe

def analyze_audio_raw(clip, start, end, is_video=True):
    try:
        # 비디오 클립이든 오디오 클립이든 오디오 데이터를 가져옴
        target_clip = clip.audio if is_video else clip
        sub_audio = target_clip.subclipped(start, end)
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
    last_label = "설교"
    for c in chunks:
        ratio = c['ratio']
        if ratio >= 3.0: c['final_label'] = "찬양"
        elif ratio >= 2.0 and last_label == "찬양": c['final_label'] = "찬양"
        else: c['final_label'] = "설교"
        last_label = c['final_label']

    prayer_start_pattern = r"(기도하시겠|기도합시다|기도하겠|하나님아버지|주님앞에|사랑의주님)"
    prayer_end_pattern = r"(예수|주님).*(이름으로).*(기도).*(합니다|나이다|습니다|아멘)"
    
    in_prayer_stream = False
    for i in range(len(chunks)):
        text = chunks[i]['text'].replace(" ", "").lower()
        if chunks[i]['final_label'] != "찬양":
            if re.search(prayer_start_pattern, text): in_prayer_stream = True
            if in_prayer_stream: chunks[i]['final_label'] = "기도"
            if re.search(prayer_end_pattern, text) or "아멘" in text:
                chunks[i]['final_label'] = "기도"
                if not in_prayer_stream:
                    for j in range(max(0, i-2), i):
                        if chunks[j]['final_label'] == "설교": chunks[j]['final_label'] = "기도"
                in_prayer_stream = False

    for c in chunks:
        if c['final_label'] == "설교":
            text = c['text'].replace(" ", "").lower()
            if any(k in text for k in ["성경", "봉독", "말씀은", "오늘의말씀"]) and re.search(r'\d', text):
                c['final_label'] = "말씀봉독"
    return chunks

def format_time(seconds):
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}m{s:02d}s"

def process_media_ultimate(file_path, output_root):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    file_output_dir = os.path.join(output_root, base_name)
    summary_path = os.path.join(file_output_dir, f"{base_name}_summary.txt")
    
    if not os.path.exists(file_output_dir): os.makedirs(file_output_dir)
    
    ext = os.path.splitext(file_path)[1].lower()
    is_video = ext in ['.mp4', '.mkv', '.mov', '.avi']
    
    print(f"\n[분석 시작] {file_path}")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("medium", device=device)
    
    result = model.transcribe(file_path, language="ko", verbose=False)
    segments = result['segments']
    
    # 영상/오디오 클립 로드
    clip = VideoFileClip(file_path) if is_video else AudioFileClip(file_path)
    duration_total = clip.duration
    
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
            ratio, _ = analyze_audio_raw(clip, last_split, end, is_video=is_video)
            raw_chunks.append({'start': last_split, 'end': end, 'text': accumulated_text.strip(), 'ratio': ratio})
            last_split = end
            accumulated_text = ""

    if last_split < duration_total - 1:
        raw_chunks.append({'start': last_split, 'end': duration_total, 'text': accumulated_text.strip(), 'ratio': 0.0})

    refined_chunks = process_labels_prioritized_v4(raw_chunks)

    with open(summary_path, "w", encoding="utf-8-sig") as f:
        f.write(f"=== Analysis Summary: {base_name} ===\n")
        for i, c in enumerate(refined_chunks):
            f.write(f"[{i+1:03d}] {format_time(c['start'])} | {c['final_label']} | Ratio:{c['ratio']:.2f} | {c['text'][:80]}\n")
            
    for i, c in enumerate(refined_chunks):
        if (c['end'] - c['start']) < 1.0: continue
        time_tag = format_time(c['start'])
        output_ext = ".mp4" if is_video else ".m4a"
        output_filename = os.path.join(file_output_dir, f"{base_name}_{i+1:03d}_{time_tag}_{c['final_label']}{output_ext}")
        
        if not os.path.exists(output_filename):
            print(f"  > [{i+1}/{len(refined_chunks)}] 저장: {c['final_label']} ({time_tag})")
            # 마지막 조각의 시간이 전체 길이를 넘지 않도록 보호
            safe_end = min(c['end'], duration_total)
            sub = clip.subclipped(c['start'], safe_end)
            if is_video:
                sub.write_videofile(output_filename, codec="libx264", audio_codec="aac", logger=None)
            else:
                # 오디오 파일 저장 시 코덱 명시 (aac 또는 libmp3lame)
                sub.write_audiofile(output_filename, codec="aac", logger=None)
            
    clip.close()

if __name__ == "__main__":
    media_dir = "media"
    output_dir = os.path.join(media_dir, "output")
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    
    # kakao 파일들만 타겟팅하여 처리
    kakao_files = [f for f in os.listdir(media_dir) if f.startswith("kakao") and f.lower().endswith(('.m4a', '.mp3'))]
    
    if not kakao_files:
        print("kakao로 시작하는 오디오 파일을 찾을 수 없습니다.")
    else:
        print(f"총 {len(kakao_files)}개의 kakao 오디오 파일을 발견했습니다. 분석을 시작합니다.")
        for file in kakao_files:
            process_media_ultimate(os.path.join(media_dir, file), output_dir)
