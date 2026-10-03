"""Add a beat-locked warp-streak layer and/or an eased push-in to a clip, behind a warm-coloured subject.

    python warp_streaks.py IN.mp4 OUT.mkv --inward --push 1.0 1.1 [--beats beats.json --fps 24 --film-start 248]

* The vanishing point is fitted to the clip's own painted streaks (structure-tensor orientations,
  least-squares line intersection, median over five frames), so the code layer shares the tunnel.
* Particles move along rays from the vanishing point with perspective speed dr/dt = +-k*r.
  Use --inward when the subject flies TOWARD the camera: the visible vanishing point is then behind it
  (the focus of contraction) and stars must rush INTO it. Outward flow there reads as "flying backwards".
* Beats: optional JSON list of beat frame numbers in film time (or {"beats": [...], "accents": [...]});
  speed and brightness surge on each with a 0.12 s decay.
* The subject matte is the convex hull of sizeable warm regions (tuned for a burgundy/gold hull on blue
  space). Adapt ship_matte() to your subject.
Output: lossless FFV1 (bgr0) plus a JSON sidecar. Requires numpy, pillow, scipy, av.
"""
import argparse, json
from pathlib import Path
import av
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from scipy.spatial import ConvexHull


def ship_matte(f):
    a = f.astype(np.float32); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = ndimage.binary_opening((r > b + 25) & (r > 60), iterations=1)
    lab, n = ndimage.label(m)
    if n == 0:
        return np.zeros(m.shape, np.float32), (f.shape[1] / 2, f.shape[0] / 2)
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    ys, xs = np.nonzero(np.isin(lab, [i + 1 for i, v in enumerate(sizes) if v >= 400]))
    hull = ConvexHull(np.stack([xs, ys], 1))
    im = Image.new("L", (f.shape[1], f.shape[0]), 0)
    ImageDraw.Draw(im).polygon([(float(xs[i]), float(ys[i])) for i in hull.vertices], fill=255)
    s = ndimage.binary_dilation(np.asarray(im) > 127, iterations=3)
    yy, xx = np.nonzero(s)
    return ndimage.gaussian_filter(s.astype(np.float32), 1.0), (float(xx.mean()), float(yy.mean()))


def vanishing_point(f, matte):
    g = f.astype(np.float32).mean(2)
    gx, gy = ndimage.sobel(g, 1), ndimage.sobel(g, 0)
    Jxx, Jyy, Jxy = [ndimage.gaussian_filter(v, 3) for v in (gx * gx, gy * gy, gx * gy)]
    tr = Jxx + Jyy; det = Jxx * Jyy - Jxy ** 2
    l1 = tr / 2 + np.sqrt(np.maximum(tr ** 2 / 4 - det, 0)); l2 = tr - l1
    coh = (l1 - l2) / (l1 + l2 + 1e-6); ang = 0.5 * np.arctan2(2 * Jxy, Jxx - Jyy)
    sel = (coh > 0.6) & (g > 60) & (matte < 0.05)
    sel[:8] = sel[-8:] = False; sel[:, :8] = sel[:, -8:] = False
    ys, xs = np.nonzero(sel)
    idx = np.random.default_rng(0).choice(len(xs), min(6000, len(xs)), replace=False); ys, xs = ys[idx], xs[idx]
    n = np.stack([np.cos(ang[ys, xs]), np.sin(ang[ys, xs])], 1); w = coh[ys, xs]
    A = (w[:, None, None] * n[:, :, None] * n[:, None, :]).sum(0)
    bvec = (w[:, None] * n * (n * np.stack([xs, ys], 1)).sum(1, keepdims=True)).sum(0)
    return np.linalg.solve(A, bvec)


