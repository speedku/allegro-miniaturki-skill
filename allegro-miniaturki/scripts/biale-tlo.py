# -*- coding: utf-8 -*-
"""Tlo miniaturki Allegro do idealnej bieli FFFFFF.

Bieli jasne, neutralne i GLADKIE piksele tla polaczone z krawedzia kadru oraz zamkniete kieszenie tla
(np. miedzy drucikami karuzeli). Do tla idzie tylko to, co ma co najmniej 248 (tlo z generatora 250-254):
nizej zostaje cien kontaktowy i jasny produkt (bialy korek, gabka, wlosie). Pas 3 proc. przy krawedzi
kadru dochodzi plynnie do czystej bieli, bo miekki cien kartonu potrafi siegnac krawedzi.

Na koniec mierzy margines produktu od krawedzi. Linia "PRZYCIETE" oznacza, ze cos dotyka
krawedzi kadru: taki kadr odrzucasz, bo dobielanie nie odtworzy uciętego fragmentu.

Uzycie: python scripts/biale-tlo.py <wejscie.jpg> <wyjscie.jpg>
"""
import sys
import numpy as np, cv2
from PIL import Image

PROG_TLA, BIEL_OD = 248.0, 252.0   # tlo z generatora ma 250-254; ponizej 248 zostaje (cien, jasny produkt)
MIN_MARGINES = 12          # px przy 2000; mniej = produkt dotyka krawedzi (odrzuc)
GLADKOSC = 2.5             # lokalny rozrzut jasnosci (okno 7x7): tlo < 1, faktura wlosia/gabki wiecej
CIASNY_MARGINES = 40      # px przy 2000; mniej = nieprzyciete, ale ciasno (przyjety wzorzec: 43)

src, out = sys.argv[1], sys.argv[2]
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
H, W, _ = a.shape
L = a.min(axis=2)
neutral = (a.max(axis=2) - L) <= 5    # tlo z generatora ma rozrzut 0-3, kremowy karton ok. 9-14
# Tlo z generatora jest GLADKIE, a biale wlosie szczotek czy gabka maja fakture. Bez tego warunku
# jasne, neutralne wlosie szlo do bieli razem z tlem i zostawaly poszarpane laty.
sr = cv2.blur(L, (7, 7)); gladkie = np.sqrt(np.maximum(cv2.blur(L * L, (7, 7)) - sr * sr, 0)) < GLADKOSC
# Do tla idzie tylko to, co juz jest prawie biale (>= PROG_TLA). Przy progu 200 gladki bialy produkt
# (np. korek) laczyl sie z tlem i tracil kwadratowe laty z brzegu; cienie ponizej progu zostaja.
kand = (neutral & (L >= PROG_TLA) & gladkie).astype(np.uint8)
n, lab = cv2.connectedComponents(kand, connectivity=4)
brzeg = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
tlo = np.isin(lab, brzeg[brzeg > 0])
# zamkniete kieszenie tla (miedzy drucikami, szpary miedzy bryla a bryla): jasne i neutralne w calosci
for i in range(1, n):
    m = lab == i
    if m.sum() >= 40 and L[m].mean() >= 246:
        tlo |= m

t = np.clip((L - PROG_TLA) / (BIEL_OD - PROG_TLA), 0, 1)
# twarda biel w pierwszych 16 px (pelne bloki 8x8 JPEG, inaczej kompresja oddaje 254), dalej
# plynne przejscie do 3 proc. boku kadru
twardo, pas = 16, int(round(min(H, W) * 0.03))
yy, xx = np.mgrid[0:H, 0:W]
d = np.minimum(np.minimum(yy, H - 1 - yy), np.minimum(xx, W - 1 - xx)).astype(np.float32)
brzegowy = np.clip(1 - (d - twardo) / (pas - twardo), 0, 1)
t = np.maximum(t, brzegowy)[..., None]
# pas przy krawedzi obejmuje tez jasny neutralny cien ponizej progu tla, inaczej siega ramki na szaro
tlo = tlo | ((brzegowy > 0) & neutral & (L >= 200))
wyn = np.where(tlo[..., None], a + (255 - a) * t, a)
Image.fromarray(np.clip(wyn + 0.5, 0, 255).astype(np.uint8)).save(out, quality=95, subsampling=0)

b = np.asarray(Image.open(out).convert("RGB")).astype(int)
ramka = np.concatenate([b[:4].reshape(-1, 3), b[-4:].reshape(-1, 3), b[:, :4].reshape(-1, 3), b[:, -4:].reshape(-1, 3)])
print("ramka: min", ramka.min(), "udzial 255:", round((ramka.min(axis=1) == 255).mean() * 100, 2), "%")

# margines: wszystko, co nie jest tlem i jest wyraznie ciemniejsze od bieli (bez rogu ze znakiem ai)
obiekt = (~tlo) & (L < 235)
obiekt[: int(H * 0.08), int(W * 0.90):] = False
ys, xs = np.nonzero(obiekt)
if len(xs):
    mg = {"lewo": xs.min(), "prawo": W - 1 - xs.max(), "gora": ys.min(), "dol": H - 1 - ys.max()}
    mg = {k: int(v) for k, v in mg.items()}
    zle = [k for k, v in mg.items() if v < MIN_MARGINES * W / 2000]
    if ramka.min() < 200 and not zle:
        zle = ["ramka"]   # cos ciemnego na samej krawedzi, np. rog kartonu schowany pod znakiem ai
    ciasno = [k for k, v in mg.items() if v < CIASNY_MARGINES * W / 2000 and k not in zle]
    print("margines px:", mg, ("PRZYCIETE: " + ", ".join(zle)) if zle
          else ("CIASNO: " + ", ".join(ciasno)) if ciasno else "OK")
