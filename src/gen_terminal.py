#!/usr/bin/env python3
"""Generate terminal theme files (Alacritty, Kitty, Windows Terminal, and a
generic ANSI/true-color spec doc) from palette.json, for both Codeparity
Dark and Codeparity Light."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
palette = json.loads((ROOT / "src" / "palette.json").read_text())
OUT = ROOT / "dist" / "terminal"
OUT.mkdir(parents=True, exist_ok=True)


def ansi16(p, mode):
    a, ad = p["accent"], p["accent_dim"]
    if mode == "dark":
        black, bright_black = p["bg1"], p["gray"]
        white, bright_white = p["fg4"], p["fg0"]
    else:
        black, bright_black = p["fg"], p["gray"]
        white, bright_white = p["bg3"], p["bg0_h"]
    return {
        "black": black, "red": ad["red"], "green": ad["green"], "yellow": ad["yellow"],
        "blue": ad["blue"], "magenta": ad["purple"], "cyan": ad["aqua"], "white": white,
        "bright_black": bright_black, "bright_red": a["red"], "bright_green": a["green"],
        "bright_yellow": a["yellow"], "bright_blue": a["blue"], "bright_magenta": a["purple"],
        "bright_cyan": a["aqua"], "bright_white": bright_white,
    }


def build(mode):
    p = palette[mode]
    c = ansi16(p, mode)
    return {
        "name": f"Codeparity {mode.capitalize()}",
        "background": p["bg"],
        "foreground": p["fg"],
        "cursor": p["accent"]["teal"],
        "cursor_text": p["bg"],
        "selection_bg": p["bg2"],
        "selection_fg": p["fg0"],
        "ansi": c,
    }


# ---------------------------------------------------------------------- #
# Alacritty (TOML, 0.13+ config schema)
# ---------------------------------------------------------------------- #
def alacritty_toml(t):
    c = t["ansi"]
    return f"""# {t['name']} — Alacritty color scheme
# Generated from the Codeparity palette (src/palette.json)

[colors.primary]
background = "{t['background']}"
foreground = "{t['foreground']}"

[colors.cursor]
text = "{t['cursor_text']}"
cursor = "{t['cursor']}"

[colors.selection]
text = "{t['selection_fg']}"
background = "{t['selection_bg']}"

[colors.normal]
black = "{c['black']}"
red = "{c['red']}"
green = "{c['green']}"
yellow = "{c['yellow']}"
blue = "{c['blue']}"
magenta = "{c['magenta']}"
cyan = "{c['cyan']}"
white = "{c['white']}"

[colors.bright]
black = "{c['bright_black']}"
red = "{c['bright_red']}"
green = "{c['bright_green']}"
yellow = "{c['bright_yellow']}"
blue = "{c['bright_blue']}"
magenta = "{c['bright_magenta']}"
cyan = "{c['bright_cyan']}"
white = "{c['bright_white']}"
"""


# ---------------------------------------------------------------------- #
# Kitty (.conf)
# ---------------------------------------------------------------------- #
def kitty_conf(t):
    c = t["ansi"]
    return f"""# {t['name']} — Kitty color scheme
# Generated from the Codeparity palette (src/palette.json)

background {t['background']}
foreground {t['foreground']}
cursor {t['cursor']}
cursor_text_color {t['cursor_text']}
selection_background {t['selection_bg']}
selection_foreground {t['selection_fg']}

