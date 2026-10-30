<p align="center"><img src="screenshots/title.png" alt="스페이스 코브라 II 한글 타이틀" width="512"></p>

# PCE-Space-Adventure-Cobra-II-Kr

**스페이스 어드벤처 코브라 II — 전설의 사나이 · 비공식 한국어 패치 v0.81**

PC Engine Super CD-ROM² 일본판의 한국어 검수판입니다. **한글화: 기타 깎는 노인** · 2026-10-30.

**[v0.81 릴리스](https://github.com/OldManCraveGuitars-bit/PCE-Space-Adventure-Cobra-II-Kr/releases/tag/v0.81)** · **[Windows 패처 ZIP](https://github.com/OldManCraveGuitars-bit/PCE-Space-Adventure-Cobra-II-Kr/releases/download/v0.81/PCE-Space-Adventure-Cobra-II-Kr-v0.81.zip)**

ZIP 전체를 압축 해제해 사용합니다. Python 설치 없이 실행하는 패처 EXE와 원본 선택 창, 차이 패치, 사용법, SHA-256, 실제 스크린샷을 포함합니다. 원본 게임·BIOS는 포함하지 않습니다.

## v0.81 수정

- 시드 행성 착륙 후 **총기 보기 → 레이저 라이플** 설명의 번역 누락을 수정했습니다. 같은 원문이 사용된 누락 위치 8곳에 기존 검토 번역을 적용했습니다. **집광 온도 4만℃ / 0.5초 간격**의 원문 수치를 유지합니다.
- 레이디의 **헤드바 시티·유적 안내 자막 2개**를 위쪽으로 옮겨 원래 노란 설명문과 겹치지 않게 했습니다.
- **“OK, 하강할게.”**를 포함한 안내 자막 3개를 실제 게임 LOAD 후 진행과 Beetle PCE FAST 코어에서 확인했습니다. 신고된 완전 미표시는 재현되지 않았으므로 그 원인까지 해결했다고 단정하지 않습니다.

| 레이저 라이플 설명 | 레이디 안내 자막 배치 |
| --- | --- |
| ![라이플 한글 설명](screenshots/laser-rifle.png) | ![위쪽 안내 자막](screenshots/lady-arrival.png) |

이 두 장과 [하강 직전 자막](screenshots/lady-descent.png)은 v0.81 빌드 `3a7c711c`의 실제 화면입니다. [수정 전 비교와 모든 스크린샷](screenshots/README.md)

## 한글화 내용

본문 원장 5,052개 중 **검토 번역 4,998개**, 코드·중복 경계 제외 54개입니다. 추가 음성 자막 **1,024개**, 오프닝 스프라이트 자막 18개, 타이틀·부제·작가명·메뉴·일본어 엔딩 크레딧 89개 필드를 한글화했습니다. 원래 영문·그림·음악·음성과 타이틀 오른쪽 반짝임을 보존합니다. 한글 12×12, ASCII 공백 6픽셀을 사용합니다.

## 적용 방법

1. 지원하는 **일본판 원본 CUE와 9개 BIN**을 한 폴더에 준비합니다. [지원 원본 해시](HASHES.md)
2. 패처 ZIP을 새 폴더에 전부 풉니다. `data`, `build` 폴더를 포함한 구성을 유지합니다.
3. **패치 적용.cmd**를 더블클릭하고 원본 CUE를 고릅니다. CUE를 CMD에 끌어 놓아도 됩니다.
4. 선택 창으로 실행하면 원본 폴더 옆에 **[KO v0.81]** 폴더가 생성됩니다. 끌어 놓기의 기본 출력 이름은 `[KO-preview]`입니다. 기존 파일은 덮어쓰지 않습니다.
5. 생성된 **cobra2-ko-experimental.cue**를 실행합니다. 모든 출력 BIN과 같은 폴더에 두며 **Super CD-ROM² System Card 3.0**이 필요합니다.

출력 공간은 약 400MiB 이상 필요합니다. CHD·단일 BIN·다른 덤프는 직접 입력으로 지원하지 않습니다. CUE의 파일명과 위치는 바꿀 수 있지만, CUE 내용과 참조 BIN의 이름·크기·해시는 매니페스트와 일치해야 합니다. 이미 패치된 이미지에 덧씌우지 않습니다.

```bat
Cobra2PatchApplier.exe "D:\원본\원본.cue" "D:\코브라2 한글 v0.81"
Cobra2PatchApplier.exe "D:\원본\원본.cue" --verify-only
Cobra2PatchApplier.exe "D:\원본\원본.cue" "D:\코브라2 한글 v0.81" --link-audio
```

`--verify-only`는 파일 생성 없이 결과 데이터 해시까지 검사합니다. `--link-audio`는 같은 드라이브의 음성 BIN을 하드링크로 공유해 추가 복사를 줄입니다. 공유한 BIN은 직접 편집하지 마세요. 소스 실행은 Python 3.11 이상에서 `python tools/apply_patch.py 원본.cue 출력폴더`를 사용합니다.

새 판은 에뮬레이터를 완전히 다시 시작해 실행합니다. 이전 판의 상태 저장은 당시 코드를 복원하므로 **게임 안의 LOAD**로 이어갑니다. 기존 SAVE·상태 파일은 보관하고 저장 파일 이름·위치는 사용 환경에 맞춥니다.

## 검수 범위

GUI/CLI 13개 출력 일치와 정적 검사 7개, 실제 시드 착륙·라이플 설명, 안내 자막의 원음 대응·글자·외곽선·스프라이트·종료 후 복구를 확인했습니다. v0.81의 안내 세 자막은 Beetle PCE FAST v1.31.0.0의 실제 libretro 영상 콜백에서도 확인했습니다. 이 추가 시험은 최소 실행기이며 RetroArch 앱 전체 설정을 재현한 것은 아닙니다.

이전 v0.8의 술집 앞 자막 시간 연장과 문장 14곳 교정도 포함합니다. 타이틀·오프닝 등 기존 사진은 촬영 당시 빌드 v0.8로 명시해 보존합니다. 전체 분기·매 프레임·모든 실기·사람의 전 음성 청취 완료를 주장하지 않습니다. [QA.md](QA.md) · [변경 내역](CHANGELOG.md)

원본·결과 파일 및 패치·EXE 해시는 [HASHES.md](HASHES.md), 다운로드 ZIP 해시는 릴리스의 SHA256SUMS에 기록합니다. [외부 구성요소와 글꼴](THIRD_PARTY_NOTICES.md) · [패처 소스](tools/portable_patch.py)
