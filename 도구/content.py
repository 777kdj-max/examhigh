# 원본: 기하 개념정리(2018) 1~3쪽 — Ⅰ. 이차곡선 / 1. 포물선
HEADER_TEXT = '기하 [ 개념 총 정리 ] Ⅰ. 이차곡선'

BLOCKS = [
    ('title', '1. 포물선'),

    ('box', '포물선의 정의', [
        '    한 점(초점)과 한 직선(준선)에 이르는 거리가 같은 점들의 자취를 **포물선**이라 한다.',
        '    포물선 위의 점 $P$에서 준선에 내린 수선의 발을 $H$라 하면  $bold {bar PH`=` bar PF}$',
    ]),

    ('box', '포물선의 방정식', [
        '➊ **준선이 $y$축과 평행할 때**',
        '    $bold {y^2 `=` 4px}$   (초점 $F(p,``0)$, 준선 $x=-p$, 꼭짓점 $(0,``0)$)',
        '➋ **준선이 $x$축과 평행할 때**',
        '    $bold {x^2 `=` 4py}$   (초점 $F(0,``p)$, 준선 $y=-p$, 꼭짓점 $(0,``0)$)',
        '    [참고] $LEFT |  p RIGHT |$는 초점과 꼭짓점 사이의 거리이다.',
    ]),

    ('ihae', '이해', [
        '**포물선의 방정식 유도**',
        ('fig', 'image1', [
            '➊ 준선이 $y$축과 평행할 때',
            '$bar PH`=` bar PF$ 이므로 $root{(x-p)^2 + y^2}`=` LEFT |  x+p RIGHT |$',
            '↳ 양변 제곱하면 $x^2 -2px +p^2 +y^2 = x^2 +2px +p^2$',
            '↳ $bold {y^2 `=` 4px}$',
        ]),
        ('fig', 'image2', [
            '➋ 준선이 $x$축과 평행할 때',
            '$bar PH`=` bar PF$ 이므로 $root{(y-p)^2 + x^2}`=` LEFT |  y+p RIGHT |$',
            '↳ 양변 제곱하면 $y^2 -2py +p^2 +x^2 = y^2 +2py +p^2$',
            '↳ $bold {x^2 `=` 4py}$',
        ]),
    ]),

    ('box', '평행이동한 포물선', [
        '    포물선 $y^2 =4px$를 $x$축의 방향으로 $m$만큼, $y$축의 방향으로 $n$만큼 평행이동하면',
        ('fig', 'image3', [
            '➊ $(y-n)^2 =4p(x-m)$',
            '    ↳ 전개하면 $y^2 +Ay+Bx+C=0$ (일반형)',
            '➋ 초점 $(p+m,``n)$, 준선 $x=-p+m$, 꼭짓점 $(m,``n)$',
            '➌ 초점과 준선이 주어질 때',
            '    ↳ 준선과 초점의 중점이 꼭짓점이므로, 꼭짓점으로부터 얼마만큼 평행이동했는지 알아낼 수 있다.',
        ]),
    ]),

    ('box', '포물선과 직선의 위치 관계', [
        ('fig', 'image4', [
            '포물선 $y^2 =4px$와 직선 $y=mx+n$의 위치 관계는 두 식을 연립한 이차방정식 $(mx+n)^2 = 4p x$의 판별식 $D$로 확인한다.',
            '➊ $D>0$ : 서로 다른 두 점에서 만난다.',
            '➋ $D=0$ : 한 점에서 만난다. (접한다)',
            '➌ $D<0$ : 만나지 않는다.',
        ]),
    ]),

    ('box', '포물선의 접선의 방정식', [
        '➊ **기울기가 $m$일 때**',
        '    포물선 $y^2`=` 4px$의 접선 :  $y`=` mx `+ p overm$',
        '    포물선 $x^2 `=` 4py$의 접선 :  $y`=` mx `-m^2 p$',
        '➋ **접점이 $( x_1 , ``y_1 )$일 때**',
        '    포물선 $y^2`=` 4px$의 접선 :  $yy_1 =2p(x+x_1 )$',
        '    포물선 $x^2 `=` 4py$의 접선 :  $xx_1 =2p(y+y_1 )$',
    ]),

    ('ihae', '이해', [
        '**접선의 방정식 유도**',
        '➊ 직선 $y=mx+n$과 포물선 $y^2`=` 4px$가 접하므로 $(mx+n)^2 = 4p x$ → $m^2 x^2 +2(mn-2p)x +n^2 =0$',
        '    ↳ $D/4 `=` (mn-2p)^2 -m^2 n^2 =-4pmn +4p^2 =0$ → $n`=` p over m$',
        "➋ 접선의 기울기 : $2y y'=4p$ (음함수의 미분) → $y'= [ 2p over y ]_y=y_1`=` 2p over y _1$",
        '    ↳ 접점 $( x_1 , ``y_1 )$을 지나는 직선 : $y`=` 2p over y_1 (x-x_1 ) +y_1$ → $yy_1 = 2px -2px_1 +y_1`^2$',
        '    ↳ $y_1^2 =4px_1$이므로 $yy_1 = 2px -2px_1 +4px_1$ → $yy_1 =2p(x+x_1 )$',
    ]),

    ('box', '포물선의 성질 ① 초점을 지나는 직선', [
        "    포물선 $y^2 =4px$의 초점 $F$를 지나는 직선이 포물선과 두 점 $A$, $B$에서 만나고 $bar AF`=`a$, $bar BF`=`b$일 때",
        "    ($A'$, $B'$은 $A$, $B$에서 준선에 내린 수선의 발)",
        '➊ $1over p `=` 1 over a + 1over b$',
        "➋ $bar A'B'`=` 2 root ab$",
        '➌ 직선 $AB$가 $x$축의 양의 방향과 이루는 각을 $theta$, 기울기를 $m$이라 하면  $bar AB`=` 4p over {sin^2 theta }`=` 4p(1+{1overm^2} )$',
    ]),

    ('ihae', '이해', [
        '**증명**',
        ('fig', 'image5', [
            '✰ **$1over p `=` 1 over a + 1over b$**',
            "$bar AF `=`bar AA' `=`  a$, $bar BF`=`bar BB'`=`b$일 때, $triangle AFR$와 $triangle ABQ$는 닮음이므로",
            '↳ $bar FR `:` bar BQ`=` a: a+b`=` a-2p : a-b$',
            '↳ $a^2 +ab -2p(a+b)=a^2 -ab$ → $p`=` ab over a+b$',
            "✰ **$bar A'B'$의 길이**",
            "↳ 직각삼각형 $ABQ$에서 $bar A'B'`=` bar AQ`=` root {bar AB^2 -bar BQ^2}`=` root {(a+b)^2 -(a-b)^2}`=` 2rootab$",
        ]),
        ('fig', 'image6', [
            '✰ **직선의 기울기로 길이 구하기**',
            '↳ $a-2p over a`=` cos theta$ → $a`=`2p over {1-costheta}$, $b`=` 2p over {1+costheta}$',
            '↳ $bar AB`=` a+b = 2p( 1over {1-costheta}+`1over {1+costheta} )`=` 4p over {sin^2 theta }$',
            '↳ $bar AB`=` 4p(1+{1overm^2} )$',
        ]),
    ]),

    ('ihae', '이해', [
        '**초점을 지나는 직선의 성질**',
        ('fig', 'image7', [
            "✰ $angle HFH' `=` pi over2 $",
            "✰ $bar HH'$을 지름으로 하고 중심이 $N$인 원은 $bar PQ$에 접한다.",
            "$triangle PHF$와 $triangle QH'F$는 이등변삼각형",
            "↳ $angle PHF `=` angle PFH`=` a$, $angle QH'F `=` angle QFH'`=` b$라고 할 때",
            "↳ $pi -(angle FHH' +angle FH'H ) =a+b= angle HFH'$",
            "↳ $a+b + angle HFH' = pi $ → $a+b= pi over 2$",
        ]),
        ('fig', 'image8', [
            '✰ $barPQ$의 중점을 중심으로 하는 원은 준선에 접한다.',
            "↳ $bar HP parallel bar H'Q$이므로 $bar HH' BOT bar NM$, 즉 원은 준선에 접한다.",
            '↳ $triangle PHQ$는 직각삼각형',
        ]),
    ]),

    ('box', '포물선의 성질 ② 포물선과 접선', [
        '➊ 준선 위의 점에서 포물선에 그은 두 접선은 서로 수직이고, 두 접점을 이은 직선은 초점을 지난다.',
        "➋ 포물선 위의 점 $A$에서의 접선이 $x$축과 만나는 점을 $A'$, $A$에서 준선에 내린 수선의 발을 $H$라 하면",
        "    $bar A'F`=` bar AF`=` bar AH$이고, 사각형 $AHA'F$는 마름모이다.",
        "    ↳ 접선 $AA'$은 $angle HAF$의 이등분선이다.",
    ]),

    ('ihae', '이해', [
        ('fig', 'image9', [
            '✰ **준선에서 포물선에 그은 두 접선은 수직이다.**',
            '↳ 두 접점을 이은 직선은 포물선의 초점을 지난다.',
            '↳ 직선 $y`=` mx + p overm$이 $(-p,``b)$를 지날 때',
            '↳ $mb`= -m^2 p+p$ → $pm^2 +bm-p=0$ : 두 근의 곱이 $-1$',
            '↳ 두 접선의 기울기(=방정식의 두 실근)의 곱이 $-1$',
        ]),
        ('fig', 'image10', [
            "✰ **$bar A'F`=` bar AF`=` bar AH$ → 사각형 $AHA'F$는 마름모**",
            "↳ 접선 $y_1 y=2p(x+x_1 )$의 $x$절편 $A'(-x_1 ,`0)$ → $bar A'F `=` x_1 +p`=` bar AH`=` bar AF$",
            "✰ $bar AA'$은 $angle HAF$의 이등분선 ($because$ 마름모)",
            '✰ 마름모의 중심은 $y$축 위에 있다.',
            "✰ $bar FH'`=` bar FA'`=` bar AF$ & 사각형 $AH'FH$는 평행사변형",
            "↳ $bar FH'`=` bar FA'`=` bar FA$ ($because$ $F$가 $triangle AA'H'$의 외심)",
        ]),
    ]),
]
