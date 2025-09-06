# Composite VAT Toolbox

Variable-Angle Tow (VAT) design toolbox that:

* generates fibre toolpaths from a VAT angle field,
* checks automated fibre placement (AFP) manufacturability (minimum steering radius, gaps/overlaps),
* optimises VAT parameters using gradient‑based methods (SLSQP, BFGS) and a global metaheuristic (Differential Evolution),
* exports a minimal Abaqus shell coupon for further finite element analysis,
* previews fibre paths in Rhino/Grasshopper using a simple GHPython snippet.

## Quickstart

```bash
# 1) install dependencies
pip install -r requirements.txt

# 2) generate fibre paths for a rectangular panel
python scripts/generate_paths.py --width 0.5 --height 0.3 --tow 0.006 --spacing 0.006 --out results/case1
## Repository structure

* Core modules (root-level): `afp.py`, `clt.py`, `optim.py`, `toolpaths.py`, `vat.py`, `abaqus.py`, `__init__.py`
* CLI scripts (root-level): `generate_paths.py`, `afp_check.py`, `vat_optimize.py`, `run_benchmarks.py`, `hops_server.py`
* `grasshopper/ghpython_snippets/` – GHPython snippets for previewing fibre curves in Rhino/Grasshopper (e.g., `afp_preview.py`).
* `requirements.txt` – Python dependencies.
* `.gitignore` – ignore patterns for Python caches and result artifacts.


* Additional CLI scripts: `vat_optimize.py`, `write_abaqus_inp.py`.
* Additional details: the root package (`vatopt`) contains the true implementations, including `vatopt/afp.py`, `vatopt/clt.py`, `vatopt/optim.py`, `vatopt/vat.py`, and `vatopt/fea/abaqus.py` for Abaqus export.


# 3) evaluate AFP feasibility (plots + metrics)
python scripts/afp_check.py --paths results/case1/paths.csv --tow 0.006 --rmin 0.5 --out results/case1

# 4) optimise VAT parameters (fast demo)
python scripts/vat_optimize.py --algo slsqp --fast --spacing 0.03 --out results/case1

# 5) run benchmarks (optional)
python scripts/run_benchmarks.py

# 6) export an Abaqus coupon (optional)
python scripts/write_abaqus_inp.py --width 0.5 --height 0.3 --plies 4 --out results/case1/coupon.inp
```

## 
## License

This repository is provided for educational and research purposes. Feel free to adapt and extend it for your own projects.
