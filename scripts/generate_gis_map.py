"""
Generate High-Resolution GIS Urban Transit Map from KML.
Project: Bahawalpur Main Transportation Routes & Urban Infrastructure Planning
Author: Muhammad Umer Basit (Regn No. 259084, Section C)
"""

import os
import xml.etree.ElementTree as ET
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
kml_file = os.path.join(base_dir, "gis", "bahawalpur_transportation_planning.kml")
media_dir = os.path.join(base_dir, "media")
os.makedirs(media_dir, exist_ok=True)

tree = ET.parse(kml_file)
root = tree.getroot()
ns = {"kml": "http://www.opengis.net/kml/2.2"}

lines = []
points = []

for placemark in root.findall(".//kml:Placemark", ns):
    name_el = placemark.find("kml:name", ns)
    name = name_el.text if name_el is not None else ""

    # Check LineString
    ls = placemark.find(".//kml:LineString/kml:coordinates", ns)
    if ls is not None and ls.text:
        coords = []
        for pair in ls.text.strip().split():
            parts = pair.split(",")
            if len(parts) >= 2:
                coords.append((float(parts[0]), float(parts[1])))
        if coords:
            lines.append((name, coords))

    # Check Point
    pt = placemark.find(".//kml:Point/kml:coordinates", ns)
    if pt is not None and pt.text:
        parts = pt.text.strip().split(",")
        if len(parts) >= 2:
            points.append((name, float(parts[0]), float(parts[1])))

print(f"Extracted {len(lines)} transit corridors and {len(points)} landmark nodes.")

fig, ax = plt.subplots(figsize=(14, 10), facecolor="#0f172a")
ax.set_facecolor("#0f172a")

# Distinct vibrant colors for transportation corridors
colors = [
    "#38bdf8", "#4ade80", "#f43f5e", "#fbbf24", "#a855f7",
    "#ec4899", "#06b6d4", "#f97316", "#14b8a6", "#eab308"
]

for i, (r_name, coords) in enumerate(lines):
    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]
    c = colors[i % len(colors)]
    ax.plot(xs, ys, color=c, linewidth=2.8, alpha=0.9, zorder=3)

# Plot landmark nodes
pxs = [p[1] for p in points]
pys = [p[2] for p in points]
ax.scatter(pxs, pys, color="#fbbf24", edgecolor="#ffffff", s=45, zorder=5, alpha=0.95, label="Urban Node / Terminal")

# Annotate prominent urban landmarks in Bahawalpur
key_keywords = [
    "Railway Station", "Fawara Chowk", "Daewoo", "Noor Mahal",
    "Fareed Gate", "Library", "DC Chowk", "University", "Hospital", "Airport"
]
annotated = 0
for name, x, y in points:
    if any(k.lower() in name.lower() for k in key_keywords) and annotated < 14:
        clean_name = name.split(",")[0].strip()
        ax.annotate(
            clean_name, (x, y), xytext=(8, 8), textcoords="offset points",
            color="#f8fafc", fontsize=8.5, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.25", fc="#1e293b", ec="#38bdf8", alpha=0.88),
            zorder=10
        )
        annotated += 1

ax.set_title(
    "Bahawalpur Urban Transportation & Transit Network Planning\n"
    "By: Muhammad Umer Basit (Regn No. 259084, Section C)",
    fontsize=14, color="#f8fafc", fontweight="bold", pad=15
)
ax.set_xlabel("Longitude (°E)", fontsize=11, color="#94a3b8")
ax.set_ylabel("Latitude (°N)", fontsize=11, color="#94a3b8")
ax.tick_params(colors="#94a3b8")
ax.grid(True, linestyle="--", alpha=0.25, color="#475569")

# Attribution label in plot
ax.text(
    0.02, 0.03, "Source: Google My Maps GIS Dataset | ARCH-305 Architecture & Town Planning",
    transform=ax.transAxes, color="#64748b", fontsize=9, style="italic"
)

out_img = os.path.join(media_dir, "bahawalpur-urban-transit-map.png")
plt.tight_layout()
plt.savefig(out_img, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()
print(f"Saved GIS Transit Map to: {out_img}")
