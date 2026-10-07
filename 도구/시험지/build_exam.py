# 내신 시험지(A4 2단) hwpx 조립
#   python3 build_exam.py <내용모듈> <출력.hwpx>
#   예) python3 build_exam.py exam_2026_2_mid_calc1 ../../결과물/미적분1_2026_2학기_중간.hwpx
# 문제는 짝수 쪽에서 끝나고, 빠른정답은 다음 홀수 쪽 왼쪽 단에서 시작하도록 단 나누기로 자리를 맞춘다.
# (빠른정답 자체는 한글에서 빠른정답컨트롤v2 매크로(Alt+Shift+2)로 만든다)
import html, importlib, json, os, re, shutil, struct, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, 'base')
C = importlib.import_module(sys.argv[1] if len(sys.argv) > 1 else 'exam_2026_2_mid_calc1')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'out.hwpx')

# ---------- 쪽 설정 (A4) ----------
PAGE_W, PAGE_H = 59528, 84186
MARGIN = dict(left=3969, right=3969, top=6804, bottom=5103, header=2835, footer=1984, gutter=0)
BODY_W = PAGE_W - MARGIN['left'] - MARGIN['right']      # 51590
COL_GAP = 1701
COL_W = (BODY_W - COL_GAP) // 2                          # 24944
HANG = 1400                                              # 문항 번호 내어쓰기

EQSZ = json.load(open(os.path.join(HERE, 'eqsz.json'), encoding='utf8'))

_id = [1000000000]
def nid():
    _id[0] += 1
    return str(_id[0])

def esc(t):
    return html.escape(t, quote=False)

# ---------- header.xml 스타일 추가 ----------
def char_pr(i, height, font, bold=False):
    f = ' '.join(f'{k}="{font}"' for k in ('hangul', 'latin', 'hanja', 'japanese', 'other', 'symbol', 'user'))
    z = lambda v: ' '.join(f'{k}="{v}"' for k in ('hangul', 'latin', 'hanja', 'japanese', 'other', 'symbol', 'user'))
    return (f'<hh:charPr id="{i}" height="{height}" textColor="#000000" shadeColor="none" useFontSpace="0" useKerning="0" '
            f'symMark="NONE" borderFillIDRef="2"><hh:fontRef {f}/><hh:ratio {z(100)}/><hh:spacing {z(0)}/>'
            f'<hh:relSz {z(100)}/><hh:offset {z(0)}/>' + ('<hh:bold/>' if bold else '') +
            '<hh:underline type="NONE" shape="SOLID" color="#000000"/><hh:strikeout shape="NONE" color="#000000"/>'
            '<hh:outline type="NONE"/><hh:shadow type="NONE" color="#C0C0C0" offsetX="10" offsetY="10"/></hh:charPr>')

def para_pr(i, align='JUSTIFY', left=0, intent=0, line=160, prev=0, nxt=0, tab=0):
    def m(k):
        return (f'<hh:margin><hc:intent value="{intent * k}" unit="HWPUNIT"/><hc:left value="{left * k}" unit="HWPUNIT"/>'
                f'<hc:right value="0" unit="HWPUNIT"/><hc:prev value="{prev * k}" unit="HWPUNIT"/>'
                f'<hc:next value="{nxt * k}" unit="HWPUNIT"/></hh:margin>'
                f'<hh:lineSpacing type="PERCENT" value="{line}" unit="HWPUNIT"/>')
    return (f'<hh:paraPr id="{i}" tabPrIDRef="{tab}" condense="0" fontLineHeight="0" snapToGrid="1" suppressLineNumbers="0" checked="0">'
            f'<hh:align horizontal="{align}" vertical="BASELINE"/><hh:heading type="NONE" idRef="0" level="0"/>'
            '<hh:breakSetting breakLatinWord="KEEP_WORD" breakNonLatinWord="KEEP_WORD" widowOrphan="0" keepWithNext="0" '
            'keepLines="0" pageBreakBefore="0" lineWrap="BREAK"/><hh:autoSpacing eAsianEng="0" eAsianNum="0"/>'
            '<hp:switch><hp:case hp:required-namespace="http://www.hancom.co.kr/hwpml/2016/HwpUnitChar">' + m(1) +
            '</hp:case><hp:default>' + m(2) + '</hp:default></hp:switch>'
            '<hh:border borderFillIDRef="2" offsetLeft="0" offsetRight="0" offsetTop="0" offsetBottom="0" connect="0" ignoreMargin="0"/></hh:paraPr>')

