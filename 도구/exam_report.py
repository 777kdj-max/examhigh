# 시험지 분석 데이터(JSON) → 2쪽 분석 보고서 PDF
#   python 도구/exam_report.py 시험지분석/<이름>.json  [출력.pdf]
# 문항별 배점·단원·행동영역·난이도만 적으면 표의 문항수·배점·비중·해당 문항은 자동 계산한다.
# 1쪽: 1~4절, 2쪽: 5~9절. 넘치면 글자 크기를 줄여 항상 2쪽에 맞춘다.
import json, os, re, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Table,
                                TableStyle, Spacer, PageBreak, KeepTogether, Flowable)

SP = os.path.dirname(os.path.abspath(__file__))

# ---------- 글꼴: 윈도우 맑은 고딕 우선, 없으면 동봉한 나눔고딕 ----------
def _font(cands):
    for p in cands:
        if os.path.exists(p):
            return p
    raise SystemExit('한글 글꼴을 찾을 수 없습니다: ' + ', '.join(cands))

WIN = os.path.join(os.environ.get('WINDIR', 'C:/Windows'), 'Fonts')
pdfmetrics.registerFont(TTFont('KR', _font([os.path.join(WIN, 'malgun.ttf'), os.path.join(SP, 'fonts', 'NanumGothic.ttf')])))
pdfmetrics.registerFont(TTFont('KRB', _font([os.path.join(WIN, 'malgunbd.ttf'), os.path.join(SP, 'fonts', 'NanumGothicBold.ttf')])))
pdfmetrics.registerFontFamily('KR', normal='KR', bold='KRB', italic='KR', boldItalic='KRB')

NAVY = colors.HexColor('#3E4C6E')
LINE = colors.HexColor('#D5DAE3')
SOFT = colors.HexColor('#F6F7FA')
LABEL = colors.HexColor('#EEF0F4')
GREY = colors.HexColor('#8A8F99')
GREEN, RED = colors.HexColor('#2E7D4F'), colors.HexColor('#C0392B')
TAG = {'기본': ('#E3F4E8', '#2E7D4F'), '표준': ('#E3EEFA', '#2463A6'),
       '변별': ('#FCEFD9', '#B7791F'), '킬러': ('#FBE3E3', '#C0392B')}
GRADE_BG = ['#2E7D4F', '#24578F', '#B7791F', '#C2611F']


# ---------- 계산 ----------
def label(no, suffix='번'):
    return no if no.startswith('단') else no + suffix

def numfmt(x):
    return ('%.1f' % x).rstrip('0').rstrip('.') if x != int(x) else str(int(x))

def compress(nos):
    """['1','2','3','5','단1'] → '1~3, 5번, 단1'"""
    mc = [int(n) for n in nos if not n.startswith('단')]
    sa = [n for n in nos if n.startswith('단')]
    parts, i = [], 0
    while i < len(mc):
        j = i
        while j + 1 < len(mc) and mc[j + 1] == mc[j] + 1:
            j += 1
        parts.append(f'{mc[i]}~{mc[j]}' if j - i >= 2 else ', '.join(map(str, mc[i:j + 1])))
        i = j + 1
    out = ', '.join(parts)
    if out:
        out += '번'
    if sa:
        out = ', '.join(([out] if out else []) + sa)
    return out

def analyze(d):
    items = d['items']
    by = {it['no']: it for it in items}
    total = sum(it['pts'] for it in items)
    mc = [it for it in items if not it['no'].startswith('단')]
    sa = [it for it in items if it['no'].startswith('단')]
    def group(key, names):
        rows = []
        for k in names:
            g = [it for it in items if it[key] == k]
            rows.append((k, len(g), sum(it['pts'] for it in g), [it['no'] for it in g]))
        missing = [it['no'] for it in items if it[key] not in names]
        if missing:
            raise SystemExit(f'{key} 값이 정의되지 않은 문항: {missing}')
        return rows
    units = []
    for i, u in enumerate(d['units']):
        g = [it for it in items if it['unit'] == i]
        units.append((u, len(g), sum(it['pts'] for it in g)))
    gb = d.get('grade_basis')
    basis = None
    if gb:
        basis = sum(by[n]['pts'] for n in gb['full']) + sum(by[n]['pts'] * f for n, f in gb.get('partial', {}).items())
    return dict(total=total, mc=mc, sa=sa, by=by, units=units,
                areas=group('area', list(d['areas'])), levels=group('level', list(d['levels'])),
                killer_pts=sum(by[k['no']]['pts'] for k in d['killers']), basis=basis)


