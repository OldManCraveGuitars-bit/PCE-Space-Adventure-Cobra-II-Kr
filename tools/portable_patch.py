"""Portable Cobra II patch application with complete preflight and SHA checks."""
import argparse
import hashlib
import json
import os
import shutil
import struct
import sys
import zlib
from pathlib import Path
from disc import ROOT, read_tracks

SECTOR = 2352
CHUNK = 1024 * 1024
CUE_NAME = 'cobra2-ko-experimental.cue'


def file_sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def source_location(source, cue=None):
    source = Path(source).resolve()
    if source.is_file():
        if source.suffix.lower() != '.cue' or cue is not None:
            raise ValueError('원본 폴더 또는 원본 CUE 하나를 지정하세요.')
        return source.parent, source
    if not source.is_dir():
        raise ValueError('원본 폴더를 찾을 수 없습니다: ' + str(source))
    if cue is not None:
        selected = Path(cue)
        selected = selected.resolve() if selected.is_absolute() else (source / selected).resolve()
        if selected.parent != source or selected.suffix.lower() != '.cue' or not selected.is_file():
            raise ValueError('CUE는 지정한 원본 폴더 안에 있어야 합니다.')
        return source, selected
    return source, None


def source_cue(source, selected, manifest):
    if selected is None:
        # The manifest can come from another computer or operating system.
        # Its original absolute path is never opened.
        basename = str(manifest['original_cue']).replace('\\', '/').rsplit('/', 1)[-1]
        preferred = source / basename
        candidates = [preferred] if preferred.is_file() else sorted(
            (p for p in source.iterdir() if p.is_file() and p.suffix.lower() == '.cue'),
            key=lambda p: p.name.casefold())
        if len(candidates) != 1:
            raise ValueError('원본 CUE를 하나로 고를 수 없습니다. CUE 파일을 직접 지정하거나 --cue를 사용하세요.')
        selected = candidates[0]
    if file_sha(selected) != manifest['original_cue_sha256']:
        raise ValueError('지원하는 원본 CUE와 해시가 다릅니다: ' + selected.name)
    actual = read_tracks(selected)
    keys = ('number', 'type', 'file', 'index0', 'index1')
    expected = manifest['tracks']
    if len(actual) != len(expected) or any(
            any(a.get(k) != b.get(k) for k in keys) for a, b in zip(actual, expected)):
        raise ValueError('원본 CUE의 트랙 구성이 다릅니다.')
    return selected


def patch_records(path, manifest):
    body = memoryview(zlib.decompress(Path(path).read_bytes()))
    cursor = 0

    def take(count):
        nonlocal cursor
        if count < 0 or cursor + count > len(body):
            raise ValueError('패치 파일이 잘렸거나 손상되었습니다.')
        value = body[cursor:cursor + count]
        cursor += count
        return value

    if take(9).tobytes() != b'COBRA2KR1':
        raise ValueError('지원하는 코브라 2 패치가 아닙니다.')
    count, = struct.unpack('<I', take(4))
    data = {t['number']: t for t in manifest['tracks'] if t['type'] != 'AUDIO'}
    if count != len(data):
        raise ValueError('패치의 데이터 트랙 수가 다릅니다.')
    result = []
    seen = set()
    for _ in range(count):
        number, size, sectors = struct.unpack('<IQI', take(16))
        original = take(32).hex()
        expected = take(32).hex()
        if number not in data or number in seen:
            raise ValueError('패치에 중복되거나 지원하지 않는 트랙이 있습니다.')
        seen.add(number)
        meta = data[number]
        if size != meta['file_bytes'] or original != meta['sha256'] or sectors > size // SECTOR:
            raise ValueError('패치의 원본 트랙 정보가 다릅니다.')
        changes = []
        previous = -1
        for _ in range(sectors):
            sector, = struct.unpack('<I', take(4))
            raw = take(SECTOR).tobytes()
            if sector <= previous or (sector + 1) * SECTOR > size:
                raise ValueError('패치의 섹터 순서나 범위가 잘못되었습니다.')
            previous = sector
            changes.append((sector, raw))
        result.append(dict(number=number, size=size, expected=expected, changes=changes))
    if cursor != len(body) or seen != set(data):
        raise ValueError('패치의 끝 또는 트랙 구성이 잘못되었습니다.')
    return result


def patched_chunks(path, record):
    with Path(path).open('rb') as stream:
        position = 0
        for sector, raw in record['changes']:
            end = sector * SECTOR
            while position < end:
                chunk = stream.read(min(CHUNK, end - position))
                if not chunk:
                    raise ValueError('읽는 도중 원본 트랙 길이가 달라졌습니다.')
                position += len(chunk)
                yield chunk
            stream.seek(SECTOR, 1)
            position += SECTOR
            yield raw
        while position < record['size']:
            chunk = stream.read(min(CHUNK, record['size'] - position))
            if not chunk:
                raise ValueError('읽는 도중 원본 트랙 길이가 달라졌습니다.')
            position += len(chunk)
            yield chunk


