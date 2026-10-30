# CodeParity theme artifacts

The original single-file concept is now split into reusable palette and application artifacts. The standalone [preview](preview/index.html) shows the dark and light palettes side by side in a sample interface and is generated from `palette.json`.

## Files

- `palette.json` — canonical dark and light color tokens.
- `vim/codeparity.vim` — Vim and Neovim colorscheme, selected by `background`.
- `alacritty/codeparity-dark.toml` and `alacritty/codeparity-light.toml` — terminal palettes.
- `vscode/codeparity-color-theme.json` — VS Code dark workbench and syntax colors.
- `preview/generate_preview.py` — rebuilds the side-by-side preview from `palette.json`.

## Use

Copy `vim/codeparity.vim` to `~/.vim/colors/codeparity.vim` or `~/.config/nvim/colors/codeparity.vim`, then set `colorscheme codeparity`. Set `background=dark` or `background=light` to choose its variant.

For Alacritty, merge the desired TOML palette into your configuration. For VS Code, the JSON is the theme contribution; place it in an extension's `themes/` directory and reference it from that extension's `contributes.themes` manifest.

Regenerate the preview after changing a sample with:

```sh
python3 preview/generate_preview.py
```

## Install

Run `./install.sh` from this checkout. It detects Vim, Neovim, and Alacritty, then asks whether to install each option with standard `[Y/n]` prompts. Detected tools default to yes; Alacritty's dark palette defaults to yes and its light palette defaults to no. The Alacritty palette is copied into its themes directory; the script prints the import line to enable it in your config.

For a hosted checkout, pipe the script into Bash and point it at the raw folder containing `palette.json` and the `vim/` and `alacritty/` directories (the URL below is a placeholder for the repository's published raw URL):

```sh
curl -fsSL https://RAW-HOST/OWNER/REPO/BRANCH/install.sh \\
  | bash -s -- --base-url https://RAW-HOST/OWNER/REPO/BRANCH
```

Noninteractive options are `--vim`, `--nvim`, `--alacritty-dark`, `--alacritty-light`, and `--all` (all detected tools). `--help` lists usage.
