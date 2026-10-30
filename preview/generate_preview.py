#!/usr/bin/env python3
"""Build a side-by-side light and dark palette preview from palette.json."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PALETTE = ROOT.parent / "palette.json"
TOKENS = json.loads(PALETTE.read_text())


def make_theme(name, colors):
    swatches = "".join(
        f'<div class="swatch"><span style="background:{value}"></span>'
        f'<b>{escape(key)}</b><code>{escape(value)}</code></div>'
        for key, value in colors.items()
    )
    return f'''<section class="theme {name}">
      <header class="theme-head"><div><p class="eyebrow">CODEPARITY / {name.upper()}</p>
      <h2>{name.title()} mode</h2><p class="muted">A preview of the full {name} palette.</p></div>
      <span class="mode-pill">{name}</span></header>
      <div class="workspace"><nav class="rail"><b>CP</b><span class="active">◈</span><span>⌕</span><span>⚙</span></nav>
      <div class="content"><div class="crumb muted">Workspace <span>/</span> Appearance</div>
        <div class="panel intro-panel"><p class="eyebrow accent">COLOR &amp; TYPE</p>
          <h1>A calmer place<br>to focus.</h1>
          <p class="body-copy">Warm, balanced surfaces and carefully tuned accents make long sessions easier to settle into.</p>
          <div class="actions"><button class="primary">Apply theme</button><button class="secondary">Learn more</button></div>
        </div>
        <div class="cards"><article class="panel small-card"><p class="eyebrow muted">CURRENT THEME</p><h3>CodeParity</h3>
          <p class="muted">Muted Gruvbox accents</p><div class="mini-swatches"><i></i><i></i><i></i><i></i><i></i></div></article>
          <article class="panel small-card"><p class="eyebrow muted">STATUS</p><div class="status"><span></span> Ready to focus</div>
          <p class="muted">Your preferences are up to date.</p><div class="progress"><i></i></div></article>
        </div>
        <div class="panel selection"><span class="selection-mark">✓</span><div><b>Selected item</b><p class="muted">Selection and secondary surface colors</p></div><kbd>⌘ K</kbd></div>
        <div class="terminal"><div class="terminal-head"><span><i></i><i></i><i></i></span><b>~/workspace — preview</b><em>•••</em></div>
          <pre><span class="term-dim">$</span> cat theme.toml
<span class="term-key">name</span> = <span class="term-string">"CodeParity"</span>
<span class="term-key">background</span> = <span class="term-string">"{colors['bg0']}"</span>
<span class="term-key">foreground</span> = <span class="term-string">"{colors['fg']}"</span>
<span class="term-key">accent</span> = <span class="term-accent">"{colors['blue']}"</span>

<span class="term-dim"># A softer palette for focused work</span>
<span class="term-green">✓ Theme loaded successfully</span></pre></div>
        <div class="palette"><p class="eyebrow muted">PALETTE TOKENS</p><div class="swatches">{swatches}</div></div>
      </div></div>
    </section>'''


themes = "".join(make_theme(name, colors) for name, colors in TOKENS.items() if name in ("dark", "light"))
theme_vars = "\n".join(
    f'.{name}{{' + "".join(f"--{key}:{value};" for key, value in colors.items()) + "}"
    for name, colors in TOKENS.items() if name in ("dark", "light")
)
page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CodeParity · Palette preview</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#17191c;color:#ece9e1;font:14px/1.55 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
main{{max-width:1440px;margin:auto;padding:38px 28px 56px}}.page-head{{display:flex;align-items:end;justify-content:space-between;gap:24px;margin-bottom:24px}}
h1{{font-size:28px;line-height:1.1;margin:0 0 8px;letter-spacing:-.04em}}.page-head p{{margin:0;color:#a89984}}.legend{{color:#a89984;font-size:12px}}.themes{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;align-items:start}}
.theme{{--bg0:#181818;--bg1:#1e1e1e;--bg2:#2a2a2a;--bg3:#3a3a3a;--fg:#ebdbb2;--fgDim:#a89984;--red:#fb4934;--green:#b8bb26;--yellow:#928374;--blue:#83a598;--purple:#d3869b;--aqua:#8ec07c;--orange:#fe8019;background:var(--bg0);color:var(--fg);border:1px solid var(--bg3);border-radius:14px;overflow:hidden;box-shadow:0 16px 40px #0003}}
.theme-head{{padding:20px 22px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--bg2)}}.eyebrow{{font-size:10px;letter-spacing:.12em;font-weight:700;margin:0 0 8px}}.theme-head h2{{font-size:20px;margin:0;letter-spacing:-.03em}}.muted{{color:var(--fgDim)}}.theme-head .muted{{margin:4px 0 0;font-size:12px}}.mode-pill{{border:1px solid var(--bg3);border-radius:99px;padding:5px 10px;color:var(--fgDim);font-size:11px;text-transform:uppercase;letter-spacing:.08em}}
.workspace{{display:grid;grid-template-columns:46px 1fr;min-height:640px}}.rail{{background:var(--bg1);border-right:1px solid var(--bg2);display:flex;align-items:center;flex-direction:column;gap:18px;padding:16px 0;color:var(--fgDim)}}.rail b{{font-size:12px;color:var(--blue);margin-bottom:10px}}.rail span{{height:28px;width:28px;display:grid;place-items:center;border-radius:7px}}.rail .active{{background:var(--bg3);color:var(--yellow)}}.content{{padding:18px;min-width:0}}.crumb{{font-size:11px;margin-bottom:15px}}.crumb span{{padding:0 6px;color:var(--bg3)}}.panel{{background:var(--bg1);border:1px solid var(--bg2);border-radius:10px}}
.intro-panel{{padding:20px 21px 18px;background:linear-gradient(135deg,var(--bg1),var(--bg0))}}.accent{{color:var(--aqua)}}.intro-panel h1{{font-size:30px;line-height:1.05;letter-spacing:-.045em;margin:0 0 12px}}.body-copy{{font-size:12px;line-height:1.65;color:var(--fgDim);max-width:330px;margin:0 0 16px}}.actions{{display:flex;gap:8px}}button{{border:0;border-radius:6px;padding:8px 11px;font:600 11px system-ui}}.primary{{background:var(--blue);color:var(--bg0)}}.secondary{{background:var(--bg2);color:var(--fg)}}
.cards{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px}}.small-card{{padding:13px;min-height:106px}}.small-card h3{{font-size:15px;margin:0 0 2px}}.small-card p{{font-size:10px;margin:0 0 10px}}.mini-swatches{{display:flex;gap:5px}}.mini-swatches i{{width:17px;height:17px;border-radius:50%;background:var(--red)}}.mini-swatches i:nth-child(2){{background:var(--green)}}.mini-swatches i:nth-child(3){{background:var(--yellow)}}.mini-swatches i:nth-child(4){{background:var(--blue)}}.mini-swatches i:nth-child(5){{background:var(--purple)}}.status{{font-size:11px;display:flex;gap:6px;align-items:center;margin:2px 0 5px}}.status span{{width:7px;height:7px;border-radius:50%;background:var(--green)}}.progress{{height:4px;background:var(--bg3);border-radius:9px;overflow:hidden}}.progress i{{display:block;width:72%;height:100%;background:var(--green);border-radius:9px}}
.selection{{display:flex;align-items:center;gap:10px;padding:10px 12px;margin-top:10px;background:color-mix(in srgb,var(--blue) 13%,var(--bg1));border-color:color-mix(in srgb,var(--blue) 32%,var(--bg2))}}.selection-mark{{height:21px;width:21px;display:grid;place-items:center;border-radius:5px;background:var(--blue);color:var(--bg0);font-size:12px}}.selection b{{font-size:11px}}.selection p{{font-size:10px;margin:1px 0 0}}kbd{{margin-left:auto;color:var(--fgDim);border:1px solid var(--bg3);border-radius:4px;padding:2px 5px;font:10px ui-monospace,monospace}}
.terminal{{margin-top:11px;border:1px solid var(--bg3);border-radius:9px;overflow:hidden;background:var(--bg0)}}.terminal-head{{height:30px;background:var(--bg1);border-bottom:1px solid var(--bg2);display:flex;align-items:center;justify-content:space-between;padding:0 10px;color:var(--fgDim);font:9px ui-monospace,monospace}}.terminal-head span{{display:flex;gap:4px}}.terminal-head i{{width:6px;height:6px;border-radius:50%;background:var(--red)}}.terminal-head i:nth-child(2){{background:var(--yellow)}}.terminal-head i:nth-child(3){{background:var(--green)}}.terminal-head em{{font-style:normal}}.terminal pre{{margin:0;padding:11px 12px;color:var(--fg);font:10px/1.75 ui-monospace,SFMono-Regular,monospace;white-space:pre-wrap}}.term-dim{{color:var(--fgDim)}}.term-key{{color:var(--blue)}}.term-string{{color:var(--green)}}.term-accent{{color:var(--purple)}}.term-green{{color:var(--green)}}
.palette{{padding:15px 2px 2px}}.swatches{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px}}.swatch{{display:grid;grid-template-columns:19px 1fr;grid-template-rows:auto auto;column-gap:7px;align-items:center;font-size:10px;min-width:0}}.swatch span{{grid-row:span 2;height:19px;width:19px;border-radius:5px;border:1px solid color-mix(in srgb,var(--fg) 15%,transparent)}}.swatch b{{font-weight:550;overflow:hidden;text-overflow:ellipsis}}.swatch code{{font:9px ui-monospace,monospace;color:var(--fgDim)}}
{theme_vars}
@media(max-width:900px){{.themes{{grid-template-columns:1fr}}.workspace{{min-height:0}}}}@media(max-width:480px){{main{{padding:24px 12px}}.page-head{{display:block}}.legend{{margin-top:10px}}.content{{padding:12px}}.swatches{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
.theme[hidden]{{display:none!important}}.theme-switch{{display:flex;align-items:center;justify-content:flex-end;gap:9px;color:#a89984;font-size:12px}}.switch{{position:relative;width:42px;height:24px;border:1px solid #3a3a3a;border-radius:99px;background:#1e1e1e;padding:2px;cursor:pointer}}.switch::after{{content:"";display:block;width:18px;height:18px;border-radius:50%;background:#ebdbb2;transition:transform .2s}}.switch[aria-checked="true"]{{background:#076678;border-color:#076678}}.switch[aria-checked="true"]::after{{transform:translateX(18px);background:#e2e4e6}}.switch:focus-visible{{outline:2px solid #83a598;outline-offset:3px}}.mode-choices{{display:flex;justify-content:flex-end;gap:5px;margin-top:8px}}.mode-choices[hidden]{{display:none}}.mode-choices button{{background:#1e1e1e;color:#a89984;padding:5px 9px}}.mode-choices button[aria-pressed="true"]{{background:#076678;color:#fff}}
</style></head><body><main><header class="page-head"><div><h1>CodeParity color preview</h1><p>Compare both modes in the same interface.</p></div><div><label class="theme-switch"><span>Side by side</span><button class="switch" id="modeSwitch" role="switch" aria-checked="false" aria-label="Toggle single mode preview"></button><span>Single mode</span></label><div class="mode-choices" id="modeChoices" hidden><button type="button" data-mode="dark" aria-pressed="true">Dark</button><button type="button" data-mode="light" aria-pressed="false">Light</button></div></div></header><div class="themes">{themes}</div></main><script>
const toggle=document.getElementById('modeSwitch');
const choices=document.getElementById('modeChoices');
const cards=[...document.querySelectorAll('.theme')];
let selectedMode='dark';
function updateView(){{
  const single=toggle.getAttribute('aria-checked')==='true';
  cards.forEach(card=>{{card.hidden=single&&!card.classList.contains(selectedMode)}});
  choices.hidden=!single;
}}
toggle.addEventListener('click',()=>{{
  const single=toggle.getAttribute('aria-checked')!=='true';
  toggle.setAttribute('aria-checked',String(single));
  updateView();
}});
choices.addEventListener('click',event=>{{
  const choice=event.target.closest('[data-mode]');
  if(!choice)return;
  selectedMode=choice.dataset.mode;
  choices.querySelectorAll('[data-mode]').forEach(button=>button.setAttribute('aria-pressed',String(button===choice)));
  updateView();
}});
</script></body></html>'''
(ROOT / "index.html").write_text(page)
