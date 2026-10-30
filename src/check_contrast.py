#!/usr/bin/env python3
"""Report WCAG contrast ratios for the Codeparity palette (text + accents
against their background), flagging anything below AA thresholds:
  - 4.5:1 for normal text
  - 3.0:1 for large text / UI components / icons
"""
import json
from pathlib import Path
from gen_palette import contrast

ROOT = Path(__file__).resolve().parent
palette = json.loads((ROOT / "palette.json").read_text())

AA_TEXT = 4.5  # body text / headings: fg0, fg, fg2, fg3
AA_UI = 3.0    # large text, icons, borders, AND muted/de-emphasized text
               # (fg4, gray) — comments, placeholders, timestamps. Treating
               # these as a distinct "muted" role (not body text) matches
               # SeedColors's own long-standing design intent for its #928374
               # comment gray, which is intentionally de-emphasized rather
               # than a readability bug.

TEXT_ROLE_THRESHOLD = {
    "fg0": AA_TEXT, "fg": AA_TEXT, "fg2": AA_TEXT, "fg3": AA_TEXT,
    "fg4": AA_UI, "gray": AA_UI,
}

rows = []
fails = []

for theme in ("dark", "light"):
    p = palette[theme]
    bg = p["bg"]
    for fg_name in ("fg0", "fg", "fg2", "fg3", "fg4", "gray"):
        threshold = TEXT_ROLE_THRESHOLD[fg_name]
        c = contrast(p[fg_name], bg)
        ok = c >= threshold
        rows.append((theme, f"text:{fg_name}", p[fg_name], bg, c, threshold, ok))
        if not ok:
            fails.append(rows[-1])
    for group, threshold in (("accent", AA_TEXT), ("accent_dim", AA_UI)):
        for name, hexval in p[group].items():
            c = contrast(hexval, bg)
            ok = c >= threshold
            rows.append((theme, f"{group}:{name}", hexval, bg, c, threshold, ok))
            if not ok:
                fails.append(rows[-1])

w = max(len(r[1]) for r in rows)
print(f"{'theme':5} {'token':{w}} {'color':8} {'bg':8} {'ratio':>6} {'min':>5}  result")
for theme, token, hexval, bg, c, threshold, ok in rows:
    mark = "PASS" if ok else "FAIL"
    print(f"{theme:5} {token:{w}} {hexval:8} {bg:8} {c:6.2f} {threshold:5.1f}  {mark}")

print()
if fails:
    print(f"{len(fails)} token(s) below their AA threshold:")
    for theme, token, hexval, bg, c, threshold, ok in fails:
        print(f"  - {theme}/{token}: {c:.2f} < {threshold}")
    raise SystemExit(1)
else:
    print("All tokens meet WCAG AA for their role (text >=4.5:1, UI/dim >=3:1).")