# black
color0 {c['black']}
color8 {c['bright_black']}
# red
color1 {c['red']}
color9 {c['bright_red']}
# green
color2  {c['green']}
color10 {c['bright_green']}
# yellow
color3  {c['yellow']}
color11 {c['bright_yellow']}
# blue
color4  {c['blue']}
color12 {c['bright_blue']}
# magenta
color5  {c['magenta']}
color13 {c['bright_magenta']}
# cyan
color6  {c['cyan']}
color14 {c['bright_cyan']}
# white
color7  {c['white']}
color15 {c['bright_white']}
"""


# ---------------------------------------------------------------------- #
# Windows Terminal (JSON color scheme object; paste into "schemes": [...])
# ---------------------------------------------------------------------- #
def windows_terminal_json(t):
    c = t["ansi"]
    scheme = {
        "name": t["name"],
        "background": t["background"],
        "foreground": t["foreground"],
        "cursorColor": t["cursor"],
        "selectionBackground": t["selection_bg"],
        "black": c["black"], "red": c["red"], "green": c["green"], "yellow": c["yellow"],
        "blue": c["blue"], "purple": c["magenta"], "cyan": c["cyan"], "white": c["white"],
        "brightBlack": c["bright_black"], "brightRed": c["bright_red"],
        "brightGreen": c["bright_green"], "brightYellow": c["bright_yellow"],
        "brightBlue": c["bright_blue"], "brightPurple": c["bright_magenta"],
        "brightCyan": c["bright_cyan"], "brightWhite": c["bright_white"],
    }
    return json.dumps(scheme, indent=2) + "\n"


# ---------------------------------------------------------------------- #
# Generic ANSI / true-color spec (markdown) — format-agnostic reference
# ---------------------------------------------------------------------- #
def spec_md():
    lines = ["# Codeparity — ANSI & true-color spec",
             "",
             "Format-agnostic reference palette for porting Codeparity to any",
             "terminal emulator, TUI library, or syntax-highlighting scheme.",
             "Seed: SeedColors Dark (medium contrast). All text/accent colors are",
             "WCAG-AA verified against their background (see `src/check_contrast.py`).",
             ""]
    for mode in ("dark", "light"):
        t = build(mode)
        c = t["ansi"]
        p = palette[mode]
        lines += [f"## {t['name']}", "",
                  "### Base", "",
                  "| Role | Hex |", "|---|---|",
                  f"| background | `{t['background']}` |",
                  f"| foreground | `{t['foreground']}` |",
                  f"| cursor | `{t['cursor']}` |",
                  f"| selection background | `{t['selection_bg']}` |",
                  f"| selection foreground | `{t['selection_fg']}` |",
                  "",
                  "### ANSI 16", "",
                  "| # | Name | Hex | | # | Name | Hex |",
                  "|---|---|---|---|---|---|---|",
                  f"| 0 | black | `{c['black']}` | | 8 | bright black | `{c['bright_black']}` |",
                  f"| 1 | red | `{c['red']}` | | 9 | bright red | `{c['bright_red']}` |",
                  f"| 2 | green | `{c['green']}` | | 10 | bright green | `{c['bright_green']}` |",
                  f"| 3 | yellow | `{c['yellow']}` | | 11 | bright yellow | `{c['bright_yellow']}` |",
                  f"| 4 | blue | `{c['blue']}` | | 12 | bright blue | `{c['bright_blue']}` |",
                  f"| 5 | magenta | `{c['magenta']}` | | 13 | bright magenta | `{c['bright_magenta']}` |",
                  f"| 6 | cyan | `{c['cyan']}` | | 14 | bright cyan | `{c['bright_cyan']}` |",
                  f"| 7 | white | `{c['white']}` | | 15 | bright white | `{c['bright_white']}` |",
                  "",
                  "### Extended UI tokens (not in the ANSI 16, true-color only)",
                  "",
                  "| Token | Hex |", "|---|---|",
                  f"| bg0_h (deepest/elevated) | `{p['bg0_h']}` |",
                  f"| bg_soft | `{p['bg_soft']}` |",
                  f"| bg1 (panel) | `{p['bg1']}` |",
                  f"| bg2 (selection) | `{p['bg2']}` |",
                  f"| bg3 (border) | `{p['bg3']}` |",
                  f"| bg4 (border strong) | `{p['bg4']}` |",
                  f"| fg0 (heading) | `{p['fg0']}` |",
                  f"| fg2 | `{p['fg2']}` |",
                  f"| fg3 | `{p['fg3']}` |",
                  f"| fg4 (muted) | `{p['fg4']}` |",
                  f"| gray (comment) | `{p['gray']}` |",
                  f"| accent.teal (brand/link) | `{p['accent']['teal']}` |",
                  f"| accent_dim.teal | `{p['accent_dim']['teal']}` |",
                  ""]
    return "\n".join(lines)


for mode in ("dark", "light"):
    t = build(mode)
    (OUT / f"codeparity-{mode}.alacritty.toml").write_text(alacritty_toml(t))
    (OUT / f"codeparity-{mode}.kitty.conf").write_text(kitty_conf(t))
    (OUT / f"codeparity-{mode}.windows-terminal.json").write_text(windows_terminal_json(t))

(ROOT / "dist" / "spec").mkdir(parents=True, exist_ok=True)
(ROOT / "dist" / "spec" / "codeparity-ansi-spec.md").write_text(spec_md())

print("terminal files + spec written")
