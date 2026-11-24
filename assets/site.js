/* BioBesir — shared behaviour */
(function () {
  // Mobile navigation
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.textContent = open ? 'Close' : 'Menu';
    });
  }

  // Year in footer
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // Writing filters
  var filterBar = document.querySelector('[data-filters]');
  if (filterBar) {
    var buttons = filterBar.querySelectorAll('button');
    var items = document.querySelectorAll('.essay-item');
    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        buttons.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
        btn.setAttribute('aria-pressed', 'true');
        var f = btn.dataset.filter;
        items.forEach(function (it) { it.hidden = !(f === 'all' || it.dataset.kind === f); });
      });
    });
  }

  // Study search
  var input = document.getElementById('study-search');
  if (input && window.MATERIALS) {
    var out = document.getElementById('results');
    var status = document.getElementById('search-status');
    var base = input.dataset.base || '';
    var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
    var href = function (h) { return /^https?:/.test(h) ? h : base + h; };
    var render = function () {
      var q = input.value.trim().toLowerCase();
      if (q.length < 2) { out.innerHTML = ''; status.textContent = ''; return; }
      var words = q.split(/\s+/);
      var hits = window.MATERIALS.filter(function (l) {
        var hay = (l.title + ' ' + l.gradeLabel + ' ' + l.code + ' ' + l.res.map(function (r) { return r.label; }).join(' ')).toLowerCase();
        return words.every(function (w) { return hay.indexOf(w) !== -1; });
      });
      status.textContent = hits.length ? hits.length + (hits.length === 1 ? ' lesson' : ' lessons') + ' found' : 'No lessons match “' + input.value.trim() + '”. Try a shorter word, like “cell” or “blood”.';
      out.innerHTML = hits.length ? '<ul class="lessons">' + hits.map(function (l) {
        return '<li class="lesson"><span class="code">' + esc(l.code || '') + '</span>' +
          '<span class="title">' + esc(l.title) + '<a class="where" href="' + esc(base + 'studying-materials/' + l.page) + '">' + esc(l.gradeLabel) + '</a></span>' +
          '<ul class="res">' + l.res.map(function (r) {
            var ext = /^(https?:|simulations\/)/.test(r.href) || /\.(pdf|pptx)$/i.test(r.href);
            return '<li><a class="t-' + r.type + '" href="' + esc(href(r.href)) + '"' + (ext ? ' target="_blank" rel="noopener"' : '') + '><span class="dot"></span>' + esc(r.label) + '</a></li>';
          }).join('') + '</ul></li>';
      }).join('') + '</ul>' : '';
    };
    input.addEventListener('input', render);
    if (input.value) render();
  }

  // Home: microscope field of view (H&E-stained tissue, drawn once, panned slowly)
  var canvas = document.getElementById('scope');
  if (canvas && canvas.getContext) {
    var seed = 7;
    var rnd = function () { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var size = canvas.clientWidth || 440;
    canvas.width = size * dpr; canvas.height = size * dpr;
    var ctx = canvas.getContext('2d');

    var T = Math.round(size * 1.6 * dpr); // tissue tile
    var tile = document.createElement('canvas'); tile.width = T; tile.height = T * 2;
    var t = tile.getContext('2d');
    var H = T * 2;
    t.fillStyle = '#f6dbe4'; t.fillRect(0, 0, T, H);
    // extracellular fibres
    t.lineCap = 'round';
    for (var i = 0; i < 90; i++) {
      t.strokeStyle = 'rgba(214, 120, 152,' + (0.12 + rnd() * 0.18) + ')';
      t.lineWidth = (1 + rnd() * 3) * dpr;
      var x0 = rnd() * T, y0 = rnd() * H;
      t.beginPath(); t.moveTo(x0, y0);
      t.bezierCurveTo(x0 + (rnd() - .5) * 200 * dpr, y0 + (rnd() - .5) * 200 * dpr, x0 + (rnd() - .5) * 260 * dpr, y0 + (rnd() - .5) * 260 * dpr, x0 + (rnd() - .5) * 300 * dpr, y0 + (rnd() - .5) * 300 * dpr);
      t.stroke();
    }
    // cells on a jittered grid
    var step = 46 * dpr;
    for (var gy = -step; gy < H + step; gy += step) {
      for (var gx = -step; gx < T + step; gx += step) {
        if (rnd() < 0.12) continue;
        var cx = gx + (rnd() - .5) * step * 0.7, cy = gy + (rnd() - .5) * step * 0.7;
        var rx = step * (0.42 + rnd() * 0.16), ry = step * (0.36 + rnd() * 0.16), rot = rnd() * Math.PI;
        t.save(); t.translate(cx, cy); t.rotate(rot);
        t.beginPath(); t.ellipse(0, 0, rx, ry, 0, 0, Math.PI * 2);
        t.fillStyle = 'rgba(' + (232 + rnd() * 14 | 0) + ',' + (150 + rnd() * 40 | 0) + ',' + (178 + rnd() * 30 | 0) + ',0.75)';
        t.fill();
        t.lineWidth = 1.4 * dpr; t.strokeStyle = 'rgba(176, 64, 110, 0.55)'; t.stroke();
        // nucleus
        var nx = (rnd() - .5) * rx * 0.4, ny = (rnd() - .5) * ry * 0.4, nr = rx * (0.3 + rnd() * 0.14);
        t.beginPath(); t.ellipse(nx, ny, nr, nr * (0.75 + rnd() * 0.25), rnd(), 0, Math.PI * 2);
        t.fillStyle = 'rgba(' + (64 + rnd() * 30 | 0) + ',' + (44 + rnd() * 20 | 0) + ',' + (120 + rnd() * 30 | 0) + ',0.9)';
        t.fill();
        // chromatin specks + nucleolus
        for (var k = 0; k < 5; k++) {
          t.beginPath(); t.arc(nx + (rnd() - .5) * nr, ny + (rnd() - .5) * nr, (0.8 + rnd() * 1.2) * dpr, 0, Math.PI * 2);
          t.fillStyle = 'rgba(28, 18, 70, 0.7)'; t.fill();
        }
        t.restore();
      }
    }
    // a few red blood cells
    for (var b = 0; b < 26; b++) {
      var bx = rnd() * T, by = rnd() * H, br = 9 * dpr;
      t.beginPath(); t.arc(bx, by, br, 0, Math.PI * 2); t.fillStyle = 'rgba(205, 48, 92, 0.85)'; t.fill();
      t.beginPath(); t.arc(bx, by, br * 0.45, 0, Math.PI * 2); t.fillStyle = 'rgba(240, 130, 160, 0.7)'; t.fill();
    }

    var W = canvas.width;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var y = 0;
    var draw = function () {
      var span = H - W, m = y % (2 * span);
      var off = m < span ? m : 2 * span - m; // drift down, then back up — no jump
      ctx.drawImage(tile, (T - W) / 2, off, W, W, 0, 0, W, W);
      // soft vignette of the objective
      var g = ctx.createRadialGradient(W / 2, W / 2, W * 0.32, W / 2, W / 2, W * 0.52);
      g.addColorStop(0, 'rgba(255,255,255,0)'); g.addColorStop(1, 'rgba(40,24,60,0.35)');
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, W);
    };
    draw();
    if (!reduce) {
      var last = 0, visible = true;
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (e) { visible = e[0].isIntersecting; }).observe(canvas);
      }
      var loop = function (ts) {
        if (visible && ts - last > 33) { y += 0.35 * dpr; draw(); last = ts; }
        requestAnimationFrame(loop);
      };
      requestAnimationFrame(loop);
    }
  }
})();
