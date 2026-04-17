import os

from moviepy import AudioFileClip, ColorClip, VideoFileClip, concatenate_videoclips


ffmpeg_bin = r"C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin"
os.environ["PATH"] += os.pathsep + ffmpeg_bin
os.environ["FFMPEG_BINARY"] = os.path.join(ffmpeg_bin, "ffmpeg.exe")

OUTPUT_BASE = "media/output"
RESULT_DIR = "media/result/Codex"
OUTPUT_FILENAME = "Worship_Gathering_3min.mp4"
USED_FILES_FILENAME = "USED_FILES.md"
STORYBOARD_FILENAME = "STORYBOARD.md"
PROCESS_FILENAME = "CREATION_PROCESS.md"
FRAME_SIZE = (1280, 720)
FPS = 24

CLIPS_CONFIG = [
    {
        "section": "오프닝",
        "family": "해준해나",
        "folder": "해준해나(3)",
        "keyword": "_001_",
        "start": 0,
        "duration": 8,
        "note": "짧은 기도로 영상의 시작을 연다",
    },
    {
        "section": "찬양",
        "family": "소유사랑",
        "folder": "소유사랑(1)",
        "keyword": "_001_",
        "start": 0,
        "duration": 10,
        "note": "아이들 찬양으로 예배 분위기를 세운다",
    },
    {
        "section": "찬양",
        "family": "우진아인",
        "folder": "우진아인(1)",
        "keyword": "_012_",
        "start": 0,
        "duration": 12,
        "note": "주 예수보다 더 귀한 것은 없네",
    },
    {
        "section": "찬양",
        "family": "해준해나",
        "folder": "해준해나(2)",
        "keyword": "_001_",
        "start": 0,
        "duration": 10,
        "note": "어린 양 찬양으로 흐름을 이어간다",
    },
    {
        "section": "찬양",
        "family": "지호리호",
        "folder": "지호리호(8)",
        "keyword": "_001_",
        "start": 0,
        "duration": 10,
        "note": "회중 찬양으로 예배 현장감을 더한다",
    },
    {
        "section": "말씀",
        "family": "수혁",
        "folder": "수혁(1)",
        "keyword": "_002_",
        "start": 0,
        "duration": 10,
        "note": "청소년 말씀봉독으로 중심 문장을 세운다",
    },
    {
        "section": "말씀",
        "family": "이안이서",
        "folder": "이안이서(2)",
        "keyword": "_001_",
        "start": 0,
        "duration": 10,
        "note": "가정이 함께 읽는 마태복음 봉독",
    },
    {
        "section": "말씀",
        "family": "지호리호",
        "folder": "지호리호(5)",
        "keyword": "_008_",
        "start": 0,
        "duration": 10,
        "note": "요한복음 봉독으로 말씀 구간을 맺는다",
    },
    {
        "section": "나눔",
        "family": "이안이서",
        "folder": "이안이서(3)",
        "keyword": "_017_",
        "start": 0,
        "duration": 12,
        "note": "하나님이 늘 함께하신다는 설명",
    },
    {
        "section": "나눔",
        "family": "우진아인",
        "folder": "우진아인(1)",
        "keyword": "_030_",
        "start": 0,
        "duration": 12,
        "note": "두려울 때 기도하라는 부모의 권면",
    },
    {
        "section": "나눔",
        "family": "지호리호",
        "folder": "지호리호(7)",
        "keyword": "_008_",
        "start": 0,
        "duration": 12,
        "note": "학교 속 믿음의 경험을 나누는 고백",
    },
    {
        "section": "나눔",
        "family": "소유사랑",
        "folder": "소유사랑(2)",
        "keyword": "_029_",
        "start": 0,
        "duration": 12,
        "note": "함께 하시는 하나님을 생활 언어로 풀어낸다",
    },
    {
        "section": "기도",
        "family": "수혁",
        "folder": "수혁(2)",
        "keyword": "_001_",
        "start": 0,
        "duration": 12,
        "note": "청소년 기도로 합심 기도를 시작한다",
    },
    {
        "section": "기도",
        "family": "이안이서",
        "folder": "이안이서(3)",
        "keyword": "_028_",
        "start": 0,
        "duration": 12,
        "note": "구원자 예수님을 고백하는 기도",
    },
    {
        "section": "기도",
        "family": "우진아인",
        "folder": "우진아인(2)",
        "keyword": "_034_",
        "start": 0,
        "duration": 12,
        "note": "선한 목자 되신 주님께 드리는 기도",
    },
    {
        "section": "기도",
        "family": "소유사랑",
        "folder": "소유사랑(1)",
        "keyword": "_030_",
        "start": 0,
        "duration": 12,
        "note": "각 가정을 위한 기도로 잔잔하게 마친다",
    },
]


