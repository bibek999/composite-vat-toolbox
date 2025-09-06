import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# optional hops server example (requires flask + ghhops-server)
from flask import Flask, request, jsonify
try:
    import ghhops_server as hs
except Exception:
    hs = None
from vatopt import vat
app = Flask(__name__)
if hs: hops = hs.Hops(app)
@app.route('/vat_angles', methods=['GET'])
def vat_angles():
    w = float(request.args.get('width', 0.5)); h = float(request.args.get('height', 0.3))
    t0 = float(request.args.get('theta0', 0.0)); kx = float(request.args.get('kx', 30.0)); ky = float(request.args.get('ky', 0.0))
    X,Y = vat.panel_grid(w,h, nx=80, ny=60)
    Th = vat.vat_angle_field(X/w, Y/h, t0, kx, ky)
    return jsonify(dict(angles=Th.tolist()))
