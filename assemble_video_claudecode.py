import os

from moviepy import AudioFileClip, ColorClip, VideoFileClip, concatenate_videoclips


ffmpeg_bin = r"C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin"
os.environ["PATH"] += os.pathsep + ffmpeg_bin
os.environ["FFMPEG_BINARY"] = os.path.join(ffmpeg_bin, "ffmpeg.exe")

OUTPUT_BASE = "media/output"
RESULT_DIR = "media/result/ClaudeCode"
OUTPUT_FILENAME = "Worship_Gathering_3min.mp4"
USED_FILES_FILENAME = "USED_FILES.md"
STORYBOARD_FILENAME = "STORYBOARD.md"
PROCESS_FILENAME = "CREATION_PROCESS.md"
FRAME_SIZE = (1280, 720)
FPS = 24

# 스토리보드 구성:
# 1. 찬양으로 시작 - 각 가정의 찬양으로 예배 분위기를 연다
# 2. 말씀봉독 - 청소년 + 가정의 성경 봉독으로 말씀을 세운다
# 3. 나눔/설교 - 각 가정의 말씀 나눔과 은혜로운 고백
# 4. 기도 - 가정별 기도로 합심하며 마무리
CLIPS_CONFIG = [
    # === 1. 찬양 (Praise) - 약 50초 ===
    {
        "section": "찬양",
        "family": "소유사랑",
        "folder": "소유사랑(1)",
        "keyword": "_001_",
        "start": 0,
        "duration": 10,
        "note": "아이들의 찬양으로 예배 영상의 문을 연다",
    },
    {
        "section": "찬양",
        "family": "해준해나",
        "folder": "해준해나(2)",
        "keyword": "_001_",
        "start": 0,
        "duration": 10,
        "note": "어린이 찬양으로 밝은 분위기를 이어간다",
    },
    {
        "section": "찬양",
        "family": "우진아인",
        "folder": "우진아인(2)",
        "keyword": "_001_",
        "start": 0,
        "duration": 12,
        "note": "주 예수보다 더 귀한 것은 없네 - 가정 찬양",
    },
    {
        "section": "찬양",
        "family": "이안이서",
        "folder": "이안이서(1)",
        "keyword": "_001_",
        "start": 0,
        "duration": 10,
        "note": "온 가족이 함께 부르는 찬양",
    },
    {
        "section": "찬양",
        "family": "지호리호",
        "folder": "지호리호(8)",
        "keyword": "_001_",
        "start": 0,
        "duration": 10,
        "note": "회중 찬양으로 찬양 구간을 마무리한다",
    },

    # === 2. 말씀봉독 (Scripture) - 약 30초 ===
    {
        "section": "말씀봉독",
        "family": "수혁",
        "folder": "수혁(1)",
        "keyword": "_002_",
        "start": 0,
        "duration": 10,
        "note": "청소년 말씀봉독 - 요한복음 10장 선한 목자",
    },
    {
        "section": "말씀봉독",
        "family": "이안이서",
        "folder": "이안이서(2)",
        "keyword": "_001_",
        "start": 0,
        "duration": 10,
        "note": "가정이 함께 읽는 마태복음 임마누엘 말씀",
    },
    {
        "section": "말씀봉독",
        "family": "지호리호",
        "folder": "지호리호(5)",
        "keyword": "_007_",
        "start": 0,
        "duration": 10,
        "note": "말씀봉독으로 성경 구간을 닫는다",
    },

    # === 3. 나눔/설교 (Sharing) - 약 48초 ===
    {
        "section": "나눔",
        "family": "소유사랑",
        "folder": "소유사랑(1)",
        "keyword": "_010_",
        "start": 0,
        "duration": 12,
        "note": "선한 목자이신 예수님에 대한 아버지의 설명",
    },
    {
        "section": "나눔",
        "family": "이안이서",
        "folder": "이안이서(3)",
        "keyword": "_005_",
        "start": 0,
        "duration": 12,
        "note": "예수님의 이름 — 구원자, 임마누엘 가르침",
    },
    {
        "section": "나눔",
        "family": "우진아인",
        "folder": "우진아인(1)",
        "keyword": "_023_",
        "start": 0,
        "duration": 12,
        "note": "두려울 때 기도하라는 부모의 따뜻한 권면",
    },
    {
        "section": "나눔",
        "family": "지호리호",
        "folder": "지호리호(4)",
        "keyword": "_003_",
        "start": 0,
        "duration": 12,
        "note": "가정에서 함께 나누는 예수님의 사랑 이야기",
    },

    # === 4. 기도 (Prayer) - 약 42초 ===
    {
        "section": "기도",
        "family": "해준해나",
        "folder": "해준해나(3)",
        "keyword": "_001_",
        "start": 0,
        "duration": 10,
        "note": "어린이의 순수한 기도로 기도 시간을 연다",
    },
    {
        "section": "기도",
        "family": "수혁",
        "folder": "수혁(2)",
        "keyword": "_001_",
        "start": 0,
        "duration": 10,
        "note": "청소년의 간절한 기도",
    },
    {
        "section": "기도",
        "family": "우진아인",
        "folder": "우진아인(2)",
        "keyword": "_034_",
        "start": 0,
        "duration": 12,
        "note": "선한 목자 되신 주님께 드리는 가정 기도",
    },
    {
        "section": "기도",
        "family": "소유사랑",
        "folder": "소유사랑(2)",
        "keyword": "_046_",
        "start": 0,
        "duration": 10,
        "note": "온 가족이 함께하는 마무리 기도",
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
    return ColorClip(
        size=FRAME_SIZE, color=(8, 8, 8), duration=actual_duration
    ).with_audio(audio)


def build_clip(path, start, duration):
    if path.endswith(".mp4"):
        return build_video_clip(path, start, duration)
    return build_audio_clip(path, start, duration)


def seconds_to_mmss(value):
    total_seconds = int(round(value))
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


def build_storyboard_markdown(total_duration):
    lines = [
        "# ClaudeCode 스토리보드",
        "",
        "## 목표",
        "교회 대예배에서 상영할 약 3분 분량의 가정예배 모음 영상을 구성한다.",
        "6개 가정(소유사랑, 우진아인, 이안이서, 지호리호, 해준해나)과 청소년(수혁)이 모두 포함된다.",
        "",
        "## 편집 의도",
        "예배의 자연스러운 흐름을 따라 찬양 → 말씀봉독 → 나눔 → 기도 순서로 구성했다.",
        "각 가정의 개성이 드러나면서도 하나의 예배처럼 이어지도록 클립을 배치했다.",
        "찬양에서는 기쁨과 활력을, 말씀에서는 경건함을, 나눔에서는 따뜻함을,",
        "기도에서는 간절함을 담아 감정의 흐름이 자연스럽게 이어지도록 했다.",
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
            "- 모든 가정이 최소 2회 이상 등장한다.",
            "- 수혁(청소년) 파트는 음성 파일이므로 어두운 배경 위 원본 음성으로 처리한다.",
            "- 별도 배경음악 없이 원본 예배 음성의 현장감을 살린다.",
            "- 찬양 → 말씀 → 나눔 → 기도의 예배 흐름을 따른다.",
            f"- 예상 총 길이: 약 {total_duration:.0f}초",
        ]
    )
    return "\n".join(lines) + "\n"


def build_process_markdown(used_rows, total_duration):
    family_order = []
    family_count = {}
    seen = set()
    for row in used_rows:
        family_count[row["family"]] = family_count.get(row["family"], 0) + 1
        if row["family"] not in seen:
            family_order.append(row["family"])
            seen.add(row["family"])

    lines = [
        "# ClaudeCode 제작 과정",
        "",
        "## 작업 기준",
        "- `요구사항.md`를 기준으로 작업했으며, 다른 AI의 결과물은 참고하지 않았다.",
        "- `media/output`의 분절된 클립과 `_summary.txt` 분석 로그를 검토하여 클립을 선별했다.",
        "- 결과물과 문서는 모두 `media/result/ClaudeCode`에 저장한다.",
        "",
        "## 클립 선별 기준",
        "1. **음성 품질**: Whisper 인식이 명확하고 잡음이 적은 구간 우선",
        "2. **메시지 전달력**: 예배의 핵심 메시지가 담긴 구간 선택",
        "3. **가정 균형**: 모든 가정이 최소 2회 이상 등장하도록 배분",
        "4. **흐름 연결**: 찬양→말씀→나눔→기도의 예배 순서를 따름",
        "",
        "## 편집 흐름",
        "1. **찬양** (약 50초): 5개 가정의 찬양으로 예배의 기쁨을 보여준다.",
        "2. **말씀봉독** (약 30초): 청소년과 가정의 성경 봉독으로 말씀을 세운다.",
        "3. **나눔** (약 48초): 각 가정 아버지들의 따뜻한 말씀 나눔.",
        "4. **기도** (약 42초): 어린이부터 청소년까지 세대를 아우르는 기도로 마무리.",
        "",
        "## 포함된 가정",
    ]

    for family in family_order:
        lines.append(f"- {family} ({family_count[family]}회 등장)")

    lines.extend(
        [
            "",
            "## 결과 요약",
            f"- 총 클립 수: {len(used_rows)}개",
            f"- 예상 총 길이: 약 {total_duration:.0f}초",
            f"- 결과 파일: `{os.path.join(RESULT_DIR, OUTPUT_FILENAME)}`",
            "",
            "## 추가 작업 및 개선 방향",
            "- **자막 삽입**: 가정 이름이나 핵심 성경 구절 자막을 넣으면 전달력이 높아진다.",
            "- **장면 전환 효과**: crossfade(0.5초)를 적용하면 클립 간 전환이 부드러워진다.",
            "- **음량 정규화**: 가정별 녹음 환경이 달라 음량 편차가 있으므로 정규화가 필요하다.",
            "- **수혁 오디오 구간**: 검은 배경 대신 성경 구절 이미지나 교회 로고를 삽입하면 좋다.",
            "- **배경음악**: 잔잔한 피아노 반주를 깔면 통일감을 줄 수 있다.",
            "- **인트로/아웃트로**: 교회 로고와 제목 타이틀 카드를 추가하면 완성도가 올라간다.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_used_files(result_dir, used_rows):
    manifest_path = os.path.join(result_dir, USED_FILES_FILENAME)
    with open(manifest_path, "w", encoding="utf-8") as handle:
        handle.write("# ClaudeCode 사용 파일 목록\n\n")
        handle.write("| 순서 | 구간 | 가정 | 폴더 | 파일 | 비고 |\n")
        handle.write("| --- | --- | --- | --- | --- | --- |\n")
        for index, row in enumerate(used_rows, start=1):
            handle.write(
                f"| {index} | {row['section']} | {row['family']} | {row['folder']} | "
                f"`{os.path.basename(row['path'])}` | {row['note']} |\n"
            )


def write_documents(result_dir, used_rows, total_duration):
    storyboard_path = os.path.join(result_dir, STORYBOARD_FILENAME)
    with open(storyboard_path, "w", encoding="utf-8") as handle:
        handle.write(build_storyboard_markdown(total_duration))

    process_path = os.path.join(result_dir, PROCESS_FILENAME)
    with open(process_path, "w", encoding="utf-8") as handle:
        handle.write(build_process_markdown(used_rows, total_duration))


def create_final_video():
    os.makedirs(RESULT_DIR, exist_ok=True)

    final_clips = []
    used_rows = []

    for item in CLIPS_CONFIG:
        target_file = find_target_file(OUTPUT_BASE, item["folder"], item["keyword"])
        print(f"처리 중: {target_file}")

        clip = build_clip(target_file, item["start"], item["duration"])
        if clip is None:
            print(f"  > 건너뜀 (길이 부족)")
            continue

        print(f"  > 사용 길이: {clip.duration:.2f}초")
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
    print(f"\n총 {len(final_clips)}개 클립, 예상 길이: {total_duration:.1f}초")
    print("영상 병합 중...")

    final_video = concatenate_videoclips(final_clips, method="compose")
    output_path = os.path.join(RESULT_DIR, OUTPUT_FILENAME)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=FPS)

    write_used_files(RESULT_DIR, used_rows)
    write_documents(RESULT_DIR, used_rows, total_duration)

    final_video.close()
    for clip in final_clips:
        clip.close()

    print(f"\n최종 영상 생성 완료: {output_path}")
    print(f"문서 생성 완료: {RESULT_DIR}/")


if __name__ == "__main__":
    create_final_video()
