"""주간테스트 hwpx 조립기 — assets/template.hwpx 의 견본 문단을 복제해 문항을 채운다.

    python3 build_weekly.py <내용.py> <출력.hwpx> [--eqsz 수식크기.json]

내용 파일 형식은 SKILL.md 의 '내용 파일' 절 참고.
"""
import argparse, html, importlib.util, json, os, re, shutil, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, '..', 'assets', 'template.hwpx')
EASY_GAP = 16          # 쉬운 문항 2개를 한 단에 둘 때 첫 문항 뒤 빈 줄 수
SUB_GAP = 5            # 서답형 소문항 뒤 빈 줄 수(기본)

_id = [1400000000]
def nid():
    _id[0] += 1
    return str(_id[0])

def esc(t):
    return html.escape(t, quote=False)

def split_paras(xml):
    out, depth, st = [], 0, 0
    for m in re.finditer(r'<hp:p [^>]*>|</hp:p>', xml):
        if m.group(0).startswith('<hp:p '):
            if depth == 0:
                st = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                out.append(xml[st:m.end()])
    return out

# ---------- 템플릿 견본 ----------
with zipfile.ZipFile(TEMPLATE) as z:
    S1 = z.read('Contents/section1.xml').decode('utf8')
    S0 = z.read('Contents/section0.xml').decode('utf8')
EX = split_paras(S1)
(FIRST, PROBLEM, BLANK, CH1, CH2, COLBREAK, DISPLAY, PICTURE, BOX, LONGCH,
 NOTICE, HEADING, SUBQ) = EX
SEC_HEAD = S1[:S1.index('<hp:p ')]
P_OPEN = re.match(r'<hp:p [^>]*>', BLANK).group(0)                    # paraPr 3
P_CENTER = re.match(r'<hp:p [^>]*>', DISPLAY).group(0)                # paraPr 51
EQ_TPL = re.search(r'<hp:equation .*?</hp:equation>', CH1, re.S).group(0)
ENDNOTE = re.search(r'<hp:ctrl><hp:endNote .*?</hp:endNote></hp:ctrl>', PROBLEM, re.S).group(0)
AUTONUM_RUN = re.search(r'<hp:run charPrIDRef="\d+"><hp:ctrl><hp:autoNum .*?</hp:run>', ENDNOTE, re.S).group(0)

# ---------- 수식 ----------
EQSZ = {}
def eq_size(script):
    if script in EQSZ:
        w, h, bl = EQSZ[script][:3]
        return w, h, bl
    t = re.sub(r'\b(LEFT|RIGHT|lim|rarrow|over|TIMES|cases|lbrace|rbrace|le|ge|INF|prime|rm|it|sqrt|root)\b', 'x', script)
    t = re.sub(r'[`~{}\s^_&#]', '', t)
    w, h, bl = max(1, len(t)) * 560, 1125, 85
    if 'over' in script or 'lim' in script:
        h, bl = 2600, 64
    if 'cases' in script:
        h, bl = 2600 + 1100 * script.count('#'), 55
    return w, h, bl

def equation(script):
    w, h, bl = eq_size(script)
    x = re.sub(r'<hp:equation id="\d+"', f'<hp:equation id="{nid()}"', EQ_TPL, count=1)
    x = re.sub(r'baseLine="\d+"', f'baseLine="{bl}"', x, count=1)
    x = re.sub(r'<hp:sz width="\d+"', f'<hp:sz width="{w}"', x, count=1)
    x = re.sub(r'height="\d+" heightRelTo', f'height="{h}" heightRelTo', x, count=1)
    return re.sub(r'<hp:script>.*?</hp:script>', f'<hp:script>{esc(script)}</hp:script>', x, flags=re.S)

def body(s):
    """$수식$ 과 \t(탭) 을 hp:run 내부 XML 로"""
    out = ''
    for part in re.split(r'(\$.*?\$)', s):
        if not part:
            continue
        if part.startswith('$'):
            out += equation(part[1:-1])
        else:
            out += '<hp:t>' + esc(part).replace('\t', '<hp:tab width="4000" leader="0" type="1"/>') + '</hp:t>'
    return out

def para(s, opener=P_OPEN, cp='58'):
    if not s:
        return BLANK
    return f'{opener}<hp:run charPrIDRef="{cp}">{body(s)}<hp:t/></hp:run></hp:p>'

def blanks(n):
    return BLANK * n

