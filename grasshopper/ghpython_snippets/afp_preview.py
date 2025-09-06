"""GHPython snippet to preview paths.csv"""
import Rhino.Geometry as rg
curves = []
try:
    with open(csvPath, 'r') as f:
        header = f.readline()
        current = []; pid_prev=None
        for line in f:
            pid,xs,ys = line.strip().split(',')
            pid = int(pid); x=float(xs); y=float(ys)
            if pid_prev is None: pid_prev=pid
            if pid!=pid_prev:
                if len(current)>1:
                    pts=[rg.Point3d(px,py,0.0) for (px,py) in current]
                    curves.append(rg.Polyline(pts).ToNurbsCurve())
                current=[]; pid_prev=pid
            current.append((x,y))
        if len(current)>1:
            pts=[rg.Point3d(px,py,0.0) for (px,py) in current]
            curves.append(rg.Polyline(pts).ToNurbsCurve())
except Exception: pass
