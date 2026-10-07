# 2026 2-2 중간 미적분Ⅰ 4번 그래프 (원본 스캔을 보고 다시 그림)
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '그래프'))
from exam_graph import plt, axes, save

def dot(ax, x, y, filled=True):
    ax.plot(x, y, 'o', ms=4.2, mfc='k' if filled else 'white', mec='k', mew=0.9, zorder=5)

def dash(ax, xs, ys):
    ax.plot(xs, ys, 'k--', lw=0.6, dashes=(2.5, 2))

fig, ax = plt.subplots(figsize=(3.3, 2.9))
axes(ax, (-3.7, 3.9), (-2.6, 2.75))
L = dict(color='k', lw=1.3)
x = np.linspace(-3.45, -2, 50); ax.plot(x, 1.5 * (x + 2), **L)
x = np.linspace(-2, 0, 100); ax.plot(x, x**2 - 2, **L)
ax.plot([0, 1], [1, 2], **L)
ax.plot([1, 2], [1, 0], **L)
ax.plot([2, 3.6], [0, 1.6], **L)
dash(ax, [-2, 1], [2, 2]); dash(ax, [-2, -2], [0, 2]); dash(ax, [1, 1], [0, 2])
dash(ax, [0, 2], [1, 1]); dash(ax, [2, 2], [0, 1]); dash(ax, [3, 3], [0, 1])
dash(ax, [-3, -3], [0, -1.5])
dot(ax, -2, 0, False); dot(ax, -2, 2)
dot(ax, 0, -2, False); dot(ax, 0, 1)
dot(ax, 1, 2, False); dot(ax, 1, 1, False); dot(ax, 1, 0)
dot(ax, 2, 0, False); dot(ax, 2, 1)
for v, s in [(-3, '$-3$'), (-2, '$-2$')]:
    ax.text(v, 0.12, s, ha='center', va='bottom', fontsize=11)
for v in (1, 2, 3):
    ax.text(v, -0.15, f'${v}$', ha='center', va='top', fontsize=11)
for v, s in [(2, '$2$'), (1, '$1$'), (-2, '$-2$')]:
    ax.text(-0.12, v, s, ha='right', va='center', fontsize=11, bbox=dict(fc='white', ec='none', pad=0.5))
ax.text(1.3, 2.35, '$y=f(x)$', fontsize=12)
save(fig, sys.argv[1] if len(sys.argv) > 1 else 'q4.png')