def surges(n, film_start, beats_path):
    if not beats_path:
        return [0.0] * n
    d = json.loads(Path(beats_path).read_text())
    ev = [(b, 1.0) for b in (d if isinstance(d, list) else d.get("beats", []))] + ([(x, 1.6) for x in d.get("accents", [])] if isinstance(d, dict) else [])
    return [float(sum(A * np.exp(-((ff - fb) / 24.0) / 0.12) for fb, A in ev if 0 <= ff - fb < 12)) for ff in range(film_start, film_start + n)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip"); ap.add_argument("out")
    ap.add_argument("--push", type=float, nargs=2); ap.add_argument("--inward", action="store_true"); ap.add_argument("--no-streaks", action="store_true")
    ap.add_argument("--beats"); ap.add_argument("--film-start", type=int, default=0)
    ap.add_argument("--count", type=int, default=240); ap.add_argument("--gain", type=float, default=0.7)
    a = ap.parse_args()
    with av.open(a.clip) as c:
        frames = [f.to_ndarray(format="rgb24") for f in c.decode(video=0)]
    H, W = frames[0].shape[:2]; n = len(frames)
    _, centre = ship_matte(frames[0])
    vps = [vanishing_point(frames[t], ship_matte(frames[t])[0]) for t in np.linspace(0, n - 1, 5).astype(int)]
    vp = np.median(np.array(vps), 0)
    surge = surges(n, a.film_start, a.beats)
    rng = np.random.default_rng(20); S = 2; Rmax = np.hypot(W, H) * S
    th = rng.uniform(0, 2 * np.pi, a.count); r = np.exp(rng.uniform(np.log(12 * S), np.log(Rmax), a.count))
    wid = rng.uniform(0.8, 2.2, a.count); br = rng.uniform(0.55, 1.0, a.count); k0 = 0.055
    out = []
    for i, f in enumerate(frames):
        img = f.astype(np.float32) / 255
        if not a.no_streaks:
            sp = k0 * (1 + 1.4 * surge[i]); r_new = r * np.exp(-sp if a.inward else sp)
            lay = Image.new("L", (W * S, H * S), 0); d = ImageDraw.Draw(lay)
            for j in range(a.count):
                u = (np.cos(th[j]), np.sin(th[j]))
                r0, r1 = (r_new[j], r[j] * (1 + 1.2 * sp)) if a.inward else (r[j], r_new[j] * (1 + 1.2 * sp))
                v = int(255 * br[j] * min(1.0, (r0 / (60 * S)) ** 1.2) * min(1.0, 1.0 + 0.45 * surge[i]))
                d.line([(vp[0] * S + u[0] * r0, vp[1] * S + u[1] * r0), (vp[0] * S + u[0] * r1, vp[1] * S + u[1] * r1)],
                       fill=min(v, 255), width=max(1, int(round(wid[j] * S * (0.6 + 0.8 * r0 / Rmax)))))
            core = np.asarray(lay.resize((W, H), Image.LANCZOS)).astype(np.float32) / 255
            col = core[..., None] * np.array([0.82, 0.93, 1.0]) + ndimage.gaussian_filter(core, 2.5)[..., None] * np.array([0.18, 0.42, 1.0]) * 0.9
            img = np.clip(img + a.gain * col * (1 - ship_matte(f)[0][..., None]), 0, 1)
            r = r_new
            dead = (r < 14 * S) if a.inward else (r > Rmax)
            r[dead] = np.exp(rng.uniform(np.log(0.55 * Rmax), np.log(Rmax), dead.sum())) if a.inward else np.exp(rng.uniform(np.log(10 * S), np.log(80 * S), dead.sum()))
            th[dead] = rng.uniform(0, 2 * np.pi, dead.sum())
        if a.push:
            t = i / max(1, n - 1); e = t * t * (3 - 2 * t); s = a.push[0] + (a.push[1] - a.push[0]) * e
            pim = Image.fromarray((img * 255 + 0.5).astype(np.uint8))
            img = np.asarray(pim.transform((W, H), Image.AFFINE, (1 / s, 0, centre[0] - centre[0] / s, 0, 1 / s, centre[1] - centre[1] / s), Image.BICUBIC)).astype(np.float32) / 255
        out.append((img * 255 + 0.5).astype(np.uint8))
    with av.open(a.out, "w") as o:
        st = o.add_stream("ffv1", rate=24); st.width, st.height = W, H; st.pix_fmt = "bgr0"
        for fr in out:
            for p in st.encode(av.VideoFrame.from_ndarray(fr, format="rgb24").reformat(format="bgr0")): o.mux(p)
        for p in st.encode(): o.mux(p)
    Path(a.out).with_suffix(".json").write_text(json.dumps({"vanishing_point": [round(float(v), 1) for v in vp], "inward": a.inward, "push": a.push,
                                                            "film_start": a.film_start, "frames": n}, indent=1))
    print("done", a.out, "vp", [round(float(v), 1) for v in vp])


if __name__ == "__main__":
    main()
