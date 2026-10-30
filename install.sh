#!/usr/bin/env bash
# CodeParity installer. Works from a checkout or via curl with --base-url.
set -euo pipefail

usage() {
  cat <<'HELP'
CodeParity installer

Usage:
  ./install.sh [--base-url URL] [--all | --vim | --nvim | --alacritty-dark | --alacritty-light]

Run without options in a terminal to confirm detected tools with Y/n prompts. When
piped through curl, pass --base-url pointing to the hosted codeparity folder:
  curl -fsSL URL/install.sh | bash -s -- --base-url RAW_URL --all

The base URL should contain palette.json and the vim/, alacritty/ directories.
HELP
}

BASE_URL="${CODEPARITY_BASE_URL:-}"
MODE="menu"
while (($#)); do
  case "$1" in
    --base-url) BASE_URL="${2:?Expected URL after --base-url}"; shift 2 ;;
    --all|--vim|--nvim|--alacritty-dark|--alacritty-light) MODE="$1"; shift ;;
    --help|-h) usage; exit 0 ;;
    *) printf 'Unknown option: %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
done
BASE_URL="${BASE_URL%/}"

LOCAL_ROOT=""
if [[ -f "${BASH_SOURCE[0]:-}" ]]; then
  SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
  LOCAL_ROOT="$SCRIPT_DIR"
  [[ "$(basename "$SCRIPT_DIR")" == codeparity ]] || LOCAL_ROOT="$SCRIPT_DIR"
fi

fetch_asset() {
  local relative="$1" destination="$2"
  if [[ -n "$LOCAL_ROOT" && -f "$LOCAL_ROOT/$relative" ]]; then
    cp "$LOCAL_ROOT/$relative" "$destination"
  elif [[ -n "$BASE_URL" ]]; then
    command -v curl >/dev/null || { echo 'curl is required to fetch theme files.' >&2; return 1; }
    curl -fsSL "$BASE_URL/$relative" -o "$destination"
  else
    echo 'Could not find local theme files. For curl installs, pass --base-url URL.' >&2
    return 1
  fi
}

has_alacritty=0; has_vim=0; has_nvim=0
command -v alacritty >/dev/null 2>&1 && has_alacritty=1
command -v vim >/dev/null 2>&1 && has_vim=1
command -v nvim >/dev/null 2>&1 && has_nvim=1
[[ -d "${XDG_CONFIG_HOME:-$HOME/.config}/alacritty" ]] && has_alacritty=1
[[ -d "$HOME/.vim" ]] && has_vim=1
[[ -d "${XDG_CONFIG_HOME:-$HOME/.config}/nvim" ]] && has_nvim=1

selected_vim=0; selected_nvim=0; selected_alacritty_dark=0; selected_alacritty_light=0
case "$MODE" in
  --all) selected_vim=$has_vim; selected_nvim=$has_nvim; ((has_alacritty)) && selected_alacritty_dark=1 ;;
  --vim) selected_vim=1 ;;
  --nvim) selected_nvim=1 ;;
  --alacritty-dark) selected_alacritty_dark=1 ;;
  --alacritty-light) selected_alacritty_light=1 ;;
  menu)
    if [[ ! -r /dev/tty ]]; then
    echo 'Interactive install needs a terminal. Use --vim, --nvim, --alacritty-dark, --alacritty-light, or --all.' >&2
      exit 2
    fi
    ask_install() {
      local label="$1" default="$2" answer
      if ((default)); then
        printf '%s [Y/n] ' "$label" >/dev/tty
        IFS= read -r answer </dev/tty || answer=''
        [[ -z "$answer" || "$answer" =~ ^[Yy]$ ]]
      else
        printf '%s [y/N] ' "$label" >/dev/tty
        IFS= read -r answer </dev/tty || answer=''
        [[ "$answer" =~ ^[Yy]$ ]]
      fi
    }
    ask_install 'Install Vim colorscheme?' "$has_vim" && selected_vim=1
    ask_install 'Install Neovim colorscheme?' "$has_nvim" && selected_nvim=1
    ask_install 'Install Alacritty dark palette?' "$has_alacritty" && selected_alacritty_dark=1
    ask_install 'Install Alacritty light palette?' 0 && selected_alacritty_light=1
    ;;
esac

if (( ! selected_vim && ! selected_nvim && ! selected_alacritty_dark && ! selected_alacritty_light )); then
  echo 'Nothing selected. Exiting.'
  exit 0
fi

install_vim() {
  local target="$1" tmp
  mkdir -p "$(dirname "$target")"
  tmp="$(mktemp)"
  fetch_asset vim/codeparity.vim "$tmp"
  install -m 0644 "$tmp" "$target"
  rm -f "$tmp"
  printf 'Installed colorscheme: %s\n' "$target"
  printf 'Enable with: colorscheme codeparity\n'
}

if ((selected_vim)); then install_vim "$HOME/.vim/colors/codeparity.vim"; fi
if ((selected_nvim)); then
  nvim_dir="${XDG_CONFIG_HOME:-$HOME/.config}/nvim"
  install_vim "$nvim_dir/colors/codeparity.vim"
fi
install_alacritty() {
  local variant="$1" config_dir theme_dir tmp
  config_dir="${XDG_CONFIG_HOME:-$HOME/.config}/alacritty"
  theme_dir="$config_dir/themes"
  mkdir -p "$theme_dir"
  tmp="$(mktemp)"
  fetch_asset "alacritty/codeparity-${variant}.toml" "$tmp"
  install -m 0644 "$tmp" "$theme_dir/codeparity-${variant}.toml"
  rm -f "$tmp"
  printf 'Installed Alacritty palette: %s\n' "$theme_dir/codeparity-${variant}.toml"
  printf 'Enable by adding this to your Alacritty config: import = ["%s"]\n' "$theme_dir/codeparity-${variant}.toml"
}
((selected_alacritty_dark)) && install_alacritty dark
((selected_alacritty_light)) && install_alacritty light