# ---------- 문단 ----------
class S:
    def __init__(self, k):
        self.k = k
        P = lambda name, size, font='KR', **kw: ParagraphStyle(name, fontName=font, fontSize=size * k,
                                                               leading=size * k * 1.45, **kw)
        self.body = P('b', 8.6)
        self.cell = P('c', 8.2)
        self.cellc = P('cc', 8.2, alignment=TA_CENTER)
        self.head = P('h', 8.2, 'KRB', alignment=TA_CENTER, textColor=colors.white)
        self.lab = P('l', 8.6, 'KRB')
        self.sec = P('s', 11, 'KRB', textColor=NAVY)
        self.note = P('n', 6.8, textColor=GREY)
        self.notec = P('nc', 6.8, textColor=GREY, alignment=TA_CENTER)
        self.box_t = P('bt', 9, 'KRB', textColor=NAVY)

def md(t):
    t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)


class SecHead(Flowable):
    """번호 원 + 절 제목"""
    def __init__(self, n, title, s, w):
        super().__init__()
        self.n, self.title, self.s, self.w = n, title, s, w
        self.h = 8.5 * mm * s.k
    def wrap(self, *a):
        return self.w, self.h
    def draw(self):
        c, k = self.canv, self.s.k
        r = 3.3 * mm * k
        c.setFillColor(NAVY)
        c.roundRect(4 * mm, self.h / 2 - r, 2 * r, 2 * r, 1.4 * mm, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont('KRB', 9 * k)
        c.drawCentredString(4 * mm + r, self.h / 2 - 3.1 * k, str(self.n))
        c.setFillColor(NAVY)
        c.setFont('KRB', 11 * k)
        c.drawString(4 * mm + 2 * r + 4 * mm, self.h / 2 - 3.8 * k, self.title)


def tag_cell(t, s):
    bg, fg = TAG.get(t, ('#EEEEEE', '#555555'))
    st = ParagraphStyle('t', parent=s.cellc, fontName='KRB', textColor=colors.HexColor(fg))
    tb = Table([[Paragraph(t, st)]], colWidths=[18 * mm])
    tb.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(bg)),
                            ('ROUNDEDCORNERS', [3, 3, 3, 3]),
                            ('TOPPADDING', (0, 0), (-1, -1), 1), ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5)]))
    return tb

def grid(rows, widths, s, align=None, extra=()):
    """첫 행이 머리글인 남색 표"""
    data = [[Paragraph(h, s.head) for h in rows[0]]]
    for r in rows[1:]:
        line = []
        for i, v in enumerate(r):
            if isinstance(v, Flowable):
                line.append(v)
            else:
                st = s.cellc if (align and align[i] == 'c') else s.cell
                line.append(Paragraph(md(str(v)), st))
        data.append(line)
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [('BACKGROUND', (0, 0), (-1, 0), NAVY),
          ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
          ('LINEBELOW', (0, 1), (-1, -1), 0.4, LINE),
          ('TOPPADDING', (0, 0), (-1, -1), 2.6 * s.k), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.6 * s.k),
          ('ROUNDEDCORNERS', [4, 4, 0, 0])]
    for i in range(2, len(data), 2):
        st.append(('BACKGROUND', (0, i), (-1, i), SOFT))
    t.setStyle(TableStyle(st + list(extra)))
    return t

def card(flows, w, s, bg=colors.white, pad=6):
    t = Table([[flows]], colWidths=[w])
    t.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.6, LINE), ('BACKGROUND', (0, 0), (-1, -1), bg),
                           ('ROUNDEDCORNERS', [6, 6, 6, 6]),
                           ('LEFTPADDING', (0, 0), (-1, -1), pad), ('RIGHTPADDING', (0, 0), (-1, -1), pad),
                           ('TOPPADDING', (0, 0), (-1, -1), pad * s.k), ('BOTTOMPADDING', (0, 0), (-1, -1), pad * s.k)]))
    return t


