// Shared with the main site: the same stored light or dark choice, and the small-screen menu.
document.addEventListener("DOMContentLoaded", function () {
  var root = document.documentElement;
  var toggle = document.querySelector("[data-aa-theme]");
  if (toggle) toggle.addEventListener("click", function () {
    var now = root.getAttribute("data-theme") || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    var next = now === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("theme", next); } catch (e) {}
  });
  var menu = document.querySelector("[data-aa-menu]");
  var nav = document.getElementById("aa-nav");
  if (menu && nav) menu.addEventListener("click", function () {
    menu.setAttribute("aria-expanded", nav.classList.toggle("open") ? "true" : "false");
  });
});
