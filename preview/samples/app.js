const palette = {
  background: "#181818",
  foreground: "#ebdbb2",
  accent: "#83a598",
};

export function applyTheme(root = document.documentElement) {
  root.style.setProperty("--background", palette.background);
  root.style.setProperty("--foreground", palette.foreground);
  return palette;
}
