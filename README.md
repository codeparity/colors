# CodeParity theme artifacts

The original single-file concept is now split into reusable palette and application artifacts. The standalone [preview](preview/index.html) is generated from the five files in `preview/samples/` (Python, JavaScript, Rust, JSON, and HTML).

## Files

- `palette.json` — canonical dark and light color tokens.
- `vim/codeparity.vim` — Vim and Neovim colorscheme, selected by `background`.
- `alacritty/codeparity-dark.toml` and `alacritty/codeparity-light.toml` — terminal palettes.
- `vscode/codeparity-color-theme.json` — VS Code dark workbench and syntax colors.
- `preview/samples/` — source files used to populate the preview.
- `preview/generate_preview.py` — rebuilds `preview/index.html` from those samples.

## Use

Copy `vim/codeparity.vim` to `~/.vim/colors/codeparity.vim` or `~/.config/nvim/colors/codeparity.vim`, then set `colorscheme codeparity`. Set `background=dark` or `background=light` to choose its variant.

For Alacritty, merge the desired TOML palette into your configuration. For VS Code, the JSON is the theme contribution; place it in an extension's `themes/` directory and reference it from that extension's `contributes.themes` manifest.

Regenerate the preview after changing a sample with:

```sh
python3 codeparity/preview/generate_preview.py
```

The existing `codeparity_theme_showcase.html` remains the interactive palette and UI showcase.

## Install

Run `./codeparity/install.sh` from this checkout. It detects Vim, Neovim, and Alacritty, then opens a checkbox menu with detected choices preselected. Enter a number to toggle an option, `i` to install, or `q` to quit. The Alacritty palette is copied into its themes directory; the script prints the import line to enable it in your config.

For a hosted checkout, pipe the script into Bash and point it at the raw `codeparity/` folder (the URL below is a placeholder for the repository's published raw URL):

```sh
curl -fsSL https://RAW-HOST/OWNER/REPO/BRANCH/codeparity/install.sh \\
  | bash -s -- --base-url https://RAW-HOST/OWNER/REPO/BRANCH/codeparity
```

Noninteractive options are `--vim`, `--nvim`, `--alacritty-dark`, `--alacritty-light`, and `--all` (all detected tools). `--help` lists usage.
