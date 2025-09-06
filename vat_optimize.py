import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse, os, time, csv
import numpy as np
from vatopt import clt, vat, afp, optim

def abd_from_angles(angles):
    tf = 1.0/len(angles)
    A,B,D = clt.ABD_stack([(ang, tf) for ang in angles])
    return A,B,D

def evaluate_afp(width, height, angles, tow, spacing, step=0.002):
    def theta_field(X,Y):
        return vat.vat_angle_field(X,Y, theta0=angles[0], kx=angles[1], ky=angles[2] if len(angles)>2 else 0.0)
    paths = vat.streamline_paths(width, height, theta_field, tow=tow, spacing=spacing, step=step)
    radii = []
    for p in paths:
        r = afp.curvature_radius(p)
        if r.size: radii.append(r.min())
    minR = min(radii) if radii else np.inf
    deltas = afp.gaps_overlaps(paths, tow)
    gap_violation = max(0.0, float(np.max(deltas) if deltas.size else 0.0))
    overlap_violation = max(0.0, float(-np.min(deltas) if deltas.size else 0.0))
    return {'min_radius': float(minR), 'gap_violation': gap_violation, 'overlap_violation': overlap_violation}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--width', type=float, default=0.5)
    ap.add_argument('--height', type=float, default=0.3)
    ap.add_argument('--plies', type=int, default=4)
    ap.add_argument('--tow', type=float, default=0.006)
    ap.add_argument('--spacing', type=float, default=0.006)
    ap.add_argument('--rmin', type=float, default=0.5)
    ap.add_argument('--algo', choices=['de','slsqp','bfgs'], default='de')
    ap.add_argument('--out', default='results/demo')
    ap.add_argument('--fast', action='store_true')
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    bounds = [(-45,45), (-60,60), (-60,60)]

    def fun(x):
        _,_,D = abd_from_angles([x[0]]*args.plies)
        stiff = -D[0,0]
        step = 0.005 if args.fast else 0.002
        metrics = evaluate_afp(args.width, args.height, x, args.tow, args.spacing, step=step)
        pen = optim.penalty_afp(metrics, rmin=args.rmin, gap_tol=0.0)
        return stiff + pen

    t0 = time.time()
    if args.algo=='de':
        res = optim.run_de(fun, bounds, maxiter=8, popsize=6)
    elif args.algo=='slsqp':
        res = optim.run_slsqp(np.array([0.0, 10.0, 0.0]), fun, bounds)
    else:
        res = optim.run_bfgs(np.array([0.0, 10.0, 0.0]), fun)
    t1 = time.time()

    with open(os.path.join(args.out, f'optim_{args.algo}.csv'), 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['algo','theta0','kx','ky','objective','time_s'])
        w.writerow([args.algo, *res.x, float(res.fun), t1 - t0])

    print(f'[{args.algo}] x* = {res.x}, f* = {res.fun:.3e}, time = {t1-t0:.3f}s')

if __name__=='__main__':
    main()
