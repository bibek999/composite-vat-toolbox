"""
CLI wrapper to write a basic composite coupon for Abaqus.

This script leverages the Abaqus writer provided in the vatopt.fea module. It
builds a rectangular shell coupon with a layered composite layup and writes an
INP file that can be imported into Abaqus/CAE for further analysis.

Usage:
    python scripts/write_abaqus_inp.py --width 0.5 --height 0.3 --plies 4 --out results/demo/coupon.inp

The units throughout this toolbox are assumed to be SI (metres, seconds,
Newtons, Pascals). Make sure loads and boundary conditions in your FE solver
are consistent with the geometry defined here.
"""

import argparse
import os
from vatopt.fea.abaqus import write_abaqus_coupon


def main() -> None:
    parser = argparse.ArgumentParser(description="Write a composite coupon to an Abaqus INP file.")
    parser.add_argument(
        "--width",
        type=float,
        default=0.5,
        help="Panel width in metres (default: 0.5)",
    )
    parser.add_argument(
        "--height",
        type=float,
        default=0.3,
        help="Panel height in metres (default: 0.3)",
    )
    parser.add_argument(
        "--plies",
        type=int,
        default=4,
        help="Number of plies (layers) in the laminate (default: 4)",
    )
    parser.add_argument(
        "--out",
        default="results/demo/coupon.inp",
        help="Output path for the Abaqus INP file (default: results/demo/coupon.inp)",
    )
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    out_path = args.out
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Use a uniform ply angle for the coupon. Customize this list as needed.
    angles = [0.0] * args.plies

    write_abaqus_coupon(out_path, args.width, args.height, angles)
    print(f"Wrote INP to {out_path}")


if __name__ == "__main__":
    main()