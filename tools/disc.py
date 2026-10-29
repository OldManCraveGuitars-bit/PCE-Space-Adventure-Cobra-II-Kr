"""CUE / MODE1 sector handling. All disc positions are explicit, never inferred from names."""
from pathlib import Path
import hashlib
import re
import struct
import sys

ROOT = Path(sys.executable).resolve().parent if getattr(sys,'frozen',False) else Path(__file__).resolve().parents[1]
RAW_SECTOR = 2352
USER_SECTOR = 2048

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def read_tracks(cue_path):
    tracks = []
    file_name = None
    for line in Path(cue_path).read_text(encoding='utf-8-sig').splitlines():
        file_match = re.search(r'FILE "(.+)" BINARY', line)
        track_match = re.search(r'TRACK (\d+) (\S+)', line)
        index_match = re.search(r'INDEX (\d+) (\d+):(\d+):(\d+)', line)
        if file_match:
            file_name = file_match[1]
        elif track_match:
            tracks.append({'number': int(track_match[1]), 'type': track_match[2], 'file': file_name})
        elif index_match:
            idx, minutes, seconds, frames = map(int, index_match.groups())
            tracks[-1][f'index{idx}'] = (minutes * 60 + seconds) * 75 + frames
    for i, track in enumerate(tracks):
        track['end'] = tracks[i+1].get('index0', tracks[i+1]['index1']) if i+1 < len(tracks) else None
    return tracks

def user_data(raw, track):
    end = track['end'] if track['end'] is not None else len(raw)//RAW_SECTOR
    return b''.join(raw[s*RAW_SECTOR+16:s*RAW_SECTOR+2064] for s in range(track['index1'],end))

# ECMA-130 MODE1 EDC and P/Q parity. Audio and MSF/sync headers are never rewritten.
EDC = []
ECC_F = []
ECC_B = [0]*256
for i in range(256):
    edc = i
    for _ in range(8):
        edc = (edc >> 1) ^ (0xD8018001 if edc & 1 else 0)
    EDC.append(edc)
    value = (i << 1) ^ (0x11D if i & 0x80 else 0)
    ECC_F.append(value)
    ECC_B[i ^ value] = i

def parity(source, major_count, minor_count, major_mult, minor_inc):
    size = major_count * minor_count
    out = bytearray(major_count * 2)
    for major in range(major_count):
        index = (major >> 1) * major_mult + (major & 1)
        a = b = 0
        for _ in range(minor_count):
            value = source[index]
            index = (index + minor_inc) % size
            a ^= value
            b ^= value
            a = ECC_F[a]
        a = ECC_B[ECC_F[a] ^ b]
        out[major] = a
        out[major+major_count] = a ^ b
    return out

def repair_mode1(sector):
    sector = bytearray(sector)
    if len(sector) != 2352 or sector[15] != 1:
        raise ValueError('Expected an intact MODE1/2352 sector')
    edc = 0
    for value in sector[:2064]:
        edc = (edc >> 8) ^ EDC[(edc ^ value) & 255]
    struct.pack_into('<I', sector, 2064, edc)
    sector[2068:2076] = b'\0'*8
    sector[2076:2248] = parity(sector[12:2076],86,24,2,86)
    sector[2248:2352] = parity(sector[12:2248],52,43,86,88)
    return sector

def patch_user_data(raw, tracks, original, replacement):
    if len(original) != len(replacement):
        raise ValueError('Disc layout changes are forbidden')
    changed = [s for s in range((len(original)+2047)//2048)
               if original[s*2048:(s+1)*2048] != replacement[s*2048:(s+1)*2048]]
    output = bytearray(raw)
    changed_raw = set()
    for track in tracks:
        if track['type'] != 'MODE1/2352':
            continue
        available = (track['end'] if track['end'] is not None else len(raw)//2352)-track['index1']
        for s in changed:
            if s >= available:
                raise ValueError('Patch extends beyond a mirrored data track')
            pos = (track['index1']+s)*2352
            if output[pos+16:pos+2064] != original[s*2048:(s+1)*2048]:
                raise ValueError(f'Mirror mismatch at track {track["number"]}, sector {s}')
            sector = bytearray(output[pos:pos+2352])
            sector[16:2064] = replacement[s*2048:(s+1)*2048]
            output[pos:pos+2352] = repair_mode1(sector)
            changed_raw.add(pos//2352)
    return output, sorted(changed_raw)
