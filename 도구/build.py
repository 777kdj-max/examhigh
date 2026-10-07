# 기본틀(개념 총 정리) 블록으로 원본(기하 개념정리) 1~3쪽을 재구성
import re, json, html, os, shutil, sys
import importlib
_c = importlib.import_module(os.environ.get('CONTENT', 'content'))
HEADER_TEXT, BLOCKS = _c.HEADER_TEXT, _c.BLOCKS

SP = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(SP, 'ref')
SRC = os.path.join(SP, 'src')
OUT = os.path.join(SP, 'out')

EQSZ = json.load(open(os.path.join(SP, 'src_eqsizes.json'), encoding='utf8'))
SCALE = 1100 / 1500

_id = [1900000000]
def nid():
    _id[0] += 1
    return str(_id[0])

def esc(t):
    return html.escape(t, quote=False)

# ---------- 수식 ----------
def eq_size(script):
    if script in EQSZ:
        w, h, bl = EQSZ[script]
        return int(w * SCALE), int(h * SCALE), bl
    # 추정치 (한글에서 열 때 다시 계산됨)
    t = re.sub(r'\b(bold|bar|root|sqrt|LEFT|RIGHT|over|rm|it|triangle|angle|cos|sin|theta|pi|because|parallel|BOT|SIM)\b', 'x', script)
    t = re.sub(r'[`~{}\s]', '', t)
    n = max(1, len(t))
    w = int(n * 560)
    h = 1125
    bl = 85
    if 'over' in script:
        h, bl = 2400, 65
    elif 'root' in script or 'sqrt' in script:
        h, bl = 1450, 80
    return w, h, bl

def equation(script):
    w, h, bl = eq_size(script)
    return (f'<hp:equation id="{nid()}" zOrder="0" numberingType="EQUATION" textWrap="TOP_AND_BOTTOM" '
            f'textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" version="Equation Version 60" baseLine="{bl}" '
            f'textColor="#000000" baseUnit="1100" lineMode="CHAR" font="HYhwpEQ">'
            f'<hp:sz width="{w}" widthRelTo="ABSOLUTE" height="{h}" heightRelTo="ABSOLUTE" protect="0"/>'
            f'<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" '
            f'vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
            f'<hp:outMargin left="56" right="56" top="0" bottom="0"/><hp:shapeComment>수식입니다.</hp:shapeComment>'
            f'<hp:script>{esc(script)}</hp:script></hp:equation>')

# ---------- 인라인 마크업 → run ----------
# $..$ 수식, **..** 굵게, 문단 첫머리 ➊~➍ 분홍 번호, [참고] 초록 참고 라벨
NUMS = '➊➋➌➍➎➏'
def runs(text, base, bold='34'):
    out = []
    m0 = re.match(r'^(\s*)\[참고\]\s*', text)
    if m0:
        if m0.group(1):
            out.append(f'<hp:run charPrIDRef="{base}"><hp:t>{m0.group(1)}</hp:t></hp:run>')
        out.append(f'<hp:run charPrIDRef="39"><hp:t>참고 </hp:t></hp:run>')
        out.append(f'<hp:run charPrIDRef="38"><hp:t>▶ </hp:t></hp:run>')
        text = text[m0.end():]
        base = '40'
    m = re.match(r'^(\s*)([' + NUMS + '])', text)
    if m:
        if m.group(1):
            out.append(f'<hp:run charPrIDRef="{base}"><hp:t>{m.group(1)}</hp:t></hp:run>')
        out.append(f'<hp:run charPrIDRef="29"><hp:t>{m.group(2)}</hp:t></hp:run>')
        text = text[m.end():]
    for seg in re.split(r'(\*\*.*?\*\*)', text):
        if not seg:
            continue
        cp = base
        if seg.startswith('**'):
            cp, seg = bold, seg[2:-2]
        parts = re.split(r'(\$.*?\$)', seg)
        body = ''
        for p in parts:
            if not p:
                continue
            if p.startswith('$'):
                body += equation(p[1:-1])
            else:
                body += f'<hp:t>{esc(p)}</hp:t>'
        out.append(f'<hp:run charPrIDRef="{cp}">{body}</hp:run>')
    return ''.join(out)

def para(text, base, ppr='3'):
    if text == '':
        return f'<hp:p id="0" paraPrIDRef="{ppr}" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="{base}"><hp:t/></hp:run></hp:p>'
    return f'<hp:p id="0" paraPrIDRef="{ppr}" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">{runs(text, base)}</hp:p>'

# ---------- 그림 (원본 hp:pic 복제) ----------
SRC_SEC = open(os.path.join(SRC, 'Contents/section0.xml'), encoding='utf8').read()
PICS = {}
for m in re.finditer(r'<hp:pic .*?</hp:pic>', SRC_SEC, re.S):
    iid = re.search(r'binaryItemIDRef="(\w+)"', m.group(0)).group(1)
    PICS.setdefault(iid, m.group(0))
