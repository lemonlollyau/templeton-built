/* Templeton Built — site behaviour.
   Nav state, scroll reveals, and the costing-schedule row animation.
   No framework, no jQuery. */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // --- nav: solid on scroll, drawer on mobile -----------------------------
  var nav = document.getElementById('nav');
  if (nav) {
    var setSolid = function () {
      nav.classList.toggle('solid', window.scrollY > 60);
    };
    setSolid();
    window.addEventListener('scroll', setSolid, { passive: true });

    var toggle = document.getElementById('toggle');
    var links = document.getElementById('links');
    if (toggle && links) {
      toggle.addEventListener('click', function () {
        var open = links.classList.toggle('open');
        toggle.classList.toggle('open', open);
        toggle.setAttribute('aria-expanded', String(open));
        toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      });
      // Close the drawer on Escape, so keyboard users aren't trapped.
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && links.classList.contains('open')) {
          toggle.click();
          toggle.focus();
        }
      });
    }
  }

  // --- scroll reveals -----------------------------------------------------
  var revs = document.querySelectorAll('.rev');
  if (revs.length) {
    if (reduce || !('IntersectionObserver' in window)) {
      revs.forEach(function (el) { el.classList.add('in'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('in');
            io.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
      revs.forEach(function (el) { io.observe(el); });
    }
  }

  // --- costing schedule: rows settle in sequence --------------------------
  var sheets = document.querySelectorAll('.sheet');
  if (!sheets.length) return;

  sheets.forEach(function (sheet) {
    if (reduce || !('IntersectionObserver' in window)) {
      sheet.classList.add('tb-in');
      return;
    }
    sheet.querySelectorAll('.row').forEach(function (row, i) {
      var delay = (i * 90) + 'ms';
      row.style.transitionDelay = delay;
      var span = row.querySelector('span');
      if (span) span.style.setProperty('--tbd', delay);
    });
    var sio = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('tb-in');
          sio.unobserve(entry.target);
        }
      });
    }, { threshold: 0.25 });
    sio.observe(sheet);
  });
})();
