import numpy as np

def vat_angle_field(X, Y, theta0=0.0, kx=45.0, ky=0.0):
    return theta0 + kx*(2*X-1.0) + ky*(2*Y-1.0)

def panel_grid(width, height, nx=200, ny=120):
    x = np.linspace(0, width, nx); y = np.linspace(0, height, ny)
    return np.meshgrid(x,y, indexing='xy')

def streamline_paths(width, height, theta_func, tow=0.006, spacing=0.006, step=0.001):
    Xg, Yg = panel_grid(width, height, nx=int(width/step)+1, ny=int(height/step)+1)
    Theta = theta_func(Xg/width, Yg/height)
    ux = np.cos(np.deg2rad(Theta)); uy = np.sin(np.deg2rad(Theta))
    seeds = np.arange(spacing/2, height, spacing)
    paths = []
    for y0 in seeds:
        x,y = 0.0, y0
        pts = [(x,y)]
        for _ in range(20000):
            ix = int(np.clip((x/width)*(ux.shape[1]-1), 0, ux.shape[1]-1))
            iy = int(np.clip((y/height)*(ux.shape[0]-1), 0, ux.shape[0]-1))
            dx = ux[iy,ix]*step; dy = uy[iy,ix]*step
            x += dx; y += dy
            if x<0 or x>width or y<0 or y>height: break
            pts.append((x,y))
        if len(pts)>5: paths.append(np.array(pts))
    return paths