def find_target_file(output_base, folder, keyword):
    folder_path = os.path.join(output_base, folder)
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"폴더를 찾을 수 없습니다: {folder_path}")

    for name in sorted(os.listdir(folder_path)):
        if keyword in name and name.endswith((".mp4", ".m4a")):
            return os.path.join(folder_path, name)

    raise FileNotFoundError(f"파일을 찾을 수 없습니다: {folder} / {keyword}")


def build_video_clip(path, start, duration):
    clip = VideoFileClip(path)
    actual_duration = min(duration, clip.duration - start)
    if actual_duration <= 0:
        clip.close()
        return None

    clip = clip.subclipped(start, start + actual_duration)
    clip = clip.resized(height=FRAME_SIZE[1])
    return clip


def build_audio_clip(path, start, duration):
    audio = AudioFileClip(path)
    actual_duration = min(duration, audio.duration - start)
    if actual_duration <= 0:
        audio.close()
        return None

    audio = audio.subclipped(start, start + actual_duration)
    return ColorClip(size=FRAME_SIZE, color=(8, 8, 8), duration=actual_duration).with_audio(audio)


def build_clip(path, start, duration):
    if path.endswith(".mp4"):
        return build_video_clip(path, start, duration)
    return build_audio_clip(path, start, duration)


def build_storyboard_markdown(total_duration):
    lines = [
        "# Codex 스토리보드",
        "",
        "## 목표",
        "교회 대예배에서 상영할 약 3분 분량의 가정예배 모음 영상을 구성한다.",
        "모든 가정과 청소년 음성을 포함하고, 기도에서 시작해 찬양-말씀-고백-합심기도로 감정선을 만든다.",
        "",
        "## 편집 의도",
        "요약 파일을 다시 읽어보면 각 가정이 반복해서 말하는 핵심이 세 가지였다.",
        "예수님을 찬양하는 기쁨, 하나님이 함께하신다는 확신, 그리고 가정을 위한 기도다.",
        "이번 편집은 이 세 문장을 3분 안에 자연스럽게 이어 붙이는 방식으로 설계했다.",
        "",
        "## 타임라인",
    ]

    elapsed = 0
    for index, item in enumerate(CLIPS_CONFIG, start=1):
        start_time = seconds_to_mmss(elapsed)
        elapsed += item["duration"]
        end_time = seconds_to_mmss(elapsed)
        lines.append(
            f"{index}. {start_time} - {end_time} | {item['section']} | "
            f"{item['family']} | {item['note']}"
        )

    lines.extend(
        [
            "",
            "## 편집 원칙",
            "- 모든 가정이 최소 1회 이상 등장한다.",
            "- 수혁 파트는 음성 파일이라 검은 배경 위 원본 음성으로 처리한다.",
            "- 별도 배경음악 없이 원본 예배 음성 흐름을 살린다.",
            f"- 예상 총 길이: 약 {total_duration:.0f}초",
        ]
    )
    return "\n".join(lines) + "\n"


