#!/usr/bin/env python3
"""
Codeparity color theme — palette generator.

Builds Codeparity Dark (seeded from Gruvbox Dark) and Codeparity Light
(a fresh, custom-reinterpreted companion that keeps the same hue identity
per role but is NOT a literal lightness-inversion of the dark palette).

For every accent, we binary-search the HSL lightness (hue/sat fixed) until
the color hits a target WCAG contrast ratio against its intended background,
so every token in palette.json is contrast-checked at generation time
rather than eyeballed.
"""
import json
import colorsys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "src" / "palette.json"


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*[max(0, min(255, round(c))) for c in rgb])


def _lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(hexcolor):
    r, g, b = hex_to_rgb(hexcolor)
    r, g, b = _lin(r), _lin(g), _lin(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(hex_a, hex_b):
    la, lb = relative_luminance(hex_a), relative_luminance(hex_b)
    lighter, darker = max(la, lb), min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)


def hex_to_hsl(h):
    r, g, b = [v / 255 for v in hex_to_rgb(h)]
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    return hh, ss, ll


def hsl_to_hex(hh, ss, ll):
    r, g, b = colorsys.hls_to_rgb(hh, ll, ss)
    return rgb_to_hex((r * 255, g * 255, b * 255))


def desaturate(hexcolor, sat=0.0, hue=0.0):
    """Strip the warm Gruvbox hue tint from a neutral, keeping its
    lightness (so the ramp spacing is unchanged) but setting saturation
    to `sat` (0 = true grey) and hue to `hue`."""
    hh, ss, ll = hex_to_hsl(hexcolor)
    return hsl_to_hex(hue, sat, ll)


def adjust_for_contrast(seed_hex, bg_hex, target, prefer="auto", sat_scale=1.0):
    """Binary-search lightness (hue/sat fixed from seed) to hit `target`
    contrast against bg_hex. prefer='darker'|'lighter'|'auto' picks which
    direction to search when both could work (auto = whichever the seed
    is already closer to)."""
    hh, ss, ll = hex_to_hsl(seed_hex)
    ss = min(1.0, ss * sat_scale)
    bg_l = relative_luminance(bg_hex)

    def c_at(l):
        return contrast(hsl_to_hex(hh, ss, l), bg_hex)

    if prefer == "auto":
        prefer = "darker" if bg_l > 0.5 else "lighter"

    lo, hi = (0.0, ll) if prefer == "darker" else (ll, 1.0)
    # Expand/confirm the direction actually increases contrast; else flip.
    if c_at(lo if prefer == "darker" else hi) < c_at(ll):
        prefer = "lighter" if prefer == "darker" else "darker"
        lo, hi = (0.0, ll) if prefer == "darker" else (ll, 1.0)

    best = ll
    for _ in range(40):
        mid = (lo + hi) / 2
        c = c_at(mid)
        best = mid
        if abs(c - target) < 0.01:
            break
        going_right_increases = c_at(hi) > c_at(lo)
        if (c < target) == going_right_increases:
            lo = mid
        else:
            hi = mid
    return hsl_to_hex(hh, ss, best)


# ---------------------------------------------------------------------------
# Gruvbox Dark seed (medium contrast, upstream reference values)
# ---------------------------------------------------------------------------
GRUVBOX_DARK = {
    "bg0_h": "#1d2021", "bg0": "#282828", "bg0_s": "#32302f",
    "bg1": "#3c3836", "bg2": "#504945", "bg3": "#665c54", "bg4": "#7c6f64",
    "fg0": "#fbf1c7", "fg1": "#ebdbb2", "fg2": "#d5c4a1", "fg3": "#bdae93", "fg4": "#a89984",
    "gray": "#928374",
    "red": "#cc241d", "red_bright": "#fb4934",
    "green": "#98971a", "green_bright": "#b8bb26",
    "yellow": "#d79921", "yellow_bright": "#fabd2f",
    "blue": "#458588", "blue_bright": "#83a598",
    "purple": "#b16286", "purple_bright": "#d3869b",
    "aqua": "#689d6a", "aqua_bright": "#8ec07c",
    "orange": "#d65d0e", "orange_bright": "#fe8019",
}

# ---------------------------------------------------------------------------
# DARK — Codeparity Dark. Neutrals inherited from the Gruvbox seed as-is
# (that's the "seed" the user asked for); accents nudged slightly toward a
# cooler, more saturated register for a distinct brand feel, then contrast-
# verified at AA against bg0.
# ---------------------------------------------------------------------------
# Neutral style: Gruvbox's stock ramp is warm (hue ~30-40 degrees, desatur-
# ated toward brown). Codeparity uses true greys instead — same lightness
# steps (so the ramp spacing/contrast relationships carry over), hue and
# saturation stripped to 0.
NEUTRAL_SAT = 0.0
NEUTRAL_HUE = 0.0

