# 시험지 스타일 함수 그래프 (흑백, 화살표 축, 원점 O, 점선 보조선)
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({'mathtext.fontset': 'stix', 'font.family': 'STIXGeneral', 'font.size': 13})

def axes(ax, xr, yr):
    ax.set_xlim(*xr); ax.set_ylim(*yr); ax.set_aspect('equal'); ax.axis('off')
    kw = dict(arrowstyle='-|>,head_length=0.5,head_width=0.18', lw=0.8, color='k')
    ax.annotate('', (xr[1], 0), (xr[0], 0), arrowprops=kw)
    ax.annotate('', (0, yr[1]), (0, yr[0]), arrowprops=kw)
    ax.text(xr[1], -0.15, '$x$', ha='right', va='top')
    ax.text(0.12, yr[1], '$y$', ha='left', va='top')
    ax.text(-0.12, -0.12, '$O$', ha='right', va='top')

def pt(ax, x, y, label, dx=0.12, dy=0.12, ha='left', va='bottom'):
    ax.plot(x, y, 'o', ms=3.5, color='k')
    ax.text(x + dx, y + dy, label, ha=ha, va=va)

def save(fig, path):
    fig.savefig(path, dpi=300, bbox_inches='tight', pad_inches=0.05, facecolor='white')
    plt.close(fig)

if __name__ == '__main__':
    # 예시: 포물선 y^2 = 4px (p=1), 초점 F, 준선 x=-p, 포물선 위의 점 P와 준선 위의 수선의 발 H
    p = 1
    fig, ax = plt.subplots(figsize=(3.4, 3.4))
    axes(ax, (-2.4, 4.6), (-3.6, 3.8))
    y = np.linspace(-3.4, 3.4, 400)
    ax.plot(y**2 / (4*p), y, color='k', lw=1.3)
    ax.plot([-p, -p], [-3.5, 3.5], color='k', lw=0.8)
    ax.text(-p - 0.1, -3.5, '$x=-p$', ha='right', va='bottom', fontsize=11)
    py = 2.4; px = py**2 / (4*p)
    ax.plot([-p, px], [py, py], 'k--', lw=0.7, dashes=(3, 2))
    ax.plot([px, p], [py, 0], 'k--', lw=0.7, dashes=(3, 2))
    pt(ax, p, 0, '$F$', dy=-0.15, va='top')
    pt(ax, px, py, '$P$')
    pt(ax, -p, py, '$H$', dx=-0.12, ha='right')
    ax.text(3.6, 3.3, '$y^2=4px$', fontsize=12)
    save(fig, 'sample_parabola.png')
    print('ok')
