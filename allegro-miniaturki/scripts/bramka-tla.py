# -*- coding: utf-8 -*-
"""Bramka tla miniatury: siatka 24x24, zero cieni (27.10.2026).

Tlo = neutralne piksele od jasnosci 170 polaczone z krawedzia kadru, wiec obejmuje tez cien i szare plamy.
Kadr dzielony na 24x24 pola; kazde pole, ktore w >= 60 proc. jest tlem, moze miec najwyzej 5 proc. gladkich szarych pikseli tla
ponizej 250 (zadnych smug, plam, prostokatow, halo ani cienia, takze kontaktowego). Narozniki 3 proc. >= 250. Pas brzegowy 4 proc. w calosci >= 252 (margines, nic
ucietego krawedzia, cien nie dochodzi do brzegu).
Uzycie: python bramka-tla.py <plik.jpg> [...]   (kod wyjscia 1, gdy ktorys plik nie przechodzi)
"""
import sys, json
import numpy as np, cv2
from PIL import Image


def zmierz(src, N=24):
    im = src if isinstance(src, Image.Image) else Image.open(src)
    a = np.asarray(im.convert("RGB")).astype(np.int32); h, w, _ = a.shape
    L = a.min(2); neu = (a.max(2) - L) <= 14
    n, lab = cv2.connectedComponents((neu & (L >= 170)).astype(np.uint8), connectivity=4)
    b = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])); tlo = np.isin(lab, b[b > 0])
    Lf = L.astype(np.float32); sr = cv2.blur(Lf, (15, 15))
    gladkie = np.sqrt(np.maximum(cv2.blur(Lf * Lf, (15, 15)) - sr * sr, 0)) < 2.0
    # szare tlo/cien/smuga = gladkie (bez faktury) neutralne piksele tla ponizej 250; kontur i faktura produktu
    # (biale futro, srebrne haczyki) nie sa gladkie, wiec nie licza sie jako cien
    szare = tlo & (L < 250) & gladkie
    zle = pola = 0
    for i in range(N):
        for j in range(N):
            y0, y1, x0, x1 = i * h // N, (i + 1) * h // N, j * w // N, (j + 1) * w // N
            m = tlo[y0:y1, x0:x1]
            if m.mean() < 0.6: continue
            pola += 1
            if szare[y0:y1, x0:x1].mean() > 0.05: zle += 1
    k = int(.03 * min(h, w))
    rog = int(min(L[:k, :k].min(), L[:k, -k:].min(), L[-k:, :k].min(), L[-k:, -k:].min()))
    # 27.10.2026 (cien i produkt uciete krawedzia kadru): pas brzegowy 4 proc. w 100 proc. >= 252
    # we wszystkich kanalach, czyli kazdy skladnik w calosci z marginesem i nic nie dochodzi do krawedzi.
    m4 = max(1, int(.04 * min(h, w)))
    pas = np.ones((h, w), bool); pas[m4:h - m4, m4:w - m4] = False
    brzeg_zle = int((pas & (L < 252)).sum())
    return {"pola": pola, "zle": zle, "rog_min": rog, "brzeg_zle_px": brzeg_zle,
            "ok": zle == 0 and rog >= 250 and brzeg_zle == 0}


if __name__ == "__main__":
    R = {f: zmierz(f) for f in sys.argv[1:]}
    print(json.dumps(R, indent=1))
    sys.exit(0 if all(v["ok"] for v in R.values()) else 1)
