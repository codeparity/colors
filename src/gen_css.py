#!/usr/bin/env python3
"""Generate CSS custom properties for the Codeparity web theme from
palette.json. Light is the default :root; dark applies both automatically
(prefers-color-scheme) and via an explicit [data-theme] override so sites
can offer a manual toggle."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
palette = json.loads((ROOT / "src" / "palette.json").read_text())
OUT = ROOT / "dist" / "web"
OUT.mkdir(parents=True, exist_ok=True)


def block(mode):
    p = palette[mode]
    a, ad = p["accent"], p["accent_dim"]
    return f"""  --cp-bg: {p['bg']};
  --cp-bg-elevated: {p['bg0_h']};
  --cp-bg-soft: {p['bg_soft']};
  --cp-bg-panel: {p['bg1']};
  --cp-bg-selection: {p['bg2']};
  --cp-border: {p['bg3']};
  --cp-border-strong: {p['bg4']};

  --cp-text-strong: {p['fg0']};
  --cp-text: {p['fg']};
  --cp-text-soft: {p['fg2']};
  --cp-text-muted: {p['fg3']};
  --cp-text-subtle: {p['fg4']};
  --cp-comment: {p['gray']};

  --cp-red: {a['red']};
  --cp-green: {a['green']};
  --cp-yellow: {a['yellow']};
  --cp-blue: {a['blue']};
  --cp-purple: {a['purple']};
  --cp-aqua: {a['aqua']};
  --cp-orange: {a['orange']};
  --cp-teal: {a['teal']};

  --cp-red-dim: {ad['red']};
  --cp-green-dim: {ad['green']};
  --cp-yellow-dim: {ad['yellow']};
  --cp-blue-dim: {ad['blue']};
  --cp-purple-dim: {ad['purple']};
  --cp-aqua-dim: {ad['aqua']};
  --cp-orange-dim: {ad['orange']};
  --cp-teal-dim: {ad['teal']};

  /* semantic aliases */
  --cp-link: var(--cp-teal);
  --cp-success: var(--cp-green);
  --cp-warning: var(--cp-yellow);
  --cp-danger: var(--cp-red);
  --cp-info: var(--cp-blue);
  --cp-focus-ring: var(--cp-teal);"""


css = f"""/*
 * Codeparity color theme — web (CSS custom properties)
 * Seed: SeedColors Dark (medium contrast). WCAG-AA verified text/accent
 * contrast per theme (see src/check_contrast.py in the source bundle).
 *
 * Usage:
 *   - Light is the default (:root).
 *   - Dark applies automatically when the OS is in dark mode.
 *   - Add data-theme="dark" or data-theme="light" on <html> (or any
 *     ancestor) to force a theme regardless of OS preference.
 */

:root {{
{block('light')}
}}

@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
{block('dark')}
  }}
}}

:root[data-theme="dark"] {{
{block('dark')}
}}

:root[data-theme="light"] {{
{block('light')}
}}

body {{
  background: var(--cp-bg);
  color: var(--cp-text);
}}
"""

(OUT / "codeparity.css").write_text(css)
print("wrote dist/web/codeparity.css")