def border_fill(i, line):
    b = lambda s: f'<hh:{s}Border type="{"SOLID" if line else "NONE"}" width="{line or "0.1 mm"}" color="#000000"/>'
    return (f'<hh:borderFill id="{i}" threeD="0" shadow="0" centerLine="NONE" breakCellSeparateLine="0">'
            '<hh:slash type="NONE" Crooked="0" isCounter="0"/><hh:backSlash type="NONE" Crooked="0" isCounter="0"/>'
            + b('left') + b('right') + b('top') + b('bottom') +
            '<hh:diagonal type="SOLID" width="0.1 mm" color="#000000"/></hh:borderFill>')

def tab_pr(i, step, n):
    items = ''.join(f'<hp:switch><hp:case hp:required-namespace="http://www.hancom.co.kr/hwpml/2016/HwpUnitChar">'
                    f'<hh:tabItem pos="{step * k}" type="LEFT" leader="NONE" unit="HWPUNIT"/></hp:case><hp:default>'
                    f'<hh:tabItem pos="{step * k * 2}" type="LEFT" leader="NONE"/></hp:default></hp:switch>' for k in range(1, n + 1))
    return f'<hh:tabPr id="{i}" autoTabLeft="0" autoTabRight="0">{items}</hh:tabPr>'

BATANG, DOTUM = 1, 0
CP = dict(body='0', ins='7', big='8', title='9', label='10', head='11', small='12', smallb='13', num='14')
NEW_CHAR = [char_pr(7, 1000, BATANG, True), char_pr(8, 1800, DOTUM, True), char_pr(9, 1300, DOTUM, True),
            char_pr(10, 1000, DOTUM), char_pr(11, 1100, DOTUM, True), char_pr(12, 900, DOTUM),
            char_pr(13, 900, DOTUM, True), char_pr(14, 1000, BATANG, True)]
PP = dict(q='20', p='21', c='22', center='23', plain='24', right='25', left='26', box='27')
CHOICE_TAB = (COL_W - HANG) // 5
NEW_PARA = [para_pr(20, left=HANG, intent=-HANG), para_pr(21, left=HANG), para_pr(22, left=HANG, tab=3, prev=200),
            para_pr(23, 'CENTER', line=130), para_pr(24, line=150), para_pr(25, 'RIGHT', line=130),
            para_pr(26, 'LEFT', line=130), para_pr(27, 'LEFT', line=170)]
BF = dict(none='2', line='3', thick='4')
NEW_BF = [border_fill(3, '0.12 mm'), border_fill(4, '0.4 mm')]

def add(h, group, items):
    m = re.search(rf'<hh:{group} itemCnt="(\d+)">', h)
    n = int(m.group(1)) + len(items)
    h = h[:m.start()] + f'<hh:{group} itemCnt="{n}">' + h[m.end():]
    end = h.index(f'</hh:{group}>')
    return h[:end] + ''.join(items) + h[end:]

def build_header():
    h = open(os.path.join(BASE, 'Contents/header.xml'), encoding='utf8').read()
    h = add(h, 'borderFills', NEW_BF)
    h = add(h, 'charProperties', NEW_CHAR)
    h = add(h, 'tabProperties', [tab_pr(3, CHOICE_TAB, 4)])
    h = add(h, 'paraProperties', NEW_PARA)
    return h

# ---------- 수식 ----------
def eq_size(script):
    if script in EQSZ:
        w, h, bl, _ = EQSZ[script]
        return w, h, bl
    t = re.sub(r'\b(LEFT|RIGHT|lim|rarrow|over|TIMES|cases|lbrace|rbrace|le|ge|INF)\b', 'x', script)
    t = re.sub(r'[`~{}\s^_&#]', '', t)
    w = max(1, len(t)) * 560
    h, bl = 1125, 85
    if 'over' in script or 'lim' in script:
        h, bl = 2600, 64
    if 'cases' in script:
        h, bl = 2600 + 1100 * script.count('#'), 55
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

