/* ────────────────────────────────
   TOAST
──────────────────────────────── */
let toastTimer;
function showToast(msg) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.remove('show'), 2800);
}


/* ────────────────────────────────
   RENDER – TABS
──────────────────────────────── */
function renderTabs() {
  const tabs = [
    { val: 'all',       label: 'Tất cả' },
    { val: 'completed', label: 'Hoàn thành' },
    { val: 'cancelled', label: 'Đã huỷ' },
    { val: 'ongoing',   label: 'Đang đi' },
  ];
  document.getElementById('tabs').innerHTML = tabs.map(t => `
    <button
      class="tab-btn${state.tab === t.val ? ' active' : ''}"
      onclick="setTab('${t.val}')"
    >
      ${t.label}
      <span class="tab-count">${countByStatus(t.val)}</span>
    </button>
  `).join('');
}

/* ────────────────────────────────
   RENDER – LIST & PAGINATION
──────────────────────────────── */
function renderList() {
  const filtered   = getFiltered();
  const totalPages = Math.max(1, Math.ceil(filtered.length / PER_PAGE));
  if (state.page > totalPages) state.page = totalPages;

  const paged = filtered.slice((state.page - 1) * PER_PAGE, state.page * PER_PAGE);

  /* result info */
  document.getElementById('resultInfo').innerHTML =
    `Hiển thị <strong>${paged.length}</strong> / <strong>${filtered.length}</strong> chuyến đi`;

  /* filter indicators */
  const active = hasActiveFilters();
  document.getElementById('filterDot').style.display      = active ? 'block' : 'none';
  document.getElementById('clearFilterBtn').style.display = active ? 'flex'  : 'none';

  /* list */
  const listEl = document.getElementById('rideList');
  if (paged.length === 0) {
    listEl.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">🔍</div>
        <h3>Không tìm thấy chuyến đi</h3>
        <p>Thử điều chỉnh bộ lọc hoặc từ khoá tìm kiếm</p>
        <button class="btn-secondary" onclick="clearAllFilters()">Xoá bộ lọc</button>
      </div>`;
  } else {
    listEl.innerHTML = paged.map(cardHTML).join('');
  }

  /* pagination */
  renderPagination(totalPages);
}

function renderPagination(total) {
  const el = document.getElementById('pagination');
  if (total <= 1) { el.innerHTML = ''; return; }

  let html = `<button class="page-btn" onclick="goPage(${state.page - 1})" ${state.page === 1 ? 'disabled' : ''}>‹</button>`;

  for (let i = 1; i <= total; i++) {
    if (i === 1 || i === total || Math.abs(i - state.page) <= 1) {
      html += `<button class="page-btn${i === state.page ? ' active' : ''}" onclick="goPage(${i})">${i}</button>`;
    } else if (i === 2 || i === total - 1) {
      html += `<span class="page-ellipsis">…</span>`;
    }
  }

  html += `<button class="page-btn" onclick="goPage(${state.page + 1})" ${state.page === total ? 'disabled' : ''}>›</button>`;
  el.innerHTML = html;
}