# ---------- 본문 ----------
def story(d, a, s, W):
    h, k = d['header'], s.k
    out = []
    sp = lambda x: Spacer(1, x * mm * k)

    # 제목 띠
    tt = Table([[Paragraph('내신 시험지 분석 보고서', ParagraphStyle('tt', fontName='KRB', fontSize=14 * k,
                leading=18 * k, alignment=TA_CENTER, textColor=colors.white))]], colWidths=[W])
    tt.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), NAVY), ('ROUNDEDCORNERS', [6, 6, 6, 6]),
                            ('TOPPADDING', (0, 0), (-1, -1), 5 * k), ('BOTTOMPADDING', (0, 0), (-1, -1), 6 * k)]))
    out += [tt, sp(2.5)]

    # 기본 정보
    mcp = sum(i['pts'] for i in a['mc']); sap = sum(i['pts'] for i in a['sa'])
    comp = f"선택형 {len(a['mc'])}({numfmt(mcp)}점) + 단답형 {len(a['sa'])}({numfmt(sap)}점)"
    L, V = s.lab, s.body
    big = ParagraphStyle('bg', parent=V, fontName='KRB', textColor=NAVY, fontSize=9.6 * k)
    info = Table([[Paragraph('학교', L), Paragraph(md(h['school']), ParagraphStyle('x', parent=V, fontName='KRB', fontSize=9.6 * k)),
                   Paragraph('시행 일자', L), Paragraph(md(h['date']), V)],
                  [Paragraph('시험', L), Paragraph(md(h['exam']), V), Paragraph('평가 범위', L), Paragraph(md(h['scope']), V)],
                  [Paragraph('문항 구성', L), Paragraph(comp, V), Paragraph('예상 난이도', L), Paragraph(md(h['difficulty']), big)]],
                 colWidths=[0.15 * W, 0.35 * W, 0.15 * W, 0.35 * W])
    info.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.6, LINE), ('INNERGRID', (0, 0), (-1, -1), 0.4, LINE),
                              ('BACKGROUND', (0, 0), (0, -1), LABEL), ('BACKGROUND', (2, 0), (2, -1), LABEL),
                              ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('ROUNDEDCORNERS', [5, 5, 5, 5]),
                              ('TOPPADDING', (0, 0), (-1, -1), 4 * k), ('BOTTOMPADDING', (0, 0), (-1, -1), 4 * k),
                              ('LEFTPADDING', (0, 0), (-1, -1), 7)]))
    out += [info, sp(1.5)]

    # 1. 출제 개요
    out.append(SecHead(1, '출제 개요 요약', s, W))
    sap_list = '·'.join(numfmt(i['pts']) for i in a['sa'])
    stats = [(f"{len(d['items'])}문항", '총 출제 문항', f"선택형 {len(a['mc'])} · 단답형 {len(a['sa'])}"),
             (f'{numfmt(sap)}점', '단답형 배점', f'{sap_list}점 · 답만 기재'),
             (f"{len(d['killers'])}문항", '킬러·변별 문항', f"합계 {numfmt(a['killer_pts'])}점 · 1·2등급 변별 구간")]
    cw = (W - 6 * mm) / 3
    cells = []
    for big_t, lab, sub in stats:
        cells.append(card([Paragraph(big_t, ParagraphStyle('sb', fontName='KRB', fontSize=17 * k, leading=22 * k,
                                                           alignment=TA_CENTER, textColor=NAVY)),
                           sp(1.5), Paragraph(lab, ParagraphStyle('sl', parent=s.cellc, textColor=colors.HexColor('#555B66'))),
                           Paragraph(sub, s.notec)], cw - 2, s))
    row = Table([cells], colWidths=[cw + 3 * mm] * 3)
    row.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0)]))
    out += [row, sp(1.5)]

    # 2. 단원별
    out.append(SecHead(2, '단원별 출제 비중 분석', s, W))
    rows = [['평가 단원', '문항수', '배점', '비중', '출제 문항 및 특징']]
    for (u, n, p), feat in zip(a['units'], d['unit_features']):
        rows.append([u, n, f'{p:.1f}', f"{p / a['total'] * 100:.1f}%", feat])
    out.append(grid(rows, [0.18 * W, 0.08 * W, 0.08 * W, 0.08 * W, 0.58 * W], s, 'lccc l'.replace(' ', '')))
    top = max(a['units'], key=lambda x: x[2])
    hl = Paragraph(f"<font color='#2E7D4F'><b>최다 배점: {top[0].split('. ', 1)[-1]} ({numfmt(top[2])}점)</b></font>"
                   f"  |  <font color='#C0392B'><b>{md(d['unit_highlight'])}</b></font>", s.cell)
    out += [sp(1), card([hl], W, s, colors.HexColor('#EEF6F1'), 4), sp(1.5)]

    # 3. 행동영역
    out.append(SecHead(3, '행동영역별 문항 구성', s, W))
    rows = [['행동영역', '문항', '배점', '해당 문항', '성격']]
    for name, n, p, nos in a['areas']:
        ar = d['areas'][name]
        rows.append([name, n, numfmt(p) + '점', f"{compress(nos)} — {ar['desc']}", tag_cell(ar['tag'], s)])
    out += [grid(rows, [0.17 * W, 0.09 * W, 0.1 * W, 0.5 * W, 0.14 * W], s, 'lcclc'), sp(1.5)]

    # 4. 킬러
    out.append(SecHead(4, '킬러·변별 문항 상세 분석', s, W))
    rows = [['문항', '단원', '핵심 아이디어', '배점', '예상<br/>정답률']]
    for kk in d['killers']:
        it = a['by'][kk['no']]
        rows.append([label(kk['no']), d['units'][it['unit']].split('. ', 1)[-1], kk['idea'], numfmt(it['pts']), kk['rate']])
    out += [grid(rows, [0.08 * W, 0.15 * W, 0.57 * W, 0.08 * W, 0.12 * W], s, 'cclcc'),
            Paragraph(md(d.get('killer_note', '')), s.notec)]

    out.append(PageBreak())

    # 5. 등급컷
    out.append(SecHead(5, '내신 5등급제 예상 등급컷', s, W))
    gw = (W - 12 * mm) / 4
    gcells = []
    for i, g in enumerate(d['grade_cuts']):
        c = Table([[Paragraph(g['grade'], ParagraphStyle('g', fontName='KRB', fontSize=19 * k, leading=23 * k,
                                                        alignment=TA_CENTER, textColor=colors.white))],
                   [Paragraph(f"{g['range']}<br/>{g['pct']}", ParagraphStyle('gs', fontName='KR', fontSize=7 * k,
                                                                        leading=9.5 * k, alignment=TA_CENTER,
                                                                        textColor=colors.white))]],
                  colWidths=[gw - 14 * mm])
        c.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(GRADE_BG[i % 4])),
                               ('ROUNDEDCORNERS', [5, 5, 5, 5]), ('TOPPADDING', (0, 0), (-1, -1), 2 * k),
                               ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5 * k)]))
        gcells.append(c)
    gr = Table([gcells], colWidths=[gw + 3 * mm] * 4)
    gtxt = d['grade_text'].replace('{basis}', str(round(a['basis'])) if a['basis'] is not None else '?')
    out += [card([gr, sp(2), Paragraph(md(gtxt), s.body),
                  Paragraph('* 학교 실제 성적 분포가 아닌 시험지 구성만으로 추정한 참고용 등급컷이며, 실제 학교 등급컷과 다를 수 있습니다.', s.note)],
                 W, s), sp(1.5)]

    # 6. 필수 문형
    out.append(SecHead(6, '반드시 대비해야 할 필수 문형', s, W))
    rows = [['#', '필수 문형', '관련 문항', '대비 포인트']]
    for i, m in enumerate(d['must_types'], 1):
        rows.append([i, f"**{m['name']}**", m['items'], m['point']])
    out += [grid(rows, [0.05 * W, 0.3 * W, 0.18 * W, 0.47 * W], s, 'clcl'), sp(1.5)]

    # 7. 난이도
    out.append(SecHead(7, '난이도별 문항 분포', s, W))
    rows = [['난이도', '문항', '배점', '해당 문항', '성격']]
    for name, n, p, nos in a['levels']:
        lv = d['levels'][name]
        rows.append([name, n, numfmt(p) + '점', f"{compress(nos)} — {lv['desc']}", tag_cell(lv['tag'], s)])
    out += [grid(rows, [0.17 * W, 0.09 * W, 0.1 * W, 0.5 * W, 0.14 * W], s, 'lcclc'), sp(1.5)]

    # 8. 총평·로드맵
    def fill(t):  # {pts:1-6} → 1~6번 배점 합
        def rep(m):
            lo, hi = map(int, m.group(1).split('-'))
            return numfmt(sum(a['by'][str(n)]['pts'] for n in range(lo, hi + 1)))
        return re.sub(r'\{pts:([\d-]+)\}', rep, t)
    out.append(SecHead(8, '아드폰테스 종합 총평 및 대비 로드맵', s, W))
    out += [card([Paragraph('■ 출제 경향 총평', s.box_t), sp(1), Paragraph(md(d['summary']), s.body)], W, s), sp(1.2)]
    out += [card([Paragraph('■ 등급대별 대비 로드맵', s.box_t), sp(1)] +
                 [Paragraph(f'<b>{md(x)}</b> {md(fill(y))}', s.body) for x, y in d['roadmap']], W, s), sp(1.5)]

    # 9. 다음 시험
    out.append(SecHead(9, '이 시험지로 본 다음 시험 대비 전략', s, W))
    out += [card([Paragraph('■ 다음 시험 예상 및 대비 방향', s.box_t), sp(1)] +
                 [Paragraph(f'<b>{md(x)}</b> {md(fill(y))}', s.body) for x, y in d['next_exam']], W, s)]
    return out