# ---------- 문단 ----------
def text_body(s):
    """$..$ 수식, \t 탭"""
    out = ''
    for part in re.split(r'(\$.*?\$)', s):
        if not part:
            continue
        if part.startswith('$'):
            out += equation(part[1:-1])
        else:
            out += '<hp:t>' + esc(part).replace('\t', '<hp:tab width="0" leader="0" type="1"/>') + '</hp:t>'
    return out

def runs(s, cp):
    out = ''
    m = re.match(r'^(\d+\.)\s', s)          # 문항 번호는 굵게
    if m and cp == CP['body']:
        out += f'<hp:run charPrIDRef="{CP["num"]}"><hp:t>{m.group(1)} </hp:t></hp:run>'
        s = s[m.end():]
    for seg in re.split(r'(\*\*.*?\*\*)', s):
        if not seg:
            continue
        c = cp
        if seg.startswith('**'):
            c, seg = CP['ins'], seg[2:-2]
        out += f'<hp:run charPrIDRef="{c}">{text_body(seg)}</hp:run>'
    return out

def P(s, pp, cp=CP['body'], col_break=False, pre=''):
    body = runs(s, cp) if s else f'<hp:run charPrIDRef="{cp}"><hp:t/></hp:run>'
    return (f'<hp:p id="{nid()}" paraPrIDRef="{pp}" styleIDRef="0" pageBreak="0" columnBreak="{1 if col_break else 0}" '
            f'merged="0">{pre}{body}</hp:p>')

def obj_para(obj, pp=PP['plain'], col_break=False):
    return (f'<hp:p id="{nid()}" paraPrIDRef="{pp}" styleIDRef="0" pageBreak="0" columnBreak="{1 if col_break else 0}" '
            f'merged="0"><hp:run charPrIDRef="0">{obj}<hp:t/></hp:run></hp:p>')

# ---------- 표 ----------
def tc(col, row, w, h, paras, bf=BF['line'], cs=1, rs=1, margin=(283, 283, 141, 141), valign='CENTER'):
    l, r, t, b = margin
    return (f'<hp:tc name="" header="0" hasMargin="1" protect="0" editable="0" dirty="0" borderFillIDRef="{bf}">'
            f'<hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="{valign}" linkListIDRef="0" '
            f'linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">{paras}</hp:subList>'
            f'<hp:cellAddr colAddr="{col}" rowAddr="{row}"/><hp:cellSpan colSpan="{cs}" rowSpan="{rs}"/>'
            f'<hp:cellSz width="{w}" height="{h}"/><hp:cellMargin left="{l}" right="{r}" top="{t}" bottom="{b}"/></hp:tc>')

def tbl(rows, cols, w, h, trs, bf=BF['line'], out_margin=(0, 0, 0, 0)):
    l, r, t, b = out_margin
    return (f'<hp:tbl id="{nid()}" zOrder="0" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" '
            f'lock="0" dropcapstyle="None" pageBreak="CELL" repeatHeader="0" rowCnt="{rows}" colCnt="{cols}" '
            f'cellSpacing="0" borderFillIDRef="{bf}" noAdjust="0">'
            f'<hp:sz width="{w}" widthRelTo="ABSOLUTE" height="{h}" heightRelTo="ABSOLUTE" protect="0"/>'
            f'<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" '
            f'vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
            f'<hp:outMargin left="{l}" right="{r}" top="{t}" bottom="{b}"/><hp:inMargin left="0" right="0" top="0" bottom="0"/>'
            + ''.join(f'<hp:tr>{x}</hp:tr>' for x in trs) + '</hp:tbl>')

def box(lines, width):
    paras = ''.join(P(s, PP['box']) for s in lines)
    return tbl(1, 1, width, 3000, [tc(0, 0, width, 3000, paras, margin=(567, 567, 283, 283))], out_margin=(0, 0, 283, 283))