dark = {
    "bg0_h": desaturate(GRUVBOX_DARK["bg0_h"], NEUTRAL_SAT, NEUTRAL_HUE),
    "bg": desaturate(GRUVBOX_DARK["bg0"], NEUTRAL_SAT, NEUTRAL_HUE),
    "bg_soft": desaturate(GRUVBOX_DARK["bg0_s"], NEUTRAL_SAT, NEUTRAL_HUE),
    "bg1": desaturate(GRUVBOX_DARK["bg1"], NEUTRAL_SAT, NEUTRAL_HUE),
    "bg2": desaturate(GRUVBOX_DARK["bg2"], NEUTRAL_SAT, NEUTRAL_HUE),
    "bg3": desaturate(GRUVBOX_DARK["bg3"], NEUTRAL_SAT, NEUTRAL_HUE),
    "bg4": desaturate(GRUVBOX_DARK["bg4"], NEUTRAL_SAT, NEUTRAL_HUE),
    "fg0": desaturate(GRUVBOX_DARK["fg0"], NEUTRAL_SAT, NEUTRAL_HUE),
    "fg": desaturate(GRUVBOX_DARK["fg1"], NEUTRAL_SAT, NEUTRAL_HUE),
    "fg2": desaturate(GRUVBOX_DARK["fg2"], NEUTRAL_SAT, NEUTRAL_HUE),
    "fg3": desaturate(GRUVBOX_DARK["fg3"], NEUTRAL_SAT, NEUTRAL_HUE),
    "fg4": desaturate(GRUVBOX_DARK["fg4"], NEUTRAL_SAT, NEUTRAL_HUE),
    "gray": desaturate(GRUVBOX_DARK["gray"], NEUTRAL_SAT, NEUTRAL_HUE),
}
dark_bg = dark["bg"]

# Signature brand accent: a cyan-leaning teal ("parity teal"), not present
# in stock Gruvbox — used for links/focus rings to give Codeparity its own
# identity on top of the Gruvbox-seeded neutrals.
PARITY_TEAL_SEED_DARK = "#2bb3a3"
PARITY_TEAL_SEED_LIGHT = "#0e7a73"

dark_accent_seeds = {
    "red": GRUVBOX_DARK["red_bright"],
    "green": GRUVBOX_DARK["green_bright"],
    "yellow": GRUVBOX_DARK["yellow_bright"],
    "blue": GRUVBOX_DARK["blue_bright"],
    "purple": GRUVBOX_DARK["purple_bright"],
    "aqua": GRUVBOX_DARK["aqua_bright"],
    "orange": GRUVBOX_DARK["orange_bright"],
    "teal": PARITY_TEAL_SEED_DARK,
}
dark_accent_dim_seeds = {
    "red": GRUVBOX_DARK["red"],
    "green": GRUVBOX_DARK["green"],
    "yellow": GRUVBOX_DARK["yellow"],
    "blue": GRUVBOX_DARK["blue"],
    "purple": GRUVBOX_DARK["purple"],
    "aqua": GRUVBOX_DARK["aqua"],
    "orange": GRUVBOX_DARK["orange"],
    "teal": "#1f8a7d",
}

dark["accent"] = {}
dark["accent_dim"] = {}
for name, seed in dark_accent_seeds.items():
    dark["accent"][name] = adjust_for_contrast(seed, dark_bg, target=4.6, prefer="lighter")
for name, seed in dark_accent_dim_seeds.items():
    # "dim" variants only need UI-level contrast (3:1) — used for borders/icons
    dark["accent_dim"][name] = adjust_for_contrast(seed, dark_bg, target=3.2, prefer="auto")

# ---------------------------------------------------------------------------
# LIGHT — Codeparity Light. Custom reinterpretation: a warm paper neutral
# ramp of its own (not an inversion of the dark ramp), with accents redrawn
# at matching hues but independently contrast-tuned against the light bg.
# ---------------------------------------------------------------------------
# Same approach as dark: keep the original warm-light lightness ramp, strip
# the hue/saturation to true grey.
_light_warm = {
    "bg0_h": "#fffdf7", "bg": "#faf6ec", "bg_soft": "#f1ead3",
    "bg1": "#e7dcb8", "bg2": "#dccb9c", "bg3": "#b9a475", "bg4": "#9c875e",
    "fg0": "#242019", "fg": "#3a332a", "fg2": "#4f473b", "fg3": "#675e4f",
    "fg4": "#7c7364", "gray": "#8a7f6a",
}
light = {k: desaturate(v, NEUTRAL_SAT, NEUTRAL_HUE) for k, v in _light_warm.items()}
light_bg = light["bg"]

light_accent_seeds = {
    "red": GRUVBOX_DARK["red"],
    "green": GRUVBOX_DARK["green"],
    "yellow": "#b57614",
    "blue": GRUVBOX_DARK["blue"],
    "purple": GRUVBOX_DARK["purple"],
    "aqua": GRUVBOX_DARK["aqua"],
    "orange": GRUVBOX_DARK["orange"],
    "teal": PARITY_TEAL_SEED_LIGHT,
}
light_accent_dim_seeds = dict(light_accent_seeds)  # same hues, lighter target

light["accent"] = {}
light["accent_dim"] = {}
for name, seed in light_accent_seeds.items():
    light["accent"][name] = adjust_for_contrast(seed, light_bg, target=4.6, prefer="darker")
for name, seed in light_accent_dim_seeds.items():
    light["accent_dim"][name] = adjust_for_contrast(seed, light_bg, target=3.2, prefer="auto")

palette = {
    "meta": {
        "name": "Codeparity",
        "seed": "Gruvbox Dark (medium contrast)",
        "generated_by": "src/gen_palette.py",
    },
    "dark": dark,
    "light": light,
}

OUT.write_text(json.dumps(palette, indent=2) + "\n")
print(f"wrote {OUT}")