def on_page(d):
    def draw(c, doc):
        w, hgt = A4
        c.saveState()
        c.setFillColor(NAVY)
        if doc.page == 1:
            c.setFont('KRB', 20); c.drawString(15 * mm, hgt - 22 * mm, 'AD FONTES')
            c.setFont('KRB', 7.5); c.drawString(15 * mm, hgt - 26.5 * mm, '아드폰테스 수학전문학원')
            c.setFont('KR', 7.5); c.setFillColor(GREY); c.drawString(47 * mm, hgt - 26.5 * mm, 'Academic Assessment')
            c.setFillColor(NAVY); c.setFont('KR', 8)
            c.drawRightString(w - 15 * mm, hgt - 17 * mm, d['header']['short_title'])
            c.drawRightString(w - 15 * mm, hgt - 21.5 * mm, '시험지 분석 보고서')
        else:
            c.setStrokeColor(LINE); c.line(15 * mm, 16 * mm, w - 15 * mm, 16 * mm)
            c.setFont('KR', 6.8); c.setFillColor(GREY)
            c.drawCentredString(w / 2, 12 * mm, 'AD FONTES 수학전문학원 | 본 분석표는 아드폰테스 시험지 분석 시스템으로 생성되었습니다.')
        c.restoreState()
    return draw


