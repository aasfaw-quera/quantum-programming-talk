### Regenerates images/ry-bloch-sphere.png: the states Ry(theta)|0> visits on the Bloch sphere
### as theta goes around, one dot per step, for the variational eigensolver notebook.
### The style follows the Bloch sphere figure in QuEra's Bloqade VQE workshop.
###
### Ry(theta)|0> = cos(theta/2)|0> + sin(theta/2)|1>  ->  Bloch vector (sin theta, 0, cos theta),
### so Ry walks the qubit around the circle through |0>, +x, |1> and -x.
###
### Axes follow the usual right-handed Bloch sphere drawing: x out of the page (lower left),
### y to the right, z up, so that x cross y = z.
###
### Run from this folder:   python make_ry_figure.py

import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'images', 'ry-bloch-sphere.png')

plt.rcParams['mathtext.fontset'] = 'cm'
ROMAN = dict(fontfamily='cmr10')

BLUE = '#4f5bd5'
RED = '#d1435b'
GRAY = '#6b7280'
LIGHT_GRAY = '#b8b8c0'

# orthographic view from slightly above the equator and a little round from the x axis,
# so x points out of the page towards the lower left and y to the right
azimuth, elevation = np.deg2rad(35), np.deg2rad(15)
toward_viewer = np.array([np.cos(elevation) * np.cos(azimuth), np.cos(elevation) * np.sin(azimuth), np.sin(elevation)])
screen_right = np.cross([0, 0, 1], toward_viewer)
screen_right /= np.linalg.norm(screen_right)
screen_up = np.cross(toward_viewer, screen_right)
# (right, up, towards viewer) must be right-handed, otherwise the drawing is a mirror image
assert np.allclose(np.cross(screen_right, screen_up), toward_viewer)


def project(points):
	"""3D points (..., 3) -> screen x, screen y, depth (depth > 0 is the front half of the sphere)."""
	points = np.asarray(points, dtype=float)
	return points @ screen_right, points @ screen_up, points @ toward_viewer


fig, ax = plt.subplots(figsize=(6.4, 4.6))
ax.set_aspect('equal')
ax.axis('off')
ax.set_xlim(-1.95, 1.75)
ax.set_ylim(-1.3, 1.3)

# sphere
ax.add_patch(Circle((0, 0), 1, facecolor='#f6f6fe', edgecolor=LIGHT_GRAY, linewidth=1.5, zorder=0))

# equator: back half dashed, front half solid
ring = np.linspace(0, 2 * np.pi, 400)
ex, ey, ed = project(np.stack([np.cos(ring), np.sin(ring), np.zeros_like(ring)], axis=-1))
ax.plot(np.where(ed < 0, ex, np.nan), np.where(ed < 0, ey, np.nan), color=LIGHT_GRAY, lw=1, ls='--', zorder=1)
ax.plot(np.where(ed >= 0, ex, np.nan), np.where(ed >= 0, ey, np.nan), color=LIGHT_GRAY, lw=1, zorder=1)

# axes
for direction, name, offset in [((1, 0, 0), 'x', (-0.1, -0.1)), ((0, 1, 0), 'y', (0.12, -0.02)), ((0, 0, 1.2), 'z', (0.07, 0.07))]:
	sx, sy, _ = project(direction)
	ax.annotate('', xy=(sx, sy), xytext=(0, 0), zorder=2,
				arrowprops=dict(arrowstyle='-|>', color=GRAY, lw=1.2, mutation_scale=12, shrinkA=0, shrinkB=0))
	ax.text(sx + offset[0], sy + offset[1], f'${name}$', color=GRAY, fontsize=15, ha='center', va='center')

# poles
nx, ny, _ = project((0, 0, 1))
sx, sy, _ = project((0, 0, -1))
ax.text(nx - 0.2, ny + 0.1, r'$|0\rangle$', fontsize=16, ha='center', va='center')
ax.text(sx, sy - 0.17, r'$|1\rangle$', fontsize=16, ha='center', va='center')

# the states Ry(theta)|0> for theta = 0, pi/8, 2pi/8, ...: front half solid, back half faded
thetas = np.arange(16) * np.pi / 8
dx, dy, _ = project(np.stack([np.sin(thetas), np.zeros_like(thetas), np.cos(thetas)], axis=-1))
front = np.sin(thetas) >= -1e-9  # the +x half of the circle faces the viewer (both poles included)
# faint guide through the dots, so they read as one circle
path = np.linspace(0, 2 * np.pi, 400)
gx, gy, _ = project(np.stack([np.sin(path), np.zeros_like(path), np.cos(path)], axis=-1))
ax.plot(np.where(np.sin(path) >= 0, gx, np.nan), np.where(np.sin(path) >= 0, gy, np.nan), color=BLUE, lw=1, alpha=0.3, zorder=2)
ax.plot(np.where(np.sin(path) < 0, gx, np.nan), np.where(np.sin(path) < 0, gy, np.nan), color=BLUE, lw=1, alpha=0.15, ls='--', zorder=2)
ax.scatter(dx[front], dy[front], s=70, color=BLUE, zorder=4, edgecolor='white', linewidth=0.8)
ax.scatter(dx[~front], dy[~front], s=70, color=BLUE, alpha=0.35, zorder=3, edgecolor='white', linewidth=0.8)

# label a few of the dots with their theta
for theta, text, (ox, oy) in [(np.pi / 2, r'$\theta=\pi/2$', (-0.4, 0.06)), (3 * np.pi / 2, r'$\theta=3\pi/2$', (0.42, 0.04))]:
	px, py, _ = project((np.sin(theta), 0, np.cos(theta)))
	ax.text(px + ox, py + oy, text, color=BLUE, fontsize=12, ha='center', va='center')

# direction of travel as theta increases
a0, a1 = np.pi / 8 + 0.08, 3 * np.pi / 8 - 0.08
ax0, ay0, _ = project((1.12 * np.sin(a0), 0, 1.12 * np.cos(a0)))
ax1, ay1, _ = project((1.12 * np.sin(a1), 0, 1.12 * np.cos(a1)))
ax.add_patch(FancyArrowPatch((ax0, ay0), (ax1, ay1), connectionstyle='arc3,rad=0.25', arrowstyle='-|>',
							 mutation_scale=12, color=BLUE, lw=1.4, zorder=4))

# callout
ax.text(-1.12, 0.72, r'$R_y(\theta)\,|0\rangle$', color=BLUE, fontsize=15, ha='right', va='bottom')
ax.text(-1.12, 0.66, r'$\theta = 0,\ \pi/8,\ 2\pi/8,\ \ldots$', color=BLUE, fontsize=13, ha='right', va='top')

# where the optimizer ends up: theta = pi, the state |1>, which always measures 1 (cost 0)
ax.annotate('', xy=(sx, sy + 0.04), xytext=(0, 0), zorder=5,
			arrowprops=dict(arrowstyle='-|>', color=RED, lw=2.2, mutation_scale=14, shrinkA=0, shrinkB=0))
ax.text(0.62, -1.02, 'optimizer finds\n' + r'$\theta=\pi$' + ', so cost is 0', color=RED, fontsize=12.5,
		ha='left', va='center', **ROMAN)

fig.savefig(OUT, dpi=150, bbox_inches='tight', facecolor='white')
print('wrote', OUT)