def title_table():
    T = C.TITLE
    ws = [9600, 2300, 5600, 2300, 15890, 2300]
    ws.append(BODY_W - sum(ws))
    cp = lambda s, c, pp=PP['center']: P(s, pp, c)
    r0 = tc(0, 0, BODY_W, 2000, cp(T['top'], CP['title']), cs=7)
    cells = [cp(T['grade'], CP['title']), cp('코드', CP['label']), cp(T['code'], CP['big']), cp('과목', CP['label']),
             cp(T['subject'], CP['big']), cp('배점', CP['label']), ''.join(P(s, PP['left'], CP['label']) for s in T['score'])]
    r1 = ''.join(tc(i, 1, ws[i], 3400, c) for i, c in enumerate(cells))
    return tbl(2, 7, BODY_W, 5400, [r0, r1], bf=BF['thick'], out_margin=(0, 0, 0, 283))

def strip_table():
    ws = [26000, 10000]
    ws.append(BODY_W - sum(ws))
    cells = ''.join(tc(i, 0, ws[i], 1500, P(s, PP['center'], CP['label'])) for i, s in enumerate(C.HEADER))
    return tbl(1, 3, BODY_W, 1500, [cells], bf=BF['thick'])

def footer_table():
    ws = [17000, 17590, 17000]
    page = ('<hp:run charPrIDRef="12"><hp:t>( ' + str(C.TOTAL_PAGES) + ' )쪽 중 ( </hp:t>'
            '<hp:ctrl><hp:autoNum num="1" numType="PAGE"><hp:autoNumFormat type="DIGIT" userChar="" prefixChar="" '
            'suffixChar="" supscript="0"/></hp:autoNum></hp:ctrl><hp:t> )쪽</hp:t></hp:run>')
    cells = (tc(0, 0, ws[0], 1000, P(C.SCHOOL, PP['left'], CP['smallb']), bf=BF['none']) +
             tc(1, 0, ws[1], 1000, f'<hp:p id="{nid()}" paraPrIDRef="{PP["center"]}" styleIDRef="0" pageBreak="0" '
                                    f'columnBreak="0" merged="0">{page}</hp:p>', bf=BF['none']) +
             tc(2, 0, ws[2], 1000, P(C.EXAM, PP['right'], CP['smallb']), bf=BF['none']))
    return tbl(1, 3, BODY_W, 1000, [cells], bf=BF['none'])

# ---------- 그림 ----------
IMAGES = []
def picture(path, width_mm):
    from PIL import Image
    px_w, px_h = Image.open(path).size
    n = len(IMAGES) + 1
    IMAGES.append((f'image{n}', path))
    ow, oh = px_w * 75, px_h * 75
    w = int(width_mm * 283.465)
    h = int(w * px_h / px_w)
    sx, sy = w / ow, h / oh
    return (f'<hp:pic id="{nid()}" zOrder="1" numberingType="PICTURE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" '
            f'lock="0" dropcapstyle="None" href="" groupLevel="0" instid="{nid()}" reverse="0">'
            f'<hp:offset x="0" y="0"/><hp:orgSz width="{ow}" height="{oh}"/><hp:curSz width="{w}" height="{h}"/>'
            f'<hp:flip horizontal="0" vertical="0"/><hp:rotationInfo angle="0" centerX="{w // 2}" centerY="{h // 2}" rotateimage="1"/>'
            f'<hp:renderingInfo><hc:transMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>'
            f'<hc:scaMatrix e1="{sx:.6f}" e2="0" e3="0" e4="0" e5="{sy:.6f}" e6="0"/>'
            f'<hc:rotMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/></hp:renderingInfo>'
            f'<hc:img binaryItemIDRef="image{n}" bright="0" contrast="0" effect="REAL_PIC" alpha="0"/>'
            f'<hp:imgRect><hc:pt0 x="0" y="0"/><hc:pt1 x="{ow}" y="0"/><hc:pt2 x="{ow}" y="{oh}"/><hc:pt3 x="0" y="{oh}"/></hp:imgRect>'
            f'<hp:imgClip left="0" right="{ow}" top="0" bottom="{oh}"/><hp:inMargin left="0" right="0" top="0" bottom="0"/>'
            f'<hp:imgDim dimwidth="{ow}" dimheight="{oh}"/><hp:effects/>'
            f'<hp:sz width="{w}" widthRelTo="ABSOLUTE" height="{h}" heightRelTo="ABSOLUTE" protect="0"/>'
            f'<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" '
            f'vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
            f'<hp:outMargin left="0" right="0" top="0" bottom="0"/><hp:shapeComment>그림입니다.</hp:shapeComment></hp:pic>')