IMG_MAP = {}  # 원본 id -> 새 id
def pic(src_id, maxw=None):
    new = 'image%d' % (100 + int(src_id[5:]))
    IMG_MAP[src_id] = new
    x = PICS[src_id]
    x = x.replace(f'binaryItemIDRef="{src_id}"', f'binaryItemIDRef="{new}"')
    x = re.sub(r'<hp:pic id="\d+"', f'<hp:pic id="{nid()}"', x, count=1)
    x = re.sub(r' xmlns:\w+="[^"]*"', '', x)
    # 본문 흐름을 따라가도록 글자처럼 취급
    x = re.sub(r'<hp:pos [^>]*/>', '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" '
               'holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" '
               'vertOffset="0" horzOffset="0"/>', x, count=1)
    x = x.replace('textWrap="SQUARE"', 'textWrap="TOP_AND_BOTTOM"', 1)
    w, h = map(int, re.search(r'<hp:sz width="(\d+)"[^>]*height="(\d+)"', x).groups())
    if maxw and w > maxw:
        f = maxw / w
        nw, nh = int(w * f), int(h * f)
        x = re.sub(r'<hp:sz width="\d+"([^>]*)height="\d+"', f'<hp:sz width="{nw}"\\1height="{nh}"', x, count=1)
        x = re.sub(r'<hp:curSz width="\d+" height="\d+"/>', f'<hp:curSz width="{nw}" height="{nh}"/>', x, count=1)
        x = re.sub(r'centerX="\d+" centerY="\d+"', f'centerX="{nw // 2}" centerY="{nh // 2}"', x, count=1)
        def sca(m):
            return f'<hc:scaMatrix e1="{float(m.group(1)) * f:.6f}" e2="0" e3="0" e4="0" e5="{float(m.group(2)) * f:.6f}" e6="0"/>'
        x = re.sub(r'<hc:scaMatrix e1="([\d.]+)" e2="0" e3="0" e4="0" e5="([\d.]+)" e6="0"/>', sca, x, count=1)
        w = nw
    return x, w

# ---------- 표 공통 ----------
def cell(col, row, cs, rs, w, h, bf, paras, margin=(0, 0, 0, 0), valign='CENTER'):
    l, r, t, b = margin
    return (f'<hp:tc name="" header="0" hasMargin="1" protect="0" editable="0" dirty="0" borderFillIDRef="{bf}">'
            f'<hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="{valign}" linkListIDRef="0" '
            f'linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">{paras}</hp:subList>'
            f'<hp:cellAddr colAddr="{col}" rowAddr="{row}"/><hp:cellSpan colSpan="{cs}" rowSpan="{rs}"/>'
            f'<hp:cellSz width="{w}" height="{h}"/><hp:cellMargin left="{l}" right="{r}" top="{t}" bottom="{b}"/></hp:tc>')

def table(rows, cols, w, h, bf, trs, out_margin=(0, 0, 0, 0)):
    l, r, t, b = out_margin
    return (f'<hp:tbl id="{nid()}" zOrder="0" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" '
            f'lock="0" dropcapstyle="None" pageBreak="CELL" repeatHeader="1" rowCnt="{rows}" colCnt="{cols}" '
            f'cellSpacing="0" borderFillIDRef="{bf}" noAdjust="0">'
            f'<hp:sz width="{w}" widthRelTo="ABSOLUTE" height="{h}" heightRelTo="ABSOLUTE" protect="0"/>'
            f'<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" '
            f'vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
            f'<hp:outMargin left="{l}" right="{r}" top="{t}" bottom="{b}"/><hp:inMargin left="0" right="0" top="0" bottom="0"/>'
            + ''.join(f'<hp:tr>{tr}</hp:tr>' for tr in trs) + '</hp:tbl>')

def wrap_obj(obj, cp='24', page_break=False):
    return f'<hp:p id="0" paraPrIDRef="3" styleIDRef="0" pageBreak="{1 if page_break else 0}" columnBreak="0" merged="0"><hp:run charPrIDRef="{cp}">{obj}<hp:t/></hp:run></hp:p>'

