(() => {
  const root = document.documentElement;
  const button = document.querySelector(".card-theme");
  const meta = document.querySelector('meta[name="theme-color"]');
  const saved = localStorage.getItem("card-theme");
  const preferred = matchMedia("(prefers-color-scheme: light)").matches
    ? "light"
    : "dark";
  const apply = (theme) => {
    root.dataset.theme = theme;
    root.style.colorScheme = theme;
    meta?.setAttribute("content", theme === "dark" ? "#151512" : "#f1eee6");
  };
  apply(saved || preferred);
  button?.addEventListener("click", () => {
    const theme = root.dataset.theme === "dark" ? "light" : "dark";
    apply(theme);
    localStorage.setItem("card-theme", theme);
  });
  document
    .querySelectorAll("[data-year]")
    .forEach((node) => (node.textContent = new Date().getFullYear()));
})();
