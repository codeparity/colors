const palette = {
  background: "#202124",
  foreground: "#d6d3c8",
  accent: "#83a6a0",
};

export function applyTheme(root = document.documentElement) {
  root.style.setProperty("--background", palette.background);
  root.style.setProperty("--foreground", palette.foreground);
  return palette;
}
