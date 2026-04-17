# 다른 PC 실행 가이드

## 준비물
- 이 저장소 전체 폴더 `MakeClip`
- Python 3.14 이상
- FFmpeg

## 1. 저장소 복사
다른 PC에 `MakeClip` 폴더 전체를 그대로 복사한다.

권장:
- `media/`도 같이 복사하면 원본과 결과물을 그대로 이어서 쓸 수 있다.
- 결과물만 필요하면 `media/result/`만 따로 복사해도 된다.

## 2. Python 확인
PowerShell에서 Python 경로를 확인한다.

```powershell
python --version
```

또는 특정 경로를 직접 사용할 수 있다.

```powershell
& "C:\Users\mhhan\AppData\Local\Python\bin\python.exe" --version
```

## 3. 의존성 설치
저장소 루트에서 아래를 실행한다.

```powershell
python -m pip install -r requirements.txt
```

특정 Python 경로를 직접 쓸 때:

```powershell
& "C:\Users\mhhan\AppData\Local\Python\bin\python.exe" -m pip install -r requirements.txt
```

## 4. FFmpeg 설치
이 프로젝트는 FFmpeg가 필요하다.

현재 스크립트는 기본적으로 아래 경로를 가정한다.

```text
C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin
```

다른 PC에서 이 경로가 다르면 아래 파일들의 `ffmpeg_bin` 값을 수정해야 한다.

- `split_video.py`
- `process_kakao.py`
- `assemble_video.py`
- `assemble_video_codex.py`

## 5. 실행 순서
### 영상 분절
```powershell
python split_video.py
```

### 카카오 오디오 분절
```powershell
python process_kakao.py
```

### 이름 정리
```powershell
python rename_output.py
python rename_kakao.py
```

### 최종 영상 생성
Codex 버전 결과물:

```powershell
python assemble_video_codex.py
```

기존 Gemini 버전 결과물:

```powershell
python assemble_video.py
```

## 6. 결과 위치
- 분절 결과: `media/output/`
- 최종 결과: `media/result/Codex/` 또는 `media/result/GeminiCLI/`

## 주의사항
- `split_video.py`는 `media/output/`을 다시 만든다.
- 따라서 `media/output/` 안에 보관할 파일은 두지 않는 편이 안전하다.
- `torch`와 `whisper` 설치는 다른 패키지보다 시간이 더 걸릴 수 있다.
- GPU가 없어도 실행은 가능하지만 더 느릴 수 있다.

## 가장 간단한 이전 방법
### 결과물만 다른 PC에서 열기
아래만 복사하면 된다.
- `media/result/`

### 다른 PC에서 다시 편집/재생성하기
아래가 모두 필요하다.
- `MakeClip` 전체 폴더
- Python 설치
- `requirements.txt` 설치
- FFmpeg 설치 또는 경로 수정
