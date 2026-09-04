(() => {
  const root = document.documentElement;
  const themeButton = document.querySelector(".theme-toggle");
  const themeMeta = document.querySelector('meta[name="theme-color"]');
  let manualTheme = false;

  function getTimeTheme() {
    const hour = new Date().getHours();
    return hour >= 7 && hour < 19 ? "light" : "dark";
  }

  function setTheme(theme) {
    root.dataset.theme = theme;
    root.style.colorScheme = theme;
    themeMeta?.setAttribute(
      "content",
      theme === "dark" ? "#11100e" : "#fffaf0",
    );
    const icon = themeButton?.querySelector("span");
    if (icon) icon.textContent = theme === "dark" ? "☾" : "☀";
    themeButton?.setAttribute(
      "aria-label",
      theme === "dark"
        ? themeButton.dataset.darkLabel
        : themeButton.dataset.lightLabel,
    );
  }

  setTheme(getTimeTheme());
  themeButton?.addEventListener("click", () => {
    const theme = root.dataset.theme === "dark" ? "light" : "dark";
    manualTheme = true;
    setTheme(theme);
  });

  window.setInterval(() => {
    const timeTheme = getTimeTheme();
    if (timeTheme !== root.dataset.timeTheme) manualTheme = false;
    root.dataset.timeTheme = timeTheme;
    if (!manualTheme) setTheme(timeTheme);
  }, 60_000);
  root.dataset.timeTheme = getTimeTheme();

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