BOX_W = 60621
def content_paras(items, base, inner_w):
    """items: 문자열(문단) 또는 ('fig', 이미지id, [문단...]) — 그림|설명 2칸 무테 표"""
    out = []
    for it in items:
        if isinstance(it, tuple) and it[0] == 'img':
            px, _ = pic(it[1], inner_w)
            out.append(f'<hp:p id="0" paraPrIDRef="27" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="{base}">{px}<hp:t/></hp:run></hp:p>')
            continue
        if isinstance(it, tuple) and it[0] == 'imgs':
            n = len(it[1])
            cw = inner_w // n
            tcs = ''
            for k, (iid, texts) in enumerate(it[1]):
                px, _ = pic(iid, cw - 567)
                ps = f'<hp:p id="0" paraPrIDRef="27" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="{base}">{px}<hp:t/></hp:run></hp:p>'
                ps += ''.join(para(t, base) for t in texts)
                tcs += cell(k, 0, 1, 1, cw, 1000, '19', ps, (283, 283, 283, 283), 'TOP')
            out.append(wrap_obj(table(1, n, cw * n, 2000, '19', [tcs]), base))
            continue
        if isinstance(it, tuple) and it[0] == 'fig':
            _, iid, texts = it
            px, pw = pic(iid, int(inner_w * 0.42))
            lw = pw + 1134
            rw = inner_w - lw
            left = f'<hp:p id="0" paraPrIDRef="3" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="{base}">{px}<hp:t/></hp:run></hp:p>'
            right = ''.join(para(t, base) for t in texts)
            tr = (cell(0, 0, 1, 1, lw, 1000, '19', left, (0, 567, 283, 283)) +
                  cell(1, 0, 1, 1, rw, 1000, '19', right, (283, 0, 283, 283)))
            out.append(wrap_obj(table(1, 2, inner_w, 2000, '19', [tr]), base))
        else:
            out.append(para(it, base))
    return ''.join(out)

def concept_box(title, items, page_break=False):
    inner = BOX_W - 1417 * 2
    paras = (f'<hp:p id="0" paraPrIDRef="3" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">'
             f'<hp:run charPrIDRef="28"><hp:t>■ {esc(title)}</hp:t></hp:run></hp:p>' + content_paras(items, '33', inner))
    tr = cell(0, 0, 1, 1, BOX_W, 6000, '7', paras, (1417, 1417, 1417, 1417))
    return wrap_obj(table(1, 1, BOX_W, 8000, '6', [tr], (141, 0, 566, 566)), '31', page_break)

def ihae_box(label, items):
    inner = 59699 - 1417 * 2
    r0 = (cell(0, 0, 1, 2, 922, 5600, '8', '<hp:p id="0" paraPrIDRef="3" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="42"/></hp:p>') +
          cell(1, 0, 1, 1, 5104, 1666, '8', f'<hp:p id="0" paraPrIDRef="35" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="37"><hp:t>{esc(label)}</hp:t></hp:run></hp:p>') +
          cell(2, 0, 1, 1, 54595, 1666, '9', '<hp:p id="0" paraPrIDRef="3" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="27"><hp:t> </hp:t></hp:run></hp:p>'))
    r1 = cell(1, 1, 2, 1, 59699, 2442, '9', content_paras(items, '40', inner), (1417, 1417, 1417, 1417))
    return wrap_obj(table(2, 3, BOX_W, 8000, '6', [r0, r1], (0, 0, 566, 0)))

def unit_title(text, newpage=False, header=None):
    ctrl = ''
    if header:
        hc = re.sub(r'<hp:header id="\d+"', '<hp:header id="7"', HEADER_CTRL.replace(HEADER_TEXT_ESC, esc(header)), count=1)
        ctrl = f'<hp:run charPrIDRef="24">{hc}</hp:run>'
    return (f'<hp:p id="0" paraPrIDRef="3" styleIDRef="0" pageBreak="{1 if newpage else 0}" columnBreak="0" merged="0">'
            f'{ctrl}<hp:run charPrIDRef="32"><hp:t>{esc(text)}</hp:t></hp:run></hp:p>')

def note(items):
    # 상자 밖 참고 ▶ + 목록
    out = ['<hp:p id="0" paraPrIDRef="3" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">'
           '<hp:run charPrIDRef="35"><hp:t>참고 </hp:t></hp:run><hp:run charPrIDRef="36"><hp:t>▶</hp:t></hp:run></hp:p>']
    out += [para(t, '33') for t in items]
    return ''.join(out)

def blank():
    return para('', '24')

# ---------- 첫 문단 (secPr + 머리말/꼬리말 + 첫 제목) ----------
ref_sec = open(os.path.join(REF, 'Contents/section0.xml'), encoding='utf8').read()
head_end = ref_sec.index('<hp:p ')
sec_open = ref_sec[:head_end]
p0 = re.search(r'<hp:p [^>]*>.*?</hp:p>(?=<hp:p )', ref_sec, re.S).group(0)
p0 = re.sub(r'<hp:linesegarray>.*?</hp:linesegarray>', '', p0, flags=re.S)
p0 = p0.replace('1-2 [ 개념 총 정리 ] 1. 집합', esc(HEADER_TEXT))
HEADER_TEXT_ESC = esc(HEADER_TEXT)
HEADER_CTRL = re.search(r'<hp:ctrl><hp:header .*?</hp:header></hp:ctrl>', p0, re.S).group(0)

