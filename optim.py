import numpy as np
from scipy.optimize import minimize, differential_evolution

def penalty_afp(metrics, rmin, gap_tol):
    pen = 0.0
    if metrics.get('min_radius', np.inf) < rmin:
        pen += 1e6*(rmin - metrics['min_radius'])
    if metrics.get('gap_violation', 0.0) > 0.0:
        pen += 1e6*metrics['gap_violation']
    if metrics.get('overlap_violation', 0.0) > 0.0:
        pen += 1e6*metrics['overlap_violation']
    return pen

def run_slsqp(x0, fun, bounds):
    return minimize(fun, x0, method='SLSQP', bounds=bounds, options=dict(maxiter=200))

def run_bfgs(x0, fun):
    return minimize(fun, x0, method='BFGS', options=dict(maxiter=300))

def run_de(fun, bounds, seed=0, maxiter=15, popsize=8):
    return differential_evolution(fun, bounds=bounds, seed=seed, polish=True, updating='deferred', maxiter=maxiter, popsize=popsize)
