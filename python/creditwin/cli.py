import argparse
from pathlib import Path
from .report import generate
def main():
    p=argparse.ArgumentParser(prog='creditwin'); p.add_argument('command',choices=['verify']); p.add_argument('--root',default='.')
    a=p.parse_args()
    if a.command=='verify':
        m=generate(Path(a.root).resolve()); print(f"RMSE={m['calibration']['sensor_rmse_k']:.4f} K")
if __name__=='__main__': main()
