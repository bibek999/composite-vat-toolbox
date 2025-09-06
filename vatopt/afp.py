import numpy as np

def curvature_radius(poly):
    p = np.asarray(poly)
    if p.shape[0] < 3: return np.array([])
    radii = []
    for i in range(1, len(p)-1):
        a,b,c = p[i-1], p[i], p[i+1]
        ab, bc, ac = b-a, c-b, c-a
        cross = np.cross(np.append(ab,0), np.append(bc,0))
        area2 = np.linalg.norm(cross)
        la, lb, lc = np.linalg.norm(ab), np.linalg.norm(bc), np.linalg.norm(ac)
        if area2 < 1e-12:
            radii.append(np.inf); continue
        R = (la*lb*lc)/area2
        radii.append(R)
    return np.array(radii)

def gaps_overlaps(paths, tow_width):
    deltas = []
    for i in range(len(paths)-1):
        a, b = paths[i], paths[i+1]
        n = min(len(a), len(b))
        if n<2: continue
        d = np.linalg.norm(a[:n]-b[:n], axis=1) - tow_width
        deltas.append(d)
    return np.concatenate(deltas) if deltas else np.array([])
