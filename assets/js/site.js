/* Le Rameau d'Olivier — interactions des maquettes */
(function () {
  "use strict";
  document.documentElement.classList.add("js");

  var HORAIRES = {
    0: ["Dimanche", "10h00 – 13h00"],
    1: ["Lundi", null],
    2: ["Mardi", "9h30 – 13h15 · 14h30 – 19h00"],
    3: ["Mercredi", "9h30 – 13h00 · 14h30 – 19h00"],
    4: ["Jeudi", "9h30 – 13h00 · 14h30 – 19h00"],
    5: ["Vendredi", "9h30 – 13h15 · 14h30 – 19h00"],
    6: ["Samedi", "9h30 – 13h15 · 14h30 – 19h00"]
  };

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    var today = HORAIRES[new Date().getDay()];

    /* horaires du jour dans la barre du haut + mise en avant dans les tableaux */
    document.querySelectorAll("[data-today-hours]").forEach(function (el) {
      el.innerHTML = today[1]
        ? '<span class="open-dot"></span>Aujourd’hui : <strong>' + today[1] + "</strong>"
        : '<span class="closed-dot"></span>Fermé aujourd’hui · ouvert demain dès 9h30';
    });
    document.querySelectorAll('[data-day="' + today[0] + '"]').forEach(function (li) {
      li.classList.add("today");
    });

    /* en-tête qui se resserre au défilement */
    var header = document.querySelector("[data-header]");
    var onScroll = function () {
      if (!header) return;
      /* « collé » dès que l'en-tête atteint le haut de l'écran */
      var topbar = document.querySelector(".topbar");
      var seuil = (topbar ? topbar.offsetHeight : 0) - parseFloat(getComputedStyle(header).top || 0);
      header.classList.toggle("scrolled", window.scrollY >= seuil - 1);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });

    /* menu mobile */
    var burger = document.querySelector(".burger");
    if (burger) {
      burger.addEventListener("click", function () {
        var open = document.body.classList.toggle("nav-open");
        burger.setAttribute("aria-expanded", String(open));
        burger.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
      });
    }
    /* tiroir du site actuel (proposition 6) : bouton × et fond assombri */
    document.querySelectorAll("[data-nav-close]").forEach(function (el) {
      el.addEventListener("click", function () {
        document.body.classList.remove("nav-open");
        if (burger) { burger.setAttribute("aria-expanded", "false"); burger.setAttribute("aria-label", "Ouvrir le menu"); }
      });
    });
    /* témoignages qui défilent (site actuel) */
    document.querySelectorAll("[data-carousel]").forEach(function (box) {
      var slides = box.children, i = 0;
      if (slides.length < 2) return;
      setInterval(function () {
        slides[i].classList.remove("on");
        i = (i + 1) % slides.length;
        slides[i].classList.add("on");
      }, 6000);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        document.body.classList.remove("nav-open");
        if (burger) burger.setAttribute("aria-expanded", "false");
        document.querySelectorAll(".has-mega.open").forEach(function (m) { m.classList.remove("open"); });
        if (document.activeElement && document.activeElement.closest(".has-mega")) document.activeElement.blur();
      }
    });

    /* carrousel des nouveautés */
    document.querySelectorAll("[data-rail]").forEach(function (rail) {
      var section = rail.closest("section");
      var prev = section.querySelector("[data-rail-prev]");
      var next = section.querySelector("[data-rail-next]");
      var step = function () {
        var card = rail.querySelector(".rail-card");
        return card ? (card.getBoundingClientRect().width + 20) * 2 : 400;
      };
      var update = function () {
        if (!prev) return;
        prev.disabled = rail.scrollLeft < 8;
        next.disabled = rail.scrollLeft + rail.clientWidth >= rail.scrollWidth - 8;
      };
      if (prev) prev.addEventListener("click", function () { rail.scrollBy({ left: -step() }); });
      if (next) next.addEventListener("click", function () { rail.scrollBy({ left: step() }); });
      rail.addEventListener("scroll", update, { passive: true });
      window.addEventListener("resize", update);
      update();
    });

    /* « Lire la suite » sur les descriptions longues */
    var checkClamps = function () {
      document.querySelectorAll("[data-clamp]").forEach(function (desc) {
        var btn = desc.parentElement.querySelector("[data-more]");
        if (!btn || desc.classList.contains("open")) return;
        btn.hidden = desc.scrollHeight <= desc.clientHeight + 2;
      });
    };
    document.querySelectorAll("[data-more]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var desc = btn.parentElement.querySelector("[data-clamp]");
        var open = desc.classList.toggle("open");
        btn.textContent = open ? "Réduire" : "Lire la suite";
      });
    });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(checkClamps);
    window.addEventListener("load", checkClamps);
    window.addEventListener("resize", checkClamps);
    checkClamps();

    /* formulaire de contact (maquette) */
    document.querySelectorAll("[data-form]").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        form.querySelector(".form-ok").hidden = false;
      });
    });

    /* sélecteur de proposition : masquable, mémorisé pour la session */
    var sw = document.querySelector("[data-switch]");
    try {
      if (sw && sessionStorage.getItem("ms-hidden") === "1") sw.classList.add("hidden");
    } catch (err) { /* stockage indisponible : on ignore */ }
    var close = document.querySelector("[data-switch-close]");
    if (close) close.addEventListener("click", function () {
      sw.classList.add("hidden");
      try { sessionStorage.setItem("ms-hidden", "1"); } catch (err) { /* ignore */ }
    });

    /* apparition douce au défilement */
    var items = document.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
      items.forEach(function (el) { io.observe(el); });
    } else {
      items.forEach(function (el) { el.classList.add("in"); });
    }
  });
})();
