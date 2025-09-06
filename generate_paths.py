import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse, os, csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from vatopt import vat

ap = argparse.ArgumentParser()
ap.add_argument('--width', type=float, default=0.5)
ap.add_argument('--height', type=float, default=0.3)
ap.add_argument('--tow', type=float, default=0.006)
ap.add_argument('--spacing', type=float, default=0.006)
ap.add_argument('--out', default='results/demo')
args = ap.parse_args()

os.makedirs(args.out, exist_ok=True)

def theta_field(X,Y):
    return vat.vat_angle_field(X,Y, theta0=0.0, kx=30.0, ky=0.0)

paths = vat.streamline_paths(args.width, args.height, theta_field, tow=args.tow, spacing=args.spacing, step=0.001)

with open(os.path.join(args.out, 'paths.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['path_id','x','y'])
    for i, p in enumerate(paths):
        for x,y in p:
            w.writerow([i, x, y])

plt.figure()
for p in paths: plt.plot(p[:,0], p[:,1], linewidth=1)
plt.axis('equal'); plt.xlabel('x [m]'); plt.ylabel('y [m]'); plt.title('Fibre paths'); plt.tight_layout()
plt.savefig(os.path.join(args.out, 'paths.png'), dpi=160)
print(f'Saved {len(paths)} paths to {args.out}/paths.csv')
