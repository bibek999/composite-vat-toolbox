# Composite VAT Toolbox

Variable-Angle Tow (VAT) design toolbox that:

- Generates fibre toolpaths from a VAT angle field.
- Checks automated fibre placement (AFP) manufacturability (minimum steering radius, gaps/overlaps).
- Optimises VAT parameters using gradient-based methods (SLSQP, BFGS) and a global metaheuristic (Differential Evolution).
- Exports a minimal Abaqus shell coupon for further finite element analysis.
- Previews fibre paths in Rhino/Grasshopper using a simple GHPython snippet.

## Quickstart

1. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate fibre paths for a rectangular panel**  
   ```bash
   python scripts/generate_paths.py --width 0.5 --height 0.3 --tow 0.006 --spacing 0.006 --out results/case1
   ```

3. **Evaluate AFP feasibility (plots + metrics)**  
   ```bash
   python scripts/afp_check.py --paths results/case1/paths.csv --tow 0.006 --rmin 0.5 --out results/case1
   ```

4. **Optimise VAT parameters (fast demo)**  
   ```bash
   python scripts/vat_optimize.py --algo slsqp --fast --spacing 0.03 --out results/case1
   ```

5. **Run benchmarks (optional)**  
   ```bash
   python scripts/run_benchmarks.py
   ```

6. **Export an Abaqus coupon (optional)**  
   ```bash
   python scripts/write_abaqus_inp.py --width 0.5 --height 0.3 --plies 4 --out results/case1/coupon.inp
   ```

## Repository structure

- **vatopt/** – Python package with core modules:
  - `afp.py`, `clt.py`, `optim.py`, `toolpaths.py`, `vat.py` implement AFP checks, classical laminate theory, optimisation routines, toolpath integration, and VAT field definitions.
  - `fea/abaqus.py` writes a minimal Abaqus shell coupon (.inp).
- **scripts/** – Command-line tools for path generation, AFP checking, optimisation, benchmarking, Hops server, and Abaqus input generation.
- **grasshopper/ghpython_snippets/** – GHPython snippets for previewing fibre curves in Rhino/Grasshopper (e.g., `afp_preview.py`).
- **results/** – Example outputs (`case1/`) and benchmark results.
- **requirements.txt** – Python dependencies.
- **.gitignore** – Ignore patterns for Python caches and result artifacts.
- **README.md** – This documentation.

## License

This repository is provided for educational and research purposes. Feel free to adapt and extend it for your own projects.
