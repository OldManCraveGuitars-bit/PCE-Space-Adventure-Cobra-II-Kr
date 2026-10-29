# SHA-256 — v0.8

지원 원본은 `Space Adventure Cobra II - Densetsu no Otoko (Japan)`의 9개 BIN + CUE입니다. 아래 SHA-256은 파일 전체 기준입니다.

## 원본 CUE / BIN

| 파일 | 바이트 | SHA-256 |
| --- | ---: | --- |
| `Space Adventure Cobra II - Densetsu no Otoko (Japan).cue` | 1,209 | `bd843ff3fe1543352c3a73612c1f255fb9dafbaa8b9cd3fbc868a393beffb9ba` |
| `Space Adventure Cobra II - Densetsu no Otoko (Japan) (Track 1).bin` | 7,916,832 | `53b50bd6addf7e50dbd8620ceda2603278e3d8fdec183498c11308ad5ac2cacc` |
| `Space Adventure Cobra II - Densetsu no Otoko (Japan) (Track 2).bin` | 161,126,112 | `1d83319da45d2d4a8997a1bb9e0c542ad702474169940721913adf22647c2a60` |
| `Space Adventure Cobra II - Densetsu no Otoko (Japan) (Track 3).bin` | 25,730,880 | `23b95c11fe0ee194da31423b74b2406d891fdac336c4dd776f64a4d8f3b5f030` |
| `Space Adventure Cobra II - Densetsu no Otoko (Japan) (Track 4).bin` | 29,585,808 | `7ca247ec1496ba3fdfa6aaec20a02a43c6c2e0e753c6a441ecd212a677572fa0` |
| `Space Adventure Cobra II - Densetsu no Otoko (Japan) (Track 5).bin` | 10,965,024 | `b1735dc005e1dab59bc4aaa1cca0296032aa3fafe6c8efe8747337048b6a3807` |
| `Space Adventure Cobra II - Densetsu no Otoko (Japan) (Track 6).bin` | 6,197,520 | `df82c8e9a986cd2e7b70cbf7db0d5db2f16eb61b3a197ed74b9333eafa13ceb6` |
| `Space Adventure Cobra II - Densetsu no Otoko (Japan) (Track 7).bin` | 10,012,464 | `1f88db2bf25207e10d9299eb5ab7cdb15dea6daa1aff36fafe057fb7e667958c` |
| `Space Adventure Cobra II - Densetsu no Otoko (Japan) (Track 8).bin` | 5,675,376 | `71bac2abc597de73d6dffa779278e9d6c92b880a50aa764af78c4658192de4b7` |
| `Space Adventure Cobra II - Densetsu no Otoko (Japan) (Track 9).bin` | 160,775,664 | `b0972e76055771de3b3569c60225ef1715c1e891eda3fcb64b4d4543ce2a4d5f` |

## 패치 적용 결과

| 파일 | SHA-256 |
| --- | --- |
| `cobra2-ko-experimental.cue` | `f1d255511a5a39b3776424df63df80fc794086bbf13176ead18b8c4a1417c527` |
| `cobra2-ko-track01.bin` | `53b50bd6addf7e50dbd8620ceda2603278e3d8fdec183498c11308ad5ac2cacc` |
| `cobra2-ko-track02.bin` | `f269eb8f442b09a0384635598ee7e89c0cd5b7889f2e385ae5e301325be19c57` |
| `cobra2-ko-track03.bin` | `23b95c11fe0ee194da31423b74b2406d891fdac336c4dd776f64a4d8f3b5f030` |
| `cobra2-ko-track04.bin` | `7ca247ec1496ba3fdfa6aaec20a02a43c6c2e0e753c6a441ecd212a677572fa0` |
| `cobra2-ko-track05.bin` | `b1735dc005e1dab59bc4aaa1cca0296032aa3fafe6c8efe8747337048b6a3807` |
| `cobra2-ko-track06.bin` | `df82c8e9a986cd2e7b70cbf7db0d5db2f16eb61b3a197ed74b9333eafa13ceb6` |
| `cobra2-ko-track07.bin` | `1f88db2bf25207e10d9299eb5ab7cdb15dea6daa1aff36fafe057fb7e667958c` |
| `cobra2-ko-track08.bin` | `71bac2abc597de73d6dffa779278e9d6c92b880a50aa764af78c4658192de4b7` |
| `cobra2-ko-track09.bin` | `c76123a6f642824eeed49bfda55627f0e6001130883a54aa189e5f7c4f213fe9` |

## 패치와 실행 파일

| 파일 | SHA-256 |
| --- | --- |
| `build/cobra2-ko-experimental.c2kp` | `cf2ed9a4ce963f42926d2dd44fa0d176bc40bfe9774776339a2c1ec63efce598` |
| `Cobra2PatchApplier.exe` | `7d6dc409fb67caa34775b129a0330fe635fc2afed4e0c2bf3507a3d55940f9c6` |

## 논리 데이터 빌드

`5657193d1082175d700d75fa61e20668c0921818f5bcc3a5f085091843f03e67`

이 값은 데이터 트랙의 사용자 데이터(139,841,536바이트)에 대한 SHA-256입니다. 2,352바이트 섹터의 BIN 전체 해시와 다릅니다. 트랙 02/09 결과 해시는 위 표를 사용하세요.

## 다운로드 검증

릴리스의 `SHA256SUMS.txt`는 ZIP·EXE·차이 패치와 스크린샷 ZIP을 검사합니다. PowerShell 예: `Get-FileHash .\PCE-Space-Adventure-Cobra-II-Kr-v0.8.zip -Algorithm SHA256`.
