"""Génère src/france.json : contours SVG simplifiés des départements de métropole
(source : app/assets/departements-avec-outre-mer.geojson, IGN/Etalab), projetés
dans une boîte 1000x1000 (équirectangulaire, cos 46,5°)."""
import json, math, sys
src, dst = sys.argv[1], sys.argv[2]
g = json.load(open(src, encoding="utf-8"))
K = math.cos(math.radians(46.5))
feats = []
for f in g["features"]:
    code = str(f["properties"].get("code", ""))
    if code.startswith("97"):
        continue
    polys = f["geometry"]["coordinates"] if f["geometry"]["type"] == "MultiPolygon" else [f["geometry"]["coordinates"]]
    feats.append((code, f["properties"].get("nom", ""), polys))
xs = [p[0] * K for _, _, ps in feats for poly in ps for p in poly[0]]
ys = [-p[1] for _, _, ps in feats for poly in ps for p in poly[0]]
x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
s = 1000 / max(x1 - x0, y1 - y0)
ox, oy = (1000 - (x1 - x0) * s) / 2, (1000 - (y1 - y0) * s) / 2
def proj(p):
    return ((p[0] * K - x0) * s + ox, (-p[1] - y0) * s + oy)
def simplify(pts, tol=1.2):
    out = [pts[0]]
    for q in pts[1:]:
        if math.dist(q, out[-1]) >= tol:
            out.append(q)
    return out
out = []
for code, nom, polys in feats:
    d = ""
    for poly in polys:
        pts = simplify([proj(p) for p in poly[0]])
        if len(pts) < 4:
            continue
        d += "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"
    out.append({"code": code, "nom": nom, "d": d})
json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False)
print(len(out), "départements")
