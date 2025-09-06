import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse, os, csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from vatopt import afp

def load_paths(csv_path):
    paths = []
    with open(csv_path,'r') as f:
        r = csv.DictReader(f)
        cur_id = None; cur = []
        for row in r:
            pid = int(row['path_id']); x = float(row['x']); y = float(row['y'])
            if cur_id is None: cur_id = pid
            if pid != cur_id:
                paths.append(np.array(cur)); cur = []; cur_id = pid
            cur.append((x,y))
        if cur: paths.append(np.array(cur))
    return paths

ap = argparse.ArgumentParser()
ap.add_argument('--paths', required=True)
ap.add_argument('--tow', type=float, default=0.006)
ap.add_argument('--rmin', type=float, default=0.5)
ap.add_argument('--out', default='results/demo')
args = ap.parse_args()

os.makedirs(args.out, exist_ok=True)
paths = load_paths(args.paths)

# curvature
allR = []
for p in paths:
    R = afp.curvature_radius(p)
    if R.size: allR.extend(R.tolist())
allR = np.array(allR)
finite = allR[np.isfinite(allR)]

plt.figure()
if finite.size: plt.hist(finite, bins=40)
plt.axvline(args.rmin, linestyle='--')
plt.xlabel('Local radius [m]'); plt.ylabel('count'); plt.title('AFP curvature histogram')
plt.tight_layout(); plt.savefig(os.path.join(args.out,'afp_curvature_hist.png'), dpi=160)

# gaps/overlaps
deltas = afp.gaps_overlaps(paths, args.tow)
plt.figure()
if deltas.size: plt.hist(deltas*1e3, bins=40)
plt.axvline(0.0, linestyle='--')
plt.xlabel('delta = spacing - tow_width [mm] (+gap, -overlap)')
plt.ylabel('count'); plt.title('Gaps/overlaps histogram')
plt.tight_layout(); plt.savefig(os.path.join(args.out,'gaps_overlaps_hist.png'), dpi=160)

print(f'AFP min radius: {np.nanmin(finite) if finite.size else float("nan"):.3f} m')
print(f'Gap/overlap delta range [mm]: {np.min(deltas)*1e3 if deltas.size else float("nan"):.3f} .. {np.max(deltas)*1e3 if deltas.size else float("nan"):.3f}')
