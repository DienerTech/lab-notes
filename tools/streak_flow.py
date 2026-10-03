"""Measure which way streaks flow relative to a vanishing point: inward (into it) or outward.

    python streak_flow.py WITH_STREAKS.mkv WITHOUT_STREAKS.mkv VPX VPY

Subtracting a render without the layer isolates the streaks. Then, for rays from the vanishing point,
intensity profiles in consecutive frames are cross-correlated; the median lag is the radial speed in
px/frame (positive = outward, negative = inward).

Why not optical flow or phase correlation: thin streaks moving along their own length are an aperture
problem, and those methods report ~zero. Requires numpy, scipy, av.
"""
import argparse
import av
import numpy as np
from scipy import ndimage


def load(p):
    with av.open(p) as c:
        return [f.to_ndarray(format="rgb24").astype(np.float32).mean(2) for f in c.decode(video=0)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("with_layer"); ap.add_argument("without_layer"); ap.add_argument("vpx", type=float); ap.add_argument("vpy", type=float)
    ap.add_argument("--angles", type=float, nargs=3, default=[0, 360, 4], help="start stop step, degrees")
    a = ap.parse_args()
    X, B = load(a.with_layer), load(a.without_layer)
    L = [np.clip(x - b, 0, None) for x, b in zip(X, B)]
    H, W = L[0].shape; rr = np.arange(60, max(H, W), 1.0); lags = []
    for t in range(1, len(L) - 1, 2):
        for th in np.deg2rad(np.arange(*a.angles)):
            xs, ys = a.vpx + rr * np.cos(th), a.vpy + rr * np.sin(th)
            ok = (xs > 2) & (xs < W - 3) & (ys > 2) & (ys < H - 3)
            if ok.sum() < 80: continue
            p = ndimage.map_coordinates(L[t], [ys[ok], xs[ok]], order=1); q = ndimage.map_coordinates(L[t + 1], [ys[ok], xs[ok]], order=1)
            if p.max() < 20 or q.max() < 20: continue
            p, q = p - p.mean(), q - q.mean(); lag = int(np.argmax(np.correlate(q, p, mode="full")) - (len(p) - 1))
            if abs(lag) < 60: lags.append(lag)
    m = float(np.median(lags)) if lags else float("nan")
    print(f"median radial shift {m:+.1f} px/frame over {len(lags)} ray samples -> {'INWARD' if m < 0 else 'OUTWARD'}")


if __name__ == "__main__":
    main()