def apply(source, patch, output=None, *, cue=None, verify_only=False, link_audio=False):
    source, selected = source_location(source, cue)
    output = (Path(output) if output is not None else source.with_name(source.name + ' [KO-preview]')).resolve()
    if source == output or source in output.parents:
        raise ValueError('출력은 원본 폴더 바깥의 별도 폴더여야 합니다.')
    manifest = json.loads((ROOT / 'data/disc_manifest.json').read_text(encoding='utf-8'))
    selected = source_cue(source, selected, manifest)
    records = patch_records(patch, manifest)
    targets = [output / f'cobra2-ko-track{t["number"]:02}.bin' for t in manifest['tracks']] + [output / CUE_NAME]
    if not verify_only:
        for path in targets:
            if path.exists():
                raise FileExistsError('기존 출력 파일을 덮어쓰지 않습니다: ' + str(path))
    for meta in manifest['tracks']:
        path = source / meta['file']
        if path.resolve().parent != source or not path.is_file():
            raise ValueError('원본 트랙을 찾을 수 없습니다: ' + meta['file'])
        if path.stat().st_size != meta['file_bytes'] or file_sha(path) != meta['sha256']:
            raise ValueError('원본 트랙의 크기 또는 해시가 다릅니다: ' + meta['file'])
    result = []
    # Verify both reconstructed data tracks before writing the first file.
    for record in records:
        meta = next(t for t in manifest['tracks'] if t['number'] == record['number'])
        digest = hashlib.sha256()
        for chunk in patched_chunks(source / meta['file'], record):
            digest.update(chunk)
        if digest.hexdigest() != record['expected']:
            raise ValueError('패치를 적용한 데이터의 해시가 맞지 않습니다.')
        result.append(dict(track=record['number'], sha256=record['expected']))
    if verify_only:
        return result
    created = []
    created_directory = not output.exists()
    output.mkdir(parents=True, exist_ok=True)
    try:
        for record in records:
            meta = next(t for t in manifest['tracks'] if t['number'] == record['number'])
            path = output / f'cobra2-ko-track{record["number"]:02}.bin'
            digest = hashlib.sha256()
            with path.open('xb') as stream:
                created.append((path, path.stat().st_ino))
                for chunk in patched_chunks(source / meta['file'], record):
                    stream.write(chunk)
                    digest.update(chunk)
            if digest.hexdigest() != record['expected']:
                raise ValueError('저장한 데이터의 해시가 맞지 않습니다.')
        for meta in manifest['tracks']:
            if meta['type'] != 'AUDIO':
                continue
            path = output / f'cobra2-ko-track{meta["number"]:02}.bin'
            if link_audio:
                try:
                    os.link(source / meta['file'], path)
                except OSError as error:
                    raise ValueError('음성 하드링크를 만들 수 없습니다. 다른 출력 위치를 선택하거나 --link-audio 없이 실행하세요.') from error
                created.append((path, path.stat().st_ino))
            else:
                with path.open('xb') as stream:
                    created.append((path, path.stat().st_ino))
                    with (source / meta['file']).open('rb') as original:
                        shutil.copyfileobj(original, stream, CHUNK)
            if file_sha(path) != meta['sha256']:
                raise ValueError('저장한 음성 트랙의 해시가 맞지 않습니다.')
        text = selected.read_text(encoding='utf-8-sig')
        for meta in manifest['tracks']:
            text = text.replace(meta['file'], f'cobra2-ko-track{meta["number"]:02}.bin')
        path = output / CUE_NAME
        with path.open('x', encoding='utf-8') as stream:
            created.append((path, path.stat().st_ino))
            stream.write(text)
    except BaseException:
        # Remove only this call's exclusively created files, never originals
        # or existing outputs. No recursive cleanup is performed.
        for path, identity in reversed(created):
            assert path.resolve().parent == output and not path.is_symlink()
            if path.exists() and path.stat().st_ino == identity:
                path.unlink()
        if created_directory and output.is_dir() and not any(output.iterdir()):
            output.rmdir()
        raise
    return result


def main():
    parser = argparse.ArgumentParser(description='코브라 2 검수용 패치 적용. 원본 CUE를 끌어 놓거나 원본 폴더를 지정하세요.')
    parser.add_argument('source_folder', help='원본 CUE 또는 원본 트랙이 들어 있는 폴더')
    parser.add_argument('output_folder', nargs='?', help='생략하면 원본 폴더 옆에 [KO-preview] 폴더를 만듭니다.')
    parser.add_argument('--patch', default=str(ROOT / 'build/cobra2-ko-experimental.c2kp'))
    parser.add_argument('--cue', help='원본 폴더에 CUE가 여러 개일 때 선택할 CUE 파일명')
    parser.add_argument('--verify-only', action='store_true', help='입력·패치 해시만 검사하고 파일을 만들지 않습니다.')
    parser.add_argument('--link-audio', action='store_true', help='같은 드라이브의 음성 트랙을 하드링크로 공유하여 복사를 줄입니다.')
    args = parser.parse_args()
    try:
        source, _ = source_location(args.source_folder, args.cue)
        output = Path(args.output_folder).resolve() if args.output_folder else source.with_name(source.name + ' [KO-preview]')
        result = apply(args.source_folder, args.patch, output, cue=args.cue, verify_only=args.verify_only, link_audio=args.link_audio)
    except (OSError, ValueError, zlib.error, struct.error) as error:
        parser.exit(2, '패치 적용 실패: ' + str(error) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print('검증 완료: 파일을 만들지 않았습니다.' if args.verify_only else '출력 폴더: ' + str(output), file=sys.stderr)
