# 2026학년도 2학기 중간고사 2학년 미적분Ⅰ (과목코드 02) — 원본: 스캔 PDF 7쪽
# 표기: $..$ 한글 수식, **..** 굵게
# 블록: ('q', 문단) 문항 첫 문단(내어쓰기) / ('p', 문단) 이어지는 문단 / ('c', [보기 5개])
#       ('box', [문단...]) 조건 상자 / ('img', 파일, 가로mm) / ('gap', n) 빈 줄 n개
#       ('ins', 문단) 굵은 안내문 / ('h', 문단) 서답형 제목

SCHOOL = '여의도고등학교'
EXAM = '2026학년도 2학기 중간고사'
TOTAL_PAGES = 7

TITLE = {
    'top': '2026학년도  2학기  중간고사    10월  7일 ( 수요일 )  실시',
    'grade': '학년 :  2 학년',
    'code': '02',
    'subject': '미적분Ⅰ',
    'score': ['선택형 : 15문항 69점', '단답형 :   2문항 11점', '서술형 :   3문항 20점'],
}
HEADER = ['제 ( 2 )학년 2학기 중간고사 (미적분Ⅰ)과목', '과목코드 (02)', '2026년 10월 7일(수) 실시']

F = 'f LEFT (x RIGHT )'
G = 'g LEFT (x RIGHT )'

def nums(*xs):
    return ('c', [f'${x}$' for x in xs])

