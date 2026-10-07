# 목동고 결과물 → 문제 내용을 지운 주간테스트 템플릿
import re, os, sys, shutil, zipfile
SRC, OUT, SAMPLE_IMG = sys.argv[1], sys.argv[2], sys.argv[3]
tmp = OUT + '.d'
shutil.rmtree(tmp, ignore_errors=True)
with zipfile.ZipFile(SRC) as z:
    z.extractall(tmp)
    order = [i.filename for i in z.infolist()]
s1 = open(f'{tmp}/Contents/section1.xml', encoding='utf8').read()
head = s1[:s1.index('<hp:p ')]
pat = re.compile(r'<hp:p [^>]*>|</hp:p>')
depth = 0; paras = []
for m in pat.finditer(s1):
    if m.group(0).startswith('<hp:p '):
        if depth == 0: st = m.start()
        depth += 1
    else:
        depth -= 1
        if depth == 0: paras.append(s1[st:m.end()])
def strip(p):
    p = re.sub(r'<hp:linesegarray>.*?</hp:linesegarray>', '', p, flags=re.S)
    p = re.sub(r'<hp:script>(.*?)</hp:script>', lambda m: m.group(0) if m.group(1) == 'NGD' else '<hp:script>x</hp:script>', p, flags=re.S)
    def t(m):
        txt = m.group(1)
        if txt in ('&lt; 조 건 &gt;', '&lt; 보 기 &gt;', '※ 여기서 부터는 서답형 문제입니다.', '[서답형 1]', ' [정답] ④'):
            return m.group(0)
        if txt.strip() in ('①', '②', '③', '④', '⑤'): return m.group(0)
        return '<hp:t>예시</hp:t>' if txt.strip() else m.group(0)
    p = re.sub(r'<hp:t>([^<]*)</hp:t>', t, p)
    return p
# 견본 순서: 0 첫 문단, 1 문항, 2 빈 줄, 3 보기1줄, 4 보기2줄, 5 단 나누기, 6 가운데 수식, 7 그림,
#            8 조건 상자, 9 긴 보기, 10 서답형 안내, 11 서답형 제목, 12 소문항
idx = [0, 2, 3, 4, 5, 43, 65, 117, 236, 149, 334, 335, 339]
ex = [paras[0]] + [strip(paras[i]) for i in idx[1:]]
ex[0] = re.sub(r'<hp:linesegarray>.*?</hp:linesegarray>', '', ex[0], flags=re.S)
open(f'{tmp}/Contents/section1.xml', 'w', encoding='utf8').write(head + ''.join(ex) + '</hs:sec>')
s0 = open(f'{tmp}/Contents/section0.xml', encoding='utf8').read()
s0 = s0.replace('주간테스트 - 2026년 2학기 중간 미적분1 목동고', '{TITLE}')
s0 = s0.replace('출제범위 :  함수의 극한 – 도함수', '출제범위 :  {RANGE}')
s0 = s0.replace('60점 만점', '{TOTAL}점 만점')
s0 = re.sub(r'<hp:linesegarray>.*?</hp:linesegarray>', '', s0, flags=re.S)
open(f'{tmp}/Contents/section0.xml', 'w', encoding='utf8').write(s0)
os.remove(f'{tmp}/BinData/image4.png')
shutil.copy(SAMPLE_IMG, f'{tmp}/BinData/image3.png')
hpf = open(f'{tmp}/Contents/content.hpf', encoding='utf8').read()
hpf = re.sub(r'<opf:item id="image4"[^>]*/>', '', hpf)
hpf = re.sub(r'<opf:title>.*?</opf:title>', '<opf:title>주간테스트</opf:title>', hpf)
open(f'{tmp}/Contents/content.hpf', 'w', encoding='utf8').write(hpf)
open(f'{tmp}/Preview/PrvText.txt', 'w', encoding='utf8').write('주간테스트')
if os.path.exists(OUT): os.remove(OUT)
with zipfile.ZipFile(OUT, 'w') as z:
    for name in order:
        if name == 'BinData/image4.png': continue
        z.write(f'{tmp}/{name}', name, compress_type=zipfile.ZIP_STORED if name == 'mimetype' else zipfile.ZIP_DEFLATED)
shutil.rmtree(tmp)
print('ok', len(ex))