# ---------- 블록 ----------
def block(b, col_break, pre=''):
    k = b[0]
    if k == 'q':
        return P(b[1], PP['q'], col_break=col_break, pre=pre)
    if k == 'p':
        return P(b[1], PP['p'], col_break=col_break, pre=pre)
    if k == 'c':
        marks = '①②③④⑤'
        return P('\t'.join(f'{marks[i]} {x}' for i, x in enumerate(b[1])), PP['c'], col_break=col_break, pre=pre)
    if k == 'ins':
        return P(b[1], PP['plain'], CP['ins'], col_break=col_break, pre=pre)
    if k == 'h':
        return P(b[1], PP['plain'], CP['head'], col_break=col_break, pre=pre)
    if k == 'end':
        return P(b[1], PP['center'], CP['ins'], col_break=col_break, pre=pre)
    if k == 'gap':
        return ''.join(P('', PP['plain'], col_break=(col_break and i == 0), pre=(pre if i == 0 else ''))
                       for i in range(b[1]))
    if k == 'box':
        return obj_para(box(b[1], COL_W - HANG), PP['p'], col_break)
    if k == 'img':
        return obj_para(picture(os.path.join(HERE, b[1]) if not os.path.isabs(b[1]) else b[1], b[2]), PP['center'], col_break)
    raise ValueError(k)

TWO_COL = ('<hp:ctrl><hp:colPr id="" type="NEWSPAPER" layout="LEFT" colCount="2" sameSz="1" sameGap="%d">'
           '<hp:colLine type="SOLID" width="0.12 mm" color="#000000"/></hp:colPr></hp:ctrl>' % COL_GAP)
HIDE = ('<hp:ctrl><hp:pageHiding hideHeader="1" hideFooter="1" hideMasterPage="0" hideBorder="0" hideFill="0" '
        'hidePageNum="0"/></hp:ctrl>')

