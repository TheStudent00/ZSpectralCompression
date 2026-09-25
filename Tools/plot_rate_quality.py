#!/usr/bin/env python3
"""plot_rate_quality -- draw WORKDIR/results.json from video_vs_mp4.py as one
figure: compressed size (across) against closeness to the original (up).

usage:
    python3 Tools/plot_rate_quality.py WORKDIR
"""
import json, sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG, FG, GRID = "#12151c", "#dfe6f0", "#2b3240"
plt.rcParams.update({"figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
                     "text.color": FG, "axes.labelcolor": FG, "xtick.color": FG,
                     "ytick.color": FG, "axes.edgecolor": GRID, "grid.color": GRID,
                     "axes.titlecolor": FG, "font.size": 10})

work = Path(sys.argv[1])
res = json.loads((work / "results.json").read_text())
rows = res["rows"]
T, V, H = res["shape_time_vertical_horizontal"]

lossy_h264 = [r for r in rows if r["group"] == "lossy" and r["method"].startswith("H.264")]
lossy_zsc = [r for r in rows if r["group"] == "lossy" and r["method"].startswith("ZSC")]
lossless = [r for r in rows if r["group"] == "lossless" and not r["method"].startswith("raw")]

top = max(r["psnr"] for r in lossy_h264 + lossy_zsc) + 3.0      # the lossless band sits above
fig, ax = plt.subplots(figsize=(11, 6.2))

def kb(r):
    return r["bytes"] / 1024.0

ax.plot([kb(r) for r in lossy_h264], [r["psnr"] for r in lossy_h264], "o-",
        color="#7fb2ff", lw=2, ms=7, label="H.264 in .mp4 (lossy)")
for r in lossy_h264:
    ax.annotate(r["method"].split(",")[0].replace("H.264 ", ""), (kb(r), r["psnr"]),
                textcoords="offset points", xytext=(6, -12), color="#7fb2ff", fontsize=9)
ax.plot([kb(r) for r in lossy_zsc], [r["psnr"] for r in lossy_zsc], "s-",
        color="#ff6b8a", lw=2, ms=7, label="ZSC lossy (the prototype)")
for i, r in enumerate(sorted(lossy_zsc, key=kb)):
    ax.annotate("threshold " + r["method"].split("threshold ")[1], (kb(r), r["psnr"]),
                textcoords="offset points", xytext=(8, -14) if i % 2 else (-10, 8),
                ha="left" if i % 2 else "right", color="#ff6b8a", fontsize=9)

colors = {"xz": "#9aa5b4", "FFV1": "#9aa5b4", "H.264": "#7fb2ff", "ZSC": "#ffb454"}
short = {"xz -9 on the raw frames": "xz -9", "FFV1, .mkv (a lossless video codec)": "FFV1 .mkv",
         "H.264 lossless, .mp4": "H.264 lossless .mp4",
         "ZSC lossless, addressable": "ZSC addressable", "ZSC lossless, sequential": "ZSC sequential"}
for i, r in enumerate(sorted(lossless, key=kb)):
    c = next(v for k, v in colors.items() if r["method"].startswith(k))
    ax.plot(kb(r), top, "D", color=c, ms=9)
    ax.annotate(short.get(r["method"], r["method"]), (kb(r), top), textcoords="offset points",
                xytext=(0, 9), ha="center", va="bottom", rotation=90, color=c, fontsize=9)
ax.axhline(top - 1.5, color=GRID, lw=1, ls="--")
ax.text(11, top - 1.2,
        "above this line: every pixel comes back (lossless)", color=FG, fontsize=9)

ax.set_xscale("log")
ticks = [10, 20, 50, 100, 200, 500, 1000, 2000]
ax.set_xticks(ticks); ax.set_xticklabels([str(t) for t in ticks]); ax.minorticks_off()
ax.set_xlabel("compressed size, KB  (log scale; raw frames are %d KB)" % (T * V * H / 1024))
ax.set_ylabel("closeness to the original, PSNR in dB  (higher = closer)")
ax.set_ylim(min(r["psnr"] for r in lossy_h264) - 2, top + 13)
ax.grid(alpha=0.3, which="both")
ax.legend(facecolor=BG, edgecolor=GRID, labelcolor=FG, loc="lower right")
ax.set_title("One real clip, %d frames of %dx%d brightness: size against quality\n"
             "better is up and to the left" % (T, H, V), fontsize=11)
fig.text(0.01, 0.005, "Shows each method's file size against how close its result is to the "
         "original. It does not show how the video looks to an eye, or how fast each method is.",
         fontsize=8.5, color="#9aa5b4")
fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig(work / "rate_quality.png", dpi=110)
print("wrote", work / "rate_quality.png")
