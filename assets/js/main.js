(() => {
  const root = document.documentElement;
  const themeButton = document.querySelector(".theme-toggle");
  const themeMeta = document.querySelector('meta[name="theme-color"]');
  const savedTheme = localStorage.getItem("theme");
  const preferredTheme = matchMedia("(prefers-color-scheme: light)").matches
    ? "light"
    : "dark";

  function setTheme(theme) {
    root.dataset.theme = theme;
    root.style.colorScheme = theme;
    themeMeta?.setAttribute(
      "content",
      theme === "dark" ? "#11100e" : "#f3efe5",
    );
  }

  setTheme(savedTheme || preferredTheme);
  themeButton?.addEventListener("click", () => {
    const theme = root.dataset.theme === "dark" ? "light" : "dark";
    setTheme(theme);
    localStorage.setItem("theme", theme);
  });

  const menuButton = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".site-nav");
  const header = document.querySelector(".site-header");
  menuButton?.addEventListener("click", () => {
    const open = menuButton.getAttribute("aria-expanded") === "true";
    menuButton.setAttribute("aria-expanded", String(!open));
    nav?.classList.toggle("is-open", !open);
  });
  nav?.addEventListener("click", (event) => {
    if (event.target.closest("a")) {
      menuButton?.setAttribute("aria-expanded", "false");
      nav.classList.remove("is-open");
    }
  });

  const updateHeader = () => {
    header?.classList.toggle("is-scrolled", window.scrollY > 24);
  };
  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });

  document.querySelectorAll("[data-year]").forEach((element) => {
    element.textContent = new Date().getFullYear();
  });
})();
