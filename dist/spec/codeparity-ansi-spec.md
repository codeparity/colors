# Codeparity — ANSI & true-color spec

Format-agnostic reference palette for porting Codeparity to any
terminal emulator, TUI library, or syntax-highlighting scheme.
Seed: Gruvbox Dark (medium contrast). All text/accent colors are
WCAG-AA verified against their background (see `src/check_contrast.py`).

## Codeparity Dark

### Base

| Role | Hex |
|---|---|
| background | `#282828` |
| foreground | `#cecece` |
| cursor | `#2bb3a3` |
| selection background | `#4a4a4a` |
| selection foreground | `#e1e1e1` |

### ANSI 16

| # | Name | Hex | | # | Name | Hex |
|---|---|---|---|---|---|---|
| 0 | black | `#393939` | | 8 | bright black | `#838383` |
| 1 | red | `#e02d25` | | 9 | bright red | `#fb5744` |
| 2 | green | `#98971a` | | 10 | bright green | `#b8bb26` |
| 3 | yellow | `#d79921` | | 11 | bright yellow | `#fabd2f` |
| 4 | blue | `#458588` | | 12 | bright blue | `#83a598` |
| 5 | magenta | `#b16286` | | 13 | bright magenta | `#d3869b` |
| 6 | cyan | `#689d6a` | | 14 | bright cyan | `#8ec07c` |
| 7 | white | `#969696` | | 15 | bright white | `#e1e1e1` |

### Extended UI tokens (not in the ANSI 16, true-color only)

| Token | Hex |
|---|---|
| bg0_h (deepest/elevated) | `#1f1f1f` |
| bg_soft | `#303030` |
| bg1 (panel) | `#393939` |
| bg2 (selection) | `#4a4a4a` |
| bg3 (border) | `#5d5d5d` |
| bg4 (border strong) | `#707070` |
| fg0 (heading) | `#e1e1e1` |
| fg2 | `#bbbbbb` |
| fg3 | `#a8a8a8` |
| fg4 (muted) | `#969696` |
| gray (comment) | `#838383` |
| accent.teal (brand/link) | `#2bb3a3` |
| accent_dim.teal | `#1f8a7d` |

## Codeparity Light

### Base

| Role | Hex |
|---|---|
| background | `#f3f3f3` |
| foreground | `#323232` |
| cursor | `#0e7a73` |
| selection background | `#bcbcbc` |
| selection foreground | `#1e1e1e` |

### ANSI 16

| # | Name | Hex | | # | Name | Hex |
|---|---|---|---|---|---|---|
| 0 | black | `#323232` | | 8 | bright black | `#7a7a7a` |
| 1 | red | `#cc241d` | | 9 | bright red | `#cc241d` |
| 2 | green | `#8d8c18` | | 10 | bright green | `#727114` |
| 3 | yellow | `#b57614` | | 11 | bright yellow | `#976311` |
| 4 | blue | `#458588` | | 12 | bright blue | `#3e7779` |
| 5 | magenta | `#b16286` | | 13 | bright magenta | `#a65379` |
| 6 | cyan | `#609462` | | 14 | bright cyan | `#4e774f` |
| 7 | white | `#979797` | | 15 | bright white | `#fbfbfb` |

### Extended UI tokens (not in the ANSI 16, true-color only)

| Token | Hex |
|---|---|
| bg0_h (deepest/elevated) | `#fbfbfb` |
| bg_soft | `#e2e2e2` |
| bg1 (panel) | `#d0d0d0` |
| bg2 (selection) | `#bcbcbc` |
| bg3 (border) | `#979797` |
| bg4 (border strong) | `#7d7d7d` |
| fg0 (heading) | `#1e1e1e` |
| fg2 | `#454545` |
| fg3 | `#5b5b5b` |
| fg4 (muted) | `#707070` |
| gray (comment) | `#7a7a7a` |
| accent.teal (brand/link) | `#0e7a73` |
| accent_dim.teal | `#0e7a73` |