body = []
first_title_done = False
prev = None
for blk in BLOCKS:
    kind = blk[0]
    if kind == 'title':
        if not first_title_done:
            p0 = p0.replace('<hp:t>1. 집합과 원소</hp:t>', f'<hp:t>{esc(blk[1])}</hp:t>')
            first_title_done = True
        else:
            opt = blk[2] if len(blk) > 2 else {}
            body.append(unit_title(blk[1], opt.get('newpage', False), opt.get('header')))
    elif kind == 'box':
        # 이해 박스가 끝나면 다음 ■ 개념 박스는 새 쪽에서 시작
        body.append(concept_box(blk[1], blk[2], page_break=(prev == 'ihae')))
    elif kind == 'ihae':
        body.append(ihae_box(blk[1], blk[2]))
    elif kind == 'note':
        body.append(note(blk[1]))
    elif kind == 'blank':
        body.append(blank())
    elif kind == 'colbreak':
        body.append('<hp:p id="0" paraPrIDRef="3" styleIDRef="0" pageBreak="0" columnBreak="1" merged="0"><hp:run charPrIDRef="24"><hp:t/></hp:run></hp:p>')
    prev = kind

section = sec_open + p0 + ''.join(body) + '</hs:sec>'

# ---------- 패키지 디렉터리 구성 ----------
if os.path.exists(OUT):
    shutil.rmtree(OUT)
shutil.copytree(REF, OUT)
for i in range(1, 8):
    os.remove(os.path.join(OUT, f'Contents/section{i}.xml'))
for i in range(1, 7):
    os.remove(os.path.join(OUT, f'Contents/masterpage{i}.xml'))
for f in os.listdir(os.path.join(OUT, 'BinData')):
    if f != 'image1.jpg':
        os.remove(os.path.join(OUT, 'BinData', f))
for s_id, n_id in IMG_MAP.items():
    shutil.copy(os.path.join(SRC, 'BinData', s_id + '.bmp'), os.path.join(OUT, 'BinData', n_id + '.bmp'))
open(os.path.join(OUT, 'Contents/section0.xml'), 'w', encoding='utf8').write(section)

# header secCnt
hp = os.path.join(OUT, 'Contents/header.xml')
h = open(hp, encoding='utf8').read().replace('secCnt="8"', 'secCnt="1"', 1)
open(hp, 'w', encoding='utf8').write(h)

# content.hpf
cp = os.path.join(OUT, 'Contents/content.hpf')
c = open(cp, encoding='utf8').read()
c = re.sub(r'<opf:item id="image(?!1")\d+"[^>]*/>', '', c)
c = re.sub(r'<opf:item id="section[1-7]"[^>]*/>', '', c)
c = re.sub(r'<opf:item id="masterpage[1-6]"[^>]*/>', '', c)
c = re.sub(r'<opf:itemref idref="section[1-7]"[^>]*/>', '', c)
items = ''.join(f'<opf:item id="{n}" href="BinData/{n}.bmp" media-type="image/bmp" isEmbeded="1"/>' for n in IMG_MAP.values())
c = c.replace('<opf:item id="section0"', items + '<opf:item id="section0"')
c = re.sub(r'<opf:title>.*?</opf:title>', '<opf:title>기하 개념 총 정리</opf:title>', c)
open(cp, 'w', encoding='utf8').write(c)

# container.rdf
rp = os.path.join(OUT, 'META-INF/container.rdf')
r = open(rp, encoding='utf8').read()
r = re.sub(r'<rdf:Description rdf:about=""><ns0:hasPart [^>]*section[1-7]\.xml"/></rdf:Description>', '', r)
r = re.sub(r'<rdf:Description rdf:about="Contents/section[1-7]\.xml">.*?</rdf:Description>', '', r, flags=re.S)
open(rp, 'w', encoding='utf8').write(r)

# settings: 커서 위치 초기화
sp = os.path.join(OUT, 'settings.xml')
st = open(sp, encoding='utf8').read()
st = re.sub(r'<ha:CaretPosition [^>]*/>', '<ha:CaretPosition listIDRef="0" paraIDRef="0" pos="0"/>', st)
open(sp, 'w', encoding='utf8').write(st)

# 미리보기 텍스트
txt = re.sub(r'<[^>]+>', '', re.sub(r'<hp:equation .*?</hp:equation>', '', section, flags=re.S))
open(os.path.join(OUT, 'Preview/PrvText.txt'), 'w', encoding='utf8').write(html.unescape(txt)[:1000])
print('images', IMG_MAP)