# 쪽마다 [왼쪽 단, 오른쪽 단]
PAGES = [
    # ---- 1쪽 ----
    [[
        ('ins', '※ 선택형 1번~15번 : 문제를 잘 읽고 답을 OMR카드에 컴퓨터용 사인펜을 이용하여 정확히 표시하시오.'),
        ('gap', 1),
        ('q', '1. 함수 $f LEFT (x RIGHT )  =  2x`^{ 2 } + 1$에서 $x$의 값이 $2$에서 $4$까지 변할 때의 평균변화율은? [3.9점]'),
        nums(12, 13, 14, 15, 16),
        ('gap', 5),
        ('q', '2. $lim_{ x~rarrow~1 }``{ x`^{ 2 } + 2 x - 3 } over { x - 1 }$의 값은? [4점]'),
        nums(1, 2, 3, 4, 5),
        ('gap', 5),
        ('q', '3. 실수 전체의 집합에서 미분가능한 함수 $f LEFT (x RIGHT )$에 대하여 '
              '$g LEFT (x RIGHT )  =  f LEFT (x RIGHT ) TIMES f LEFT (x RIGHT )$라 하자. '
              '$f LEFT (0 RIGHT )f`{ ′ } LEFT (0 RIGHT )  =  2$일 때, $g`{ ′ } LEFT (0 RIGHT )$의 값은? [4.1점]'),
        nums(1, 2, 3, 4, 5),
        ('gap', 4),
        ('q', '4. 함수 $y  =  f LEFT (x RIGHT )$의 그래프가 그림과 같을 때, 닫힌구간 $LEFT [ -3,```3 RIGHT ]$에서 '
              '극한값이 존재하지 않는 $x$의 값의 개수를 $a$, 불연속인 $x$의 값의 개수를 $b$라 하자. '
              '$a TIMES  b$의 값은? [4.2점]'),
        ('img', 'q4.png', 62),
        nums(9, 10, 12, 14, 15),
    ], [
        ('q', '5. 실수 전체 집합에서 연속인 두 함수 $f LEFT (x RIGHT ),```g LEFT (x RIGHT )$가'),
        ('p', '$lim_{ x~rarrow~3 }`` LEFT (f LEFT (x RIGHT ) - g LEFT (x RIGHT ) RIGHT )  =  2,```` lim_{ x~rarrow~3 }``f LEFT (x RIGHT )g LEFT (x RIGHT )  = 24$'),
        ('p', '를 만족시킬 때, $LEFT |f LEFT (3 RIGHT ) + g LEFT (3 RIGHT ) RIGHT |$의 값은? [4.3점]'),
        nums(6, 7, 8, 9, 10),
        ('gap', 10),
        ('q', '6. 다항함수 $f LEFT (x RIGHT )  =  x`^{ 3 } - 2 ax`^{ 2 } + 3 a x$가 역함수를 갖도록 하는 모든 정수 $a$의 값의 곱은? [4.4점]'),
        nums('- 2', '- 1', 0, 1, 2),
        ('gap', 10),
        ('q', '7. 다항함수 $f LEFT (x RIGHT )  =  2x`^{ 3 } - 9x`^{ 2 } + a x + 4$는 $x  =  1$에서 극대이고, '
              '$x  =  b$에서 극소이다. 함수 $f LEFT (x RIGHT )$의 모든 극값의 합은? (단, $a,```b$는 상수이다.) [4.5점]'),
        nums(15, 17, 19, 21, 23),
    ]],
    # ---- 2쪽 ----
    [[
        ('q', '8. $x$에 대한 방정식 $x`^{ 3 } - 2x`^{ 2 } + 6 x + 8  =  a$는 $a$의 값에 관계없이 오직 하나의 실근을 갖는다. '
              '이 방정식의 실근이 열린구간 $LEFT (1,```2 RIGHT )$에 존재하도록 하는 모든 자연수 $a$의 값의 합은? [4.6점]'),
        nums(76, 80, 88, 93, 99),
        ('gap', 14),
        ('q', '9. 상수 $a$에 대하여 다항함수 $f LEFT (x RIGHT )$가 다음 조건을 만족시킨다.'),
        ('box', [
            '(가) 모든 실수 $x$에 대하여',
            '      $f LEFT (x + a RIGHT ) - f LEFT (a RIGHT )  =  x`^{ 2 } +  LEFT (2 a + 1 RIGHT )x$이다.',
            '(나) 곡선 $y  =  f LEFT (x RIGHT )$ 위의 점 $LEFT (a,```f LEFT (a RIGHT ) RIGHT )$에서의 접선이 직선',
            '      $y  =  { 1 } over { 3 }x$에 수직이다.',
        ]),
        ('p', '$f LEFT (2 RIGHT ) + f LEFT ( -2 RIGHT )  =  10$일 때, $f LEFT (a RIGHT )$의 값은? [4.7점]'),
        nums(1, 2, 3, 4, 5),
    ], [
        ('q', '10. 다항식 $f LEFT (x RIGHT )$를 $LEFT (x - 1 RIGHT )^{ 2 } LEFT (x - 2 RIGHT )$로 나누었을 때의 나머지를 '
              '$R LEFT (x RIGHT )$라 하면'),
        ('p', '        $lim_{ x~rarrow~2 }``{ R LEFT (x RIGHT ) - R LEFT (1 RIGHT ) } over { x - 2 }  =  R LEFT (2 RIGHT )  = 1$'),
        ('p', '이다. $f LEFT (x RIGHT )$를 $LEFT (x - 1 RIGHT ) LEFT (x - 2 RIGHT )$로 나눈 나머지를 $L LEFT (x RIGHT )$라 할 때, '
              '$L LEFT (1 RIGHT )$의 값은? [4.8점]'),
        nums(1, 2, 3, 4, 5),
        ('gap', 12),
        ('q', '11. 집합 $A  =   lbrace a∣a 는~정수이고,~LEFT |a RIGHT | le 4 이다.  rbrace$의 서로 다른 두 원소 '
              '$p,```q$에 대하여 두 함수 $f LEFT (x RIGHT ),```g LEFT (x RIGHT )$를'),
        ('p', '$f LEFT (x RIGHT )  =   cases{``-x + q``&`` LEFT (x le 1 RIGHT )``#``2x + p``&`` LEFT (x > 1 RIGHT )``},```'
              'g LEFT (x RIGHT )  =   cases{``x`^{ 2 } + 2x``&`` LEFT (x le p RIGHT )``#``-x + q``&`` LEFT (x > p RIGHT )``}$'),
        ('p', '라 하자. 모든 실수 $k$에 대하여 $lim_{ x~rarrow~k }`` LEFT (f LEFT (x RIGHT ) + g LEFT (x RIGHT ) RIGHT )$가 '
              '존재하도록 하는 $p,```q$의 모든 순서쌍 $LEFT (p,```q RIGHT )$의 개수는? [4.9점]'),
        nums(8, 9, 10, 11, 12),
    ]],
    # ---- 3쪽 ----
    [[
        ('q', '12. 함수 $f LEFT (x RIGHT )  =   cases{``ax`^{ 2 } - 4x``&`` LEFT (x le 2 RIGHT )``#``3x + 2``&`` LEFT (x > 2 RIGHT )``}$에 대하여 함수 '
              '$f LEFT (x RIGHT )f LEFT (x - 3 RIGHT )$이 $x  =  b$에서만 불연속일 때, $a - b$의 값은? '
              '(단, $a,```b$는 상수이다.) [5점]'),
        nums('- 9', '- 6', 3, 6, 9),
    ], [
        ('q', '13. 점 $LEFT ( -2,```1 RIGHT )$에서 곡선 $y  =  x`^{ 3 } + kx`^{ 2 } + 1$에 그은 접선의 개수가 $1$이 되도록 하는 '
              '정수 $k$의 개수는? [5.1점]'),
        nums(11, 12, 14, 15, 16),
    ]],
    # ---- 4쪽 ----
    [[
        ('q', '14. 두 자연수 $a$, $b$에 대하여 함수 $f LEFT (x RIGHT )  =  x`^{ 2 } - a x + b$이다. '
              '$f LEFT (0 RIGHT )f LEFT (1 RIGHT )f LEFT (2 RIGHT ) < 0$이고 $f LEFT (0 RIGHT )f LEFT (3 RIGHT )f LEFT (4 RIGHT ) < 0$일 때, '
              '$f LEFT (0 RIGHT )$의 값은? [5.2점]'),
        nums(1, 2, 3, 4, 5),
    ], [
        ('q', '15. $f LEFT (0 RIGHT )  =  3$인 이차함수 $f LEFT (x RIGHT )$에 대하여 함수 $g LEFT (x RIGHT )$를'),
        ('p', '        $g LEFT (x RIGHT )  =   cases{``x``&`` LEFT (x <  - 1 RIGHT )``#``f LEFT (x RIGHT )``&`` LEFT ( -1 le x le 1 RIGHT )``#``-x``&`` LEFT (x > 1 RIGHT )``}$'),
        ('p', '이라 하자. 함수'),
        ('p', '        $h LEFT (x RIGHT )  =  lim_{ t~rarrow~0 - }``g LEFT (x + t RIGHT ) TIMES  lim_{ t~rarrow~2 + }``g LEFT (x + t RIGHT )$'),
        ('p', '가 실수 전체의 집합에서 연속일 때, $- 3 < α < 1$인 실수 $α$에 대하여 함수 $h LEFT (x RIGHT )$가 '
              '$x  =  α$에서 극값을 갖는 모든 $α$의 값의 합은? [5.3점]'),
        nums('- 3', '- 2', '- 1', 0, 1),
    ]],
    # ---- 5쪽 ----
    [[
        ('ins', '※ 서답형 1번~5번 : 문제를 잘 읽고, OMR 서술·논술형 답안지에 다음 지시 사항대로 정확히 쓰시오.'),
        ('ins', '  ▶ 1번~2번 단답형 : "정답"만 쓰시오.'),
        ('ins', '  ▶ 3번~5번 서술형 : 풀이과정과 정답을 모두 쓰시오.'),
        ('p', '※ 답란의 여백이 부족하거나 수정할 답안의 내용이 많을 경우 빈 답란의 문항 번호를 수정하여 사용할 수 있음.'),
        ('p', '※ 답안지의 문항 번호와 답안 내용이 일치하지 않을 경우 점수를 부여하지 않을 수 있음.'),
        ('gap', 1),
        ('h', '<서답형1_단답형>'),
        ('p', '실수 $t$에 대하여 닫힌구간 $LEFT [t - 1,```t + 1 RIGHT ]$에서 함수'),
        ('p', '        $f LEFT (x RIGHT )  =   cases{``2``&`` LEFT (x < 0 RIGHT )``#``-x``&`` LEFT (0 le x < 1 RIGHT )``#``1``&`` LEFT (x ge 1 RIGHT )``}$'),
        ('p', '가 $x  =  a$에서 불연속인 $a$의 값의 개수를 $g LEFT (t RIGHT )$라 하자. '
              '최고차항의 계수가 $1$인 사차함수 $h LEFT (t RIGHT )$에 대하여 함수 $g LEFT (t RIGHT )h LEFT (t RIGHT )$가 '
              '실수 전체의 집합에서 연속일 때, $h LEFT (2 TIMES  g LEFT ({ 1 } over { 2 } RIGHT ) RIGHT )$의 값을 구하시오. [5점]'),
    ], [
        ('h', '<서답형2_단답형>'),
        ('p', '최고차항의 계수가 $1$인 이차함수 $f LEFT (x RIGHT )$와 상수 $k$에 대하여 함수'),
        ('p', '        $g LEFT (x RIGHT )  =   cases{``LEFT |f LEFT (x RIGHT ) RIGHT |``&`` LEFT (x < k RIGHT )``#``f LEFT (x RIGHT ) - 2f LEFT (k RIGHT )``&`` LEFT (x ge k RIGHT )``}$'),
        ('p', '가 다음 조건을 만족시킬 때, 함수 $h LEFT (x RIGHT )$의 극댓값을 구하시오. [6점]'),
        ('box', [
            '어떤 양의 실수 $α$에 대하여 함수',
            '  $h LEFT (x RIGHT )  =  g LEFT (x RIGHT ) -  LEFT (LEFT |x RIGHT | + LEFT |x - α RIGHT | RIGHT )$',
            '가 실수 전체의 집합에서 미분가능하다.',
        ]),
    ]],
    # ---- 6쪽 ----
    [[
        ('h', '<서답형3_서술형>'),
        ('p', '다음 조건을 만족시키는 모든 다항함수 $f LEFT (x RIGHT )$에 대하여 $f LEFT (3 RIGHT )$의 최댓값과 최솟값을 구하시오. [5점]'),
        ('box', [
            '(가) $f LEFT (0 RIGHT )  =  1$',
            '(나) 모든 실수 $x$에 대하여 $LEFT |f`{ ′ } LEFT (x RIGHT ) RIGHT | le 5$이다.',
        ]),
    ], [
        ('h', '<서답형4_서술형>'),
        ('p', '정수 계수를 가진 다항함수 $f LEFT (x RIGHT )$가 다음 조건을 만족시킬 때, $f LEFT (2 RIGHT )$의 최솟값을 구하시오. [7점]'),
        ('box', [
            '(가) $lim_{ x~rarrow~INF }``{  LEFT (x - 1 RIGHT )f LEFT (x RIGHT ) - x`^{ 4 } } over { x`^{ 3 } + 1 }  =  3$',
            '(나) 모든 실수 $k$에 대하여',
            '      $lim_{ x~rarrow~k }``{ f LEFT (3 x - 2 RIGHT ) } over { f LEFT (x RIGHT ) }$의 값이 존재한다.',
        ]),
    ]],
    # ---- 7쪽 ----
    [[
        ('h', '<서답형5_서술형>'),
        ('p', '함수'),
        ('p', '        $f LEFT (x RIGHT )  =   cases{``-2x``&`` LEFT (x < 0 RIGHT )``#``3x + 4``&`` LEFT (x ge 0 RIGHT )``}$'),
        ('p', '이 있다. 다음 조건을 만족시키는 모든 다항함수 $g LEFT (x RIGHT )$에 대하여 $g LEFT (4 RIGHT )$의 최솟값을 구하시오. [8점]'),
        ('box', [
            '(가) 어떤 양의 실수 $a$에 대하여 $lim_{ x~rarrow~INF }``{ g LEFT (x RIGHT ) } over { x`^{ 2 } }  =  a$이다.',
            '(나) 어떤 양의 실수 $α$에 대하여 함수 $LEFT |f LEFT (x RIGHT ) - g LEFT (x RIGHT ) RIGHT |$는',
            '      $x  =  α$에서만 미분가능하지 않다.',
        ]),
        ('gap', 24),
        ('end', '※ 문제 끝. 수고하셨습니다.'),
    ], [
    ]],
]
