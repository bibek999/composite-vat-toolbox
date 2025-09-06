import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os, time, csv, numpy as np
from vatopt import optim
from scripts.vat_optimize import abd_from_angles, evaluate_afp

outdir = 'results/benchmarks'
os.makedirs(outdir, exist_ok=True)

cases = [
    dict(width=0.4, height=0.25, tow=0.006, spacing=0.03, rmin=0.5),
    dict(width=0.6, height=0.35, tow=0.006, spacing=0.03, rmin=0.7),
]

bounds = [(-45,45), (-60,60), (-60,60)]

def run_case(case, algo):
    def fun(x):
        _,_,D = abd_from_angles([x[0]]*4)
        stiff = -D[0,0]
        metrics = evaluate_afp(case['width'], case['height'], x, case['tow'], case['spacing'])
        pen = optim.penalty_afp(metrics, rmin=case['rmin'], gap_tol=0.0)
        return stiff + pen
    t0=time.time()
    if algo=='de':
        res = optim.run_de(fun, bounds)
    elif algo=='slsqp':
        res = optim.run_slsqp(np.array([0.0,10.0,0.0]), fun, bounds)
    else:
        res = optim.run_bfgs(np.array([0.0,10.0,0.0]), fun)
    return time.time()-t0, res

with open(os.path.join(outdir,'benchmark_results.csv'),'w',newline='') as f:
    w=csv.writer(f); w.writerow(['case','algo','theta0','kx','ky','f','time_s'])
    for i,c in enumerate(cases):
        for algo in ['slsqp']:
            t,res = run_case(c, algo)
            w.writerow([i, algo, *res.x, res.fun, t])
print('Wrote results to', os.path.join(outdir,'benchmark_results.csv'))
