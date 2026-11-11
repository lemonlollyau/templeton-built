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

  // --- enquiry forms: carry a signed token ---------------------------------
  // Spam was arriving as scripted posts straight at /api/enquiry, never
  // loading the page. Every form carries a token minted server-side, so a
  // submission that skipped the page can be told apart from a real one.
  var forms = document.querySelectorAll('form[action="/api/enquiry"]');
  if (forms.length) {
    var field = function (form) {
      var input = form.querySelector('input[name="_t"]');
      if (!input) {
        input = document.createElement('input');
        input.type = 'hidden';
        input.name = '_t';
        form.appendChild(input);
      }
      return input;
    };

    var fetching = null;
    var fetchToken = function () {
      if (fetching) return fetching;
      fetching = fetch('/api/form-token', { cache: 'no-store' })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (data) {
          var token = data && data.token;
          if (token) {
            forms.forEach(function (form) { field(form).value = token; });
          }
          return token;
        })
        .catch(function () { return null; })
        .then(function (token) { fetching = null; return token; });
      return fetching;
    };

    fetchToken();

    // If the token hasn't arrived by the time someone submits — a slow
    // network, or a tab restored from cache — hold the submission just long
    // enough to fetch one, rather than letting a real enquiry be rejected.
    forms.forEach(function (form) {
      form.addEventListener('submit', function (e) {
        if (field(form).value) return;
        e.preventDefault();
        var submitted = false;
        var go = function () {
          if (submitted) return;
          submitted = true;
          form.submit();
        };
        fetchToken().then(go);
        setTimeout(go, 3000);
      });
    });
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
