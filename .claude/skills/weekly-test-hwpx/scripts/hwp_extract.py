"""변형된 한글 기본(.hwp) 읽기 — 문단 텍스트(수식 자리 ◆)와 수식 스크립트·크기 추출

    python3 hwp_extract.py 기본.hwp 텍스트.txt 수식크기.json
수식크기.json 은 build_weekly.py --eqsz 로 넘기면 한글이 잰 수식 크기를 그대로 쓴다.
"""
import json, struct, sys, zlib
import olefile

def records(data):
    i = 0
    while i < len(data):
        h = struct.unpack('<I', data[i:i + 4])[0]; i += 4
        tag, size = h & 0x3ff, h >> 20
        if size == 0xfff:
            size = struct.unpack('<I', data[i:i + 4])[0]; i += 4
        yield tag, data[i:i + size]; i += size

def main(src, txt_out, eq_out):
    f = olefile.OleFileIO(src)
    comp = f.openstream('FileHeader').read()[36] & 1
    lines, sizes, last = [], {}, None
    for s in f.listdir():
        if s[0] != 'BodyText':
            continue
        d = f.openstream(s).read()
        if comp:
            d = zlib.decompress(d, -15)
        for tag, rec in records(d):
            if tag == 67:                                   # PARA_TEXT
                t, k, out = rec.decode('utf-16le', 'replace'), 0, ''
                while k < len(t):
                    c = ord(t[k])
                    if c < 32:
                        if c in (0, 10, 13, 24, 25, 26, 27, 28, 29, 30, 31):
                            k += 1
                        else:
                            out += '◆'; k += 8
                    else:
                        out += t[k]; k += 1
                lines.append(out)
            elif tag == 71 and rec[:4] == b'deqe':          # 수식 개체 머리
                last = struct.unpack('<iiiII', rec[4:24])
            elif tag == 88:                                 # EQEDIT
                n = struct.unpack('<H', rec[4:6])[0]
                script = rec[6:6 + 2 * n].decode('utf-16le')
                p = 6 + 2 * n
                _, _, bl = struct.unpack('<IIh', rec[p:p + 10])
                lines.append('    [수식] ' + script)
                if last:
                    sizes[script] = [last[3], last[4], bl]
    open(txt_out, 'w', encoding='utf8').write('\n'.join(lines))
    json.dump(sizes, open(eq_out, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
    print(f'문단 {len(lines)}줄, 수식 {len(sizes)}개')

if __name__ == '__main__':
    main(*sys.argv[1:4])