def build_section():
    sec = open(os.path.join(BASE, 'Contents/section0.xml'), encoding='utf8').read()
    sec_open = sec[:sec.index('<hp:p ')]
    secpr = re.search(r'<hp:secPr .*?</hp:secPr>', sec, re.S).group(0)
    secpr = re.sub(r'<hp:pagePr [^>]*>', f'<hp:pagePr landscape="WIDELY" width="{PAGE_W}" height="{PAGE_H}" gutterType="LEFT_ONLY">', secpr)
    secpr = re.sub(r'<hp:margin [^>]*/>', '<hp:margin ' + ' '.join(f'{k}="{v}"' for k, v in MARGIN.items()) + '/>', secpr)
    secpr = secpr.replace('hideFirstHeader="0"', 'hideFirstHeader="1"')
    hdr = (f'<hp:ctrl><hp:header id="1" applyPageType="BOTH"><hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" '
           f'vertAlign="TOP" linkListIDRef="0" linkListNextIDRef="0" textWidth="{BODY_W}" textHeight="{MARGIN["top"] - MARGIN["header"]}" '
           f'hasTextRef="0" hasNumRef="0">{obj_para(strip_table())}</hp:subList></hp:header></hp:ctrl>')
    ftr = (f'<hp:ctrl><hp:footer id="2" applyPageType="BOTH"><hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" '
           f'vertAlign="BOTTOM" linkListIDRef="0" linkListNextIDRef="0" textWidth="{BODY_W}" textHeight="{MARGIN["bottom"] - MARGIN["footer"]}" '
           f'hasTextRef="0" hasNumRef="0">'
           f'{P("이 시험문제의 저작권은 " + C.SCHOOL + "에 있습니다. 전재와 복제시 저작권법에 의거 처벌될 수 있습니다.", PP["center"], CP["smallb"])}'
           f'{obj_para(footer_table())}</hp:subList></hp:footer></hp:ctrl>')
    p0 = (f'<hp:p id="{nid()}" paraPrIDRef="{PP["plain"]}" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">'
          f'<hp:run charPrIDRef="0">{secpr}<hp:ctrl><hp:colPr id="" type="NEWSPAPER" layout="LEFT" colCount="1" sameSz="1" sameGap="0"/></hp:ctrl>'
          f'{hdr}{ftr}{title_table()}<hp:t/></hp:run></hp:p>')
    body = []
    first = True
    for page in C.PAGES:
        for col in page:
            items = col or [('gap', 1)]
            for j, b in enumerate(items):
                cb = (j == 0 and not first)
                pre = f'<hp:run charPrIDRef="0">{TWO_COL}</hp:run>' if first else ''
                if first and b[0] in ('box', 'img'):
                    body.append(P('', PP['plain'], pre=pre))
                    pre = ''
                body.append(block(b, cb, pre))
                first = False
    # 문제 끝 쪽 → 짝수 쪽까지 비우고, 다음 홀수 쪽 왼쪽 단에 커서(빠른정답 자리)
    last = len(C.PAGES)
    target = last + 1 if last % 2 == 0 else last + 2
    for pg in range(last + 1, target + 1):
        for c in range(2 if pg < target else 1):
            body.append(P('', PP['plain'], col_break=True, pre=HIDE_RUN if (c == 0 and pg < target) else ''))
    return sec_open + p0 + ''.join(body) + '</hs:sec>', last, target

HIDE_RUN = f'<hp:run charPrIDRef="0">{HIDE}</hp:run>'

# ---------- 패키징 ----------
def main():
    header = build_header()
    section, last, target = build_section()
    tmp = OUT + '.d'
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    shutil.copytree(BASE, tmp)
    open(os.path.join(tmp, 'Contents/header.xml'), 'w', encoding='utf8').write(header)
    open(os.path.join(tmp, 'Contents/section0.xml'), 'w', encoding='utf8').write(section)
    os.makedirs(os.path.join(tmp, 'BinData'), exist_ok=True)
    items = ''
    for iid, path in IMAGES:
        shutil.copy(path, os.path.join(tmp, 'BinData', iid + '.png'))
        items += f'<opf:item id="{iid}" href="BinData/{iid}.png" media-type="image/png" isEmbeded="1"/>'
    hpf = os.path.join(tmp, 'Contents/content.hpf')
    c = open(hpf, encoding='utf8').read()
    c = c.replace('<opf:item id="header"', items + '<opf:item id="header"')
    c = c.replace('<opf:title/>', f'<opf:title>{esc(C.EXAM)} {esc(C.TITLE["subject"])}</opf:title>')
    open(hpf, 'w', encoding='utf8').write(c)
    txt = re.sub(r'<[^>]+>', ' ', re.sub(r'<hp:(equation|secPr|header|footer)\b.*?</hp:\1>', '', section, flags=re.S))
    open(os.path.join(tmp, 'Preview/PrvText.txt'), 'w', encoding='utf8').write(re.sub(r'\s+', ' ', html.unescape(txt))[:1000])
    if os.path.exists(OUT):
        os.remove(OUT)
    with zipfile.ZipFile(OUT, 'w') as z:
        z.write(os.path.join(tmp, 'mimetype'), 'mimetype', compress_type=zipfile.ZIP_STORED)
        for root, _, files in os.walk(tmp):
            for f in sorted(files):
                full = os.path.join(root, f)
                arc = os.path.relpath(full, tmp).replace(os.sep, '/')
                if arc != 'mimetype':
                    z.write(full, arc, compress_type=zipfile.ZIP_DEFLATED)
    shutil.rmtree(tmp)
    print(f'{OUT}: 문제 {last}쪽 → 빠른정답 시작 {target}쪽 (그림 {len(IMAGES)}개)')

if __name__ == '__main__':
    main()