# ---------- 미주(정답·해설) ----------
_note = [0]
def endnote(answer, sol, note=None):
    _note[0] += 1
    paras = f'{P_OPEN}{AUTONUM_RUN}<hp:run charPrIDRef="58">{body(" [정답] " + answer)}</hp:run></hp:p>'
    lines = ([note] if note else []) + list(sol)
    paras += ''.join(para(s) for s in lines)
    x = re.sub(r'number="\d+"', f'number="{_note[0]}"', ENDNOTE, count=1)
    x = re.sub(r'instId="\d+"', f'instId="{nid()}"', x, count=1)
    return re.sub(r'(<hp:subList [^>]*>).*(</hp:subList>)', lambda m: m.group(1) + paras + m.group(2), x, count=1, flags=re.S)

# ---------- 상자·그림 ----------
def box(label, lines):
    x = BOX
    x = re.sub(r'<hp:tbl id="\d+"', f'<hp:tbl id="{nid()}"', x, count=1)
    x = x.replace('&lt; 조 건 &gt;', f'&lt; {" ".join(label)} &gt;')
    # 본문 칸 = colAddr 1, rowAddr 2
    if not label:
        x = x.replace('&lt;  &gt;', '')
    end = x.index('<hp:cellAddr colAddr="1" rowAddr="2"/>')
    sl = x.rindex('<hp:subList ', 0, end)
    a = x.index('>', sl) + 1
    b = x.rindex('</hp:subList>', 0, end)
    inner_open = re.search(r'<hp:p [^>]*>', x[a:b]).group(0)
    inner = ''.join(f'{inner_open}<hp:run charPrIDRef="58">{body(s)}<hp:t/></hp:run></hp:p>' for s in lines)
    return x[:a] + inner + x[b:]

IMAGES = []
def picture(path, width_mm=53):
    from PIL import Image
    pw, ph = Image.open(path).size
    n = 3 + len(IMAGES)
    IMAGES.append((f'image{n}', path))
    ow, oh = pw * 75, ph * 75
    w = int(width_mm * 283.465)
    h = int(w * ph / pw)
    x = PICTURE
    x = re.sub(r'<hp:pic id="\d+"', f'<hp:pic id="{nid()}"', x, count=1)
    x = re.sub(r'instid="\d+"', f'instid="{nid()}"', x, count=1)
    x = re.sub(r'binaryItemIDRef="\w+"', f'binaryItemIDRef="image{n}"', x)
    x = re.sub(r'<hp:orgSz width="\d+" height="\d+"/>', f'<hp:orgSz width="{ow}" height="{oh}"/>', x)
    x = re.sub(r'<hp:curSz width="\d+" height="\d+"/>', f'<hp:curSz width="{w}" height="{h}"/>', x)
    x = re.sub(r'centerX="\d+" centerY="\d+"', f'centerX="{w // 2}" centerY="{h // 2}"', x)
    x = re.sub(r'<hc:scaMatrix e1="[\d.]+" e2="0" e3="0" e4="0" e5="[\d.]+"',
               f'<hc:scaMatrix e1="{w / ow:.6f}" e2="0" e3="0" e4="0" e5="{h / oh:.6f}"', x)
    x = re.sub(r'<hp:imgRect>.*?</hp:imgRect>', f'<hp:imgRect><hc:pt0 x="0" y="0"/><hc:pt1 x="{ow}" y="0"/>'
               f'<hc:pt2 x="{ow}" y="{oh}"/><hc:pt3 x="0" y="{oh}"/></hp:imgRect>', x, flags=re.S)
    x = re.sub(r'<hp:imgClip [^>]*/>', f'<hp:imgClip left="0" right="{ow}" top="0" bottom="{oh}"/>', x)
    x = re.sub(r'<hp:imgDim [^>]*/>', f'<hp:imgDim dimwidth="{ow}" dimheight="{oh}"/>', x)
    x = re.sub(r'<hp:sz width="\d+" widthRelTo="ABSOLUTE" height="\d+"', f'<hp:sz width="{w}" widthRelTo="ABSOLUTE" height="{h}"', x)
    return x

# ---------- 문항 ----------
def stem_part(p):
    if isinstance(p, str):
        return para(p)
    k = p[0]
    if k == 'd':                     # 가운데 줄 수식
        return para(f'${p[1]}$', P_CENTER)
    if k == 'box':                   # ('box', '조건' | '보기' | '', [줄...])
        return box(p[1], p[2])
    if k == 'img':                   # ('img', 경로, 가로mm)
        return picture(p[1], p[2] if len(p) > 2 else 53)
    raise ValueError(p)

