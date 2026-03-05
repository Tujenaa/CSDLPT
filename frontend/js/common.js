
/* ────────────────────────────────
   CONSTANTS
──────────────────────────────── */
const PAY_LABELS = { cash: 'Tiền mặt', momo: 'MoMo', card: 'Thẻ ngân hàng', zalopay: 'ZaloPay' };
const PAY_CLASS  = { cash: 'pay-cash',  momo: 'pay-momo', card: 'pay-card',  zalopay: 'pay-zalopay' };

const STATUS_LABEL = { completed: 'Hoàn thành', cancelled: 'Đã huỷ', ongoing: 'Đang đi' };
const STATUS_CLASS = { completed: 'status-completed', cancelled: 'status-cancelled', ongoing: 'status-ongoing' };
const STATUS_DOT   = { completed: '#22c55e', cancelled: '#ef4444', ongoing: '#3b82f6' };

const PER_PAGE = 5;

/* ────────────────────────────────
   HELPERS
──────────────────────────────── */
function getFiltered() {
  let list = [...rides];
  if (state.tab     !== 'all') list = list.filter(r => r.status  === state.tab);
  if (state.vehicle !== 'all') list = list.filter(r => r.vehicle === state.vehicle);
  if (state.search.trim()) {
    const q = state.search.toLowerCase();
    list = list.filter(r =>
      r.pickup.toLowerCase().includes(q)  ||
      r.dropoff.toLowerCase().includes(q) ||
      r.driver.toLowerCase().includes(q)  ||
      r.code.toLowerCase().includes(q)
    );
  }
  const dir = { newest: (a,b) => b.id.localeCompare(a.id),
                oldest: (a,b) => a.id.localeCompare(b.id),
                highest:(a,b) => b.fare - a.fare,
                lowest: (a,b) => a.fare - b.fare };
  list.sort(dir[state.sort]);
  return list;
}

function hasActiveFilters() {
  return state.tab !== 'all'
    || state.search
    || state.sort !== 'newest'
    || state.vehicle !== 'all'
    || document.getElementById('dateFrom').value
    || document.getElementById('dateTo').value;
}

function starsHTML(n, total = 5) {
  let h = '';
  for (let i = 0; i < total; i++) h += `<span>${i < n ? '⭐' : '☆'}</span>`;
  return h;
}

function countByStatus(s) {
  return s === 'all' ? rides.length : rides.filter(r => r.status === s).length;
}