def build_process_markdown(used_rows, total_duration):
    family_order = []
    seen = set()
    for row in used_rows:
        if row["family"] not in seen:
            family_order.append(row["family"])
            seen.add(row["family"])

    lines = [
        "# Codex 제작 과정",
        "",
        "## 작업 기준",
        "- `요구사항.md`만 기준으로 다시 읽고, 기존 Gemini 문서는 편집 근거에서 제외했다.",
        "- `media/output`의 분절 결과와 요약 텍스트를 다시 검토해 클립을 직접 선별했다.",
        "- 결과물과 문서는 모두 `media/result/Codex`에 저장한다.",
        "",
        "## 편집 흐름",
        "1. 짧은 기도로 시작해 대예배 상영용 집중도를 바로 만든다.",
        "2. 각 가정의 찬양을 연달아 배치해 공동체성을 먼저 보여준다.",
        "3. 말씀봉독과 생활 고백으로 메시지를 분명하게 세운다.",
        "4. 청소년과 각 가정의 기도로 차분하게 마무리한다.",
        "",
        "## 포함된 가정",
        f"- {', '.join(family_order)}",
        "",
        "## 사용 기준",
        "- 모든 가정이 최소 1회 이상 들어가도록 구성했다.",
        "- 음성 품질보다 메시지 전달력과 장면 흐름이 좋은 구간을 우선 선택했다.",
        "- 청소년 음성은 영상 소스가 없어서 검은 배경으로 처리했다.",
        "",
        "## 결과 요약",
        f"- 총 클립 수: {len(used_rows)}개",
        f"- 예상 총 길이: 약 {total_duration:.0f}초",
        f"- 결과 파일: `{os.path.join(RESULT_DIR, OUTPUT_FILENAME)}`",
        "",
        "## 추가 작업 제안",
        "- 자막을 직접 넣으면 대예배 현장에서 전달력이 더 좋아진다.",
        "- 음량 정규화와 장면 전환 효과를 더하면 완성도가 높아진다.",
        "- 수혁 오디오 구간에는 추후 정적 이미지나 성구 자막을 넣어도 좋다.",
    ]
    return "\n".join(lines) + "\n"


def write_used_files(result_dir, used_rows):
    manifest_path = os.path.join(result_dir, USED_FILES_FILENAME)
    with open(manifest_path, "w", encoding="utf-8") as handle:
        handle.write("# Codex 사용 파일 목록\n\n")
        handle.write("| 순서 | 구간 | 가정 | 폴더 | 파일 | 비고 |\n")
        handle.write("| --- | --- | --- | --- | --- | --- |\n")
        for index, row in enumerate(used_rows, start=1):
            handle.write(
                f"| {index} | {row['section']} | {row['family']} | {row['folder']} | "
                f"`{row['path']}` | {row['note']} |\n"
            )


def write_documents(result_dir, used_rows, total_duration):
    storyboard_path = os.path.join(result_dir, STORYBOARD_FILENAME)
    with open(storyboard_path, "w", encoding="utf-8") as handle:
        handle.write(build_storyboard_markdown(total_duration))

    process_path = os.path.join(result_dir, PROCESS_FILENAME)
    with open(process_path, "w", encoding="utf-8") as handle:
        handle.write(build_process_markdown(used_rows, total_duration))


def seconds_to_mmss(value):
    total_seconds = int(round(value))
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


def create_final_video():
    os.makedirs(RESULT_DIR, exist_ok=True)

    final_clips = []
    used_rows = []

    for item in CLIPS_CONFIG:
        target_file = find_target_file(OUTPUT_BASE, item["folder"], item["keyword"])
        print(f"처리 중: {target_file}")

        clip = build_clip(target_file, item["start"], item["duration"])
        if clip is None:
            continue

        final_clips.append(clip)
        used_rows.append(
            {
                "section": item["section"],
                "family": item["family"],
                "folder": item["folder"],
                "path": target_file,
                "note": item["note"],
            }
        )

    if not final_clips:
        raise RuntimeError("생성할 클립이 없습니다.")

    total_duration = sum(clip.duration for clip in final_clips)
    final_video = concatenate_videoclips(final_clips, method="compose")
    output_path = os.path.join(RESULT_DIR, OUTPUT_FILENAME)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=FPS)

    write_used_files(RESULT_DIR, used_rows)
    write_documents(RESULT_DIR, used_rows, total_duration)

    final_video.close()
    for clip in final_clips:
        clip.close()

    print(f"최종 영상 생성 완료: {output_path}")


if __name__ == "__main__":
    create_final_video()