MARKS = '①②③④⑤'
def choices(cs):
    if all(c.startswith('$') and c.endswith('$') and len(c) < 14 for c in cs):
        l1 = '\t\t\t'.join(f'{MARKS[i]} {cs[i]}' for i in range(3))
        l2 = '\t\t\t'.join(f'{MARKS[i]} {cs[i]}' for i in range(3, 5))
        return para(l1) + para(l2)
    return ''.join(para(f'{MARKS[i]} {c}') for i, c in enumerate(cs))

def item_xml(it):
    stem = list(it['stem'])
    first = stem.pop(0) if stem and isinstance(stem[0], str) else ''
    en = endnote(it['answer'], it.get('sol', []), it.get('note'))
    out = f'{P_OPEN}<hp:run charPrIDRef="58">{en}{body(first)}<hp:t/></hp:run></hp:p>'
    out += ''.join(stem_part(p) for p in stem)
    if 'choices' in it:
        out += BLANK + choices(it['choices'])
    for sub in it.get('subs', []):
        text, gap = (sub, SUB_GAP) if isinstance(sub, str) else sub
        out += para(text) + blanks(gap)
    return out

def build_section1(C):
    body_xml, col = [], 1
    first_written = False
    in_col = 0                       # 현재 단에 놓인 문항 수
    notice_done = False
    for it in C.ITEMS:
        hard = it.get('hard', 'subs' in it)
        if in_col and (hard or in_col >= 2):
            body_xml.append(COLBREAK); col += 1; in_col = 0
        if 'title' in it:            # 서답형
            if not notice_done:
                body_xml.append(NOTICE); notice_done = True
            body_xml.append(HEADING.replace('[서답형 1]', esc(it['title'])))
        body_xml.append(item_xml(it))
        in_col += 1
        if hard:
            in_col = 2
        elif in_col == 1:
            body_xml.append(blanks(EASY_GAP))
    # 문제 끝 → 짝수 쪽에서 끝내고 다음 홀수 쪽 왼쪽 단(빠른정답 자리)으로
    pages = (col + 1) // 2
    end_page = pages if pages % 2 == 0 else pages + 1
    target_col = 2 * (end_page + 1) - 1
    body_xml.append(COLBREAK * (target_col - col))
    first = FIRST.replace('제한시간은 50분입니다.', f'제한시간은 {getattr(C, "MINUTES", 50)}분입니다.')
    return SEC_HEAD + first + ''.join(body_xml) + '</hs:sec>', pages, end_page + 1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('content'); ap.add_argument('out'); ap.add_argument('--eqsz')
    a = ap.parse_args()
    if a.eqsz:
        EQSZ.update(json.load(open(a.eqsz, encoding='utf8')))
    spec = importlib.util.spec_from_file_location('content', a.content)
    C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
    base = os.path.dirname(os.path.abspath(a.content))
    for it in C.ITEMS:
        it['stem'] = [(p[0], os.path.join(base, p[1]), *p[2:]) if isinstance(p, tuple) and p[0] == 'img' and not os.path.isabs(p[1]) else p
                      for p in it['stem']]
    s1, pages, ans_page = build_section1(C)
    s0 = S0.replace('{TITLE}', esc(C.TITLE)).replace('{RANGE}', esc(C.RANGE)).replace('{TOTAL}', str(C.TOTAL))
    with zipfile.ZipFile(TEMPLATE) as zin, zipfile.ZipFile(a.out, 'w') as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == 'Contents/section0.xml':
                data = s0.encode('utf8')
            elif info.filename == 'Contents/section1.xml':
                data = s1.encode('utf8')
            elif info.filename == 'BinData/image3.png':
                continue
            elif info.filename == 'Contents/content.hpf':
                h = data.decode('utf8')
                h = re.sub(r'<opf:item id="image3"[^>]*/>', '', h)
                items = ''.join(f'<opf:item id="{iid}" href="BinData/{iid}.png" media-type="image/png" isEmbeded="1"/>' for iid, _ in IMAGES)
                h = h.replace('<opf:item id="section1"', items + '<opf:item id="section1"')
                h = re.sub(r'<opf:title>.*?</opf:title>', f'<opf:title>{esc(C.TITLE)}</opf:title>', h)
                data = h.encode('utf8')
            elif info.filename == 'Preview/PrvText.txt':
                data = C.TITLE.encode('utf8')
            zout.writestr(info, data, compress_type=info.compress_type)
        for iid, path in IMAGES:
            zout.write(path, f'BinData/{iid}.png', compress_type=zipfile.ZIP_DEFLATED)
    print(f'{a.out}: 문항 {len(C.ITEMS)}개, 문제 {pages}쪽 → 빠른정답 시작 {ans_page}쪽')

if __name__ == '__main__':
    main()