def build(d, out_pdf):
    a = analyze(d)
    if abs(a['total'] - 100) > 1e-6:
        print(f"주의: 배점 합계가 100이 아닙니다 ({numfmt(a['total'])}점)")
    w, h = A4
    W = w - 30 * mm
    for k in [1.0, 0.97, 0.94, 0.91, 0.88, 0.85, 0.82, 0.79, 0.76]:
        pages = {}
        doc = BaseDocTemplate(out_pdf, pagesize=A4, title=d['header']['short_title'], author='AD FONTES',
                              leftMargin=15 * mm, rightMargin=15 * mm, topMargin=31 * mm, bottomMargin=12 * mm)
        f1 = Frame(15 * mm, 12 * mm, W, h - 43 * mm, id='p1', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        f2 = Frame(15 * mm, 19 * mm, W, h - 31 * mm, id='p2', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        doc.addPageTemplates([PageTemplate('first', [f1], onPage=on_page(d), autoNextPageTemplate='rest'),
                              PageTemplate('rest', [f2], onPage=on_page(d))])
        doc.afterPage = lambda: pages.__setitem__('n', doc.page)
        doc.build(story(d, a, S(k), W))
        if pages['n'] == 2:
            return k, a
    raise SystemExit('글자를 줄여도 2쪽에 들어가지 않습니다. 문구를 줄여 주세요.')


if __name__ == '__main__':
    src = sys.argv[1]
    out_pdf = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + '_분석보고서.pdf'
    d = json.load(open(src, encoding='utf8'))
    k, a = build(d, out_pdf)
    print(f'{out_pdf}  (2쪽, 글자 배율 {k:.2f}, 총 {numfmt(a["total"])}점)')
    for u, n, p in a['units']:
        print(f'  {u}: {n}문항 {numfmt(p)}점')
    if a['basis'] is not None:
        print(f"  1컷 합산: {numfmt(round(a['basis'], 1))}점")
