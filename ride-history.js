/* ────────────────────────────────
   DATA
──────────────────────────────── */
const rides = [
  {
    id: '1', code: 'GX-20240301-001',
    date: '04/03/2026', time: '08:32',
    pickup:  '121 Nguyễn Huệ, Quận 1, TP.HCM',
    dropoff: 'Sân bay Tân Sơn Nhất, Tân Bình, TP.HCM',
    distance: '8.4 km', duration: '25 phút',
    fare: 95000, status: 'completed',
    driver: 'Trần Minh Khoa',
    dAvatar: 'https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?w=80&h=80&fit=crop',
    dRating: 4.8, plate: '51G-245.88',
    vehicle: 'GoCar', pay: 'momo', uRating: 5
  },
  {
    id: '2', code: 'GX-20240228-047',
    date: '28/02/2026', time: '14:15',
    pickup:  'Landmark 81, Bình Thạnh, TP.HCM',
    dropoff: 'Phố đi bộ Nguyễn Huệ, Quận 1, TP.HCM',
    distance: '5.2 km', duration: '18 phút',
    fare: 52000, status: 'completed',
    driver: 'Lê Văn Hùng',
    dAvatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=80&h=80&fit=crop',
    dRating: 4.6, plate: '51K-889.12',
    vehicle: 'GoBike', pay: 'cash', uRating: 4
  },
  {
    id: '3', code: 'GX-20240225-012',
    date: '25/02/2026', time: '19:44',
    pickup:  'Aeon Mall Tân Phú, TP.HCM',
    dropoff: 'Vincom Center, Quận 3, TP.HCM',
    distance: '6.1 km', duration: '22 phút',
    fare: 68000, status: 'cancelled',
    driver: 'Phạm Thị Lan',
    dAvatar: 'https://images.unsplash.com/photo-1531123897727-8f129e1688ce?w=80&h=80&fit=crop',
    dRating: 4.9, plate: '51F-123.45',
    vehicle: 'GoCar', pay: 'card',
    cancelReason: 'Tài xế không đến đúng điểm đón'
  },
  {
    id: '4', code: 'GX-20240222-089',
    date: '22/02/2026', time: '07:05',
    pickup:  'KDC Him Lam, Quận 7, TP.HCM',
    dropoff: 'Tòa nhà Bitexco, Quận 1, TP.HCM',
    distance: '12.3 km', duration: '38 phút',
    fare: 145000, status: 'completed',
    driver: 'Nguyễn Văn Bình',
    dAvatar: 'https://images.unsplash.com/photo-1607990281513-2c110a25bd8c?w=80&h=80&fit=crop',
    dRating: 4.7, plate: '51A-456.78',
    vehicle: 'GoCar', pay: 'zalopay', uRating: 5
  },
  {
    id: '5', code: 'GX-20240220-055',
    date: '20/02/2026', time: '11:20',
    pickup:  'Đại học Bách Khoa TP.HCM, Quận 10',
    dropoff: 'Chợ Bến Thành, Quận 1, TP.HCM',
    distance: '3.5 km', duration: '14 phút',
    fare: 38000, status: 'completed',
    driver: 'Hoàng Đức Tài',
    dAvatar: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=80&h=80&fit=crop',
    dRating: 4.5, plate: '51B-678.90',
    vehicle: 'GoBike', pay: 'momo', uRating: 4
  },
  {
    id: '6', code: 'GX-20240218-031',
    date: '18/02/2026', time: '22:10',
    pickup:  'Bar 23, Bùi Viện, Quận 1, TP.HCM',
    dropoff: 'Sunrise City, Quận 7, TP.HCM',
    distance: '7.8 km', duration: '30 phút',
    fare: 89000, status: 'completed',
    driver: 'Vũ Thành Nam',
    dAvatar: 'https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=80&h=80&fit=crop',
    dRating: 4.8, plate: '51D-321.54',
    vehicle: 'GoCar', pay: 'cash', uRating: 5
  },
  {
    id: '7', code: 'GX-20240215-076',
    date: '15/02/2026', time: '09:00',
    pickup:  'Ga Sài Gòn, Quận 3, TP.HCM',
    dropoff: 'Bến xe Miền Đông, Bình Thạnh, TP.HCM',
    distance: '4.6 km', duration: '20 phút',
    fare: 55000, status: 'cancelled',
    driver: 'Đỗ Quang Vinh',
    dAvatar: 'https://images.unsplash.com/photo-1545167622-3a6ac756afa4?w=80&h=80&fit=crop',
    dRating: 4.3, plate: '51H-765.43',
    vehicle: 'GoCar', pay: 'cash',
    cancelReason: 'Khách hàng huỷ chuyến'
  },
  {
    id: '8', code: 'GX-20240210-019',
    date: '10/02/2026', time: '16:45',
    pickup:  'Lotte Mart Quận 7, TP.HCM',
    dropoff: 'Crescent Mall, Phú Mỹ Hưng, TP.HCM',
    distance: '2.1 km', duration: '10 phút',
    fare: 28000, status: 'completed',
    driver: 'Bùi Tiến Dũng',
    dAvatar: 'https://images.unsplash.com/photo-1552058544-f2b08422138a?w=80&h=80&fit=crop',
    dRating: 4.9, plate: '51E-111.22',
    vehicle: 'GoBike', pay: 'zalopay', uRating: 5
  },
  {
    id: '9', code: 'GX-20240206-041',
    date: '06/02/2026', time: '13:30',
    pickup:  'Bệnh viện Chợ Rẫy, Quận 5, TP.HCM',
    dropoff: 'Nhà thờ Đức Bà, Quận 1, TP.HCM',
    distance: '3.9 km', duration: '16 phút',
    fare: 44000, status: 'completed',
    driver: 'Phan Thị Thu',
    dAvatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=80&h=80&fit=crop',
    dRating: 4.7, plate: '51C-999.88',
    vehicle: 'GoCar', pay: 'momo', uRating: 4
  },
  {
    id: '10', code: 'GX-20240201-063',
    date: '01/02/2026', time: '18:00',
    pickup:  'Đảo Kim Cương, Quận 2, TP.HCM',
    dropoff: 'Trung tâm thương mại Estella Place, Quận 2',
    distance: '1.8 km', duration: '8 phút',
    fare: 22000, status: 'ongoing',
    driver: 'Lý Minh Tú',
    dAvatar: 'https://images.unsplash.com/photo-1603415526960-f7e0328c63b1?w=80&h=80&fit=crop',
    dRating: 4.6, plate: '51P-444.55',
    vehicle: 'GoBike', pay: 'card'
  }
];

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
   STATE
──────────────────────────────── */
let state = {
  tab:     'all',
  search:  '',
  sort:    'newest',
  vehicle: 'all',
  page:    1,
  filterOpen: false,
};

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

/* ────────────────────────────────
   RENDER – TABS
──────────────────────────────── */
// function renderTabs() {
//   const tabs = [
//     { val: 'all',       label: 'Tất cả' },
//     { val: 'completed', label: 'Hoàn thành' },
//     { val: 'cancelled', label: 'Đã huỷ' },
//     { val: 'ongoing',   label: 'Đang đi' },
//   ];
//   document.getElementById('tabs').innerHTML = tabs.map(t => `
//     <button
//       class="tab-btn${state.tab === t.val ? ' active' : ''}"
//       onclick="setTab('${t.val}')"
//     >
//       ${t.label}
//       <span class="tab-count">${countByStatus(t.val)}</span>
//     </button>
//   `).join('');
// }

/* ────────────────────────────────
   RENDER – CARD
──────────────────────────────── */
function cardHTML(r) {
  const isCar = r.vehicle === 'GoCar';

  const vehicleSVG = isCar
    ? `<svg width="20" height="20" viewBox="0 0 24 24" fill="#16a34a">
         <path d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z"/>
       </svg>`
    : `<svg width="20" height="20" viewBox="0 0 24 24" fill="#f97316">
         <path d="M15.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM5 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5zm5.8-10l2.4-2.4.8.8c1.3 1.3 3 2.1 5 2.1V9c-1.5 0-2.7-.6-3.6-1.5l-1.9-1.9c-.4-.4-.9-.6-1.4-.6s-1 .2-1.4.6L7.8 8.4C7.4 8.8 7 9.4 7 10s.4 1.2.8 1.6L10 13v5h2v-6l-1.2-1.5zM19 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5z"/>
       </svg>`;

  const barClass = { completed: 'bar-green', cancelled: 'bar-red', ongoing: 'bar-blue' }[r.status];

  return `
    <div class="ride-card" onclick="openModal('${r.id}')">
      <div class="ride-card-body">

        <!-- Top -->
        <div class="card-top">
          <div class="card-left">
            <div class="vehicle-icon ${isCar ? 'car' : 'bike'}">${vehicleSVG}</div>
            <div>
              <div class="card-title-row">
                <span class="vehicle-name">${r.vehicle}</span>
                <span class="status-badge ${STATUS_CLASS[r.status]}">
                  <span class="status-dot" style="background:${STATUS_DOT[r.status]}"></span>
                  ${STATUS_LABEL[r.status]}
                </span>
              </div>
              <div class="card-meta">${r.date} &middot; ${r.time} &middot; ${r.code}</div>
            </div>
          </div>
          <div class="card-right">
            <div class="card-fare">${r.fare.toLocaleString('vi-VN')}đ</div>
            <span class="payment-badge ${PAY_CLASS[r.pay]}">${PAY_LABELS[r.pay]}</span>
          </div>
        </div>

        <!-- Route -->
        <div class="route">
          <div class="route-dots">
            <div class="dot-pickup"></div>
            <div class="route-line"></div>
            <span class="dot-dropoff">📍</span>
          </div>
          <div class="route-info">
            <div>
              <div class="route-label">Điểm đón</div>
              <div class="route-addr">${r.pickup}</div>
            </div>
            <div>
              <div class="route-label">Điểm đến</div>
              <div class="route-addr">${r.dropoff}</div>
            </div>
          </div>
        </div>

        <!-- Bottom -->
        <div class="card-bottom">
          <div class="driver-info">
            <img class="driver-avatar" src="${r.dAvatar}" alt="${r.driver}" />
            <span class="driver-name">${r.driver}</span>
            <span class="driver-rating">⭐ ${r.dRating}</span>
          </div>
          <div class="card-bottom-right">
            <div class="trip-meta">
              ↗ ${r.distance}
              <span class="trip-sep">&middot;</span>
              🕐 ${r.duration}
            </div>
            ${r.uRating ? `<div class="stars">${starsHTML(r.uRating)}</div>` : ''}
            <span class="chevron">›</span>
          </div>
        </div>

      </div>
      <div class="card-status-bar ${barClass}"></div>
    </div>`;
}

/* ────────────────────────────────
   RENDER – LIST & PAGINATION
──────────────────────────────── */
// function renderList() {
//   const filtered   = getFiltered();
//   const totalPages = Math.max(1, Math.ceil(filtered.length / PER_PAGE));
//   if (state.page > totalPages) state.page = totalPages;

//   const paged = filtered.slice((state.page - 1) * PER_PAGE, state.page * PER_PAGE);

//   /* result info */
//   document.getElementById('resultInfo').innerHTML =
//     `Hiển thị <strong>${paged.length}</strong> / <strong>${filtered.length}</strong> chuyến đi`;

//   /* filter indicators */
//   const active = hasActiveFilters();
//   document.getElementById('filterDot').style.display      = active ? 'block' : 'none';
//   document.getElementById('clearFilterBtn').style.display = active ? 'flex'  : 'none';

//   /* list */
//   const listEl = document.getElementById('rideList');
//   if (paged.length === 0) {
//     listEl.innerHTML = `
//       <div class="empty-state">
//         <div class="empty-icon">🔍</div>
//         <h3>Không tìm thấy chuyến đi</h3>
//         <p>Thử điều chỉnh bộ lọc hoặc từ khoá tìm kiếm</p>
//         <button class="btn-secondary" onclick="clearAllFilters()">Xoá bộ lọc</button>
//       </div>`;
//   } else {
//     listEl.innerHTML = paged.map(cardHTML).join('');
//   }

//   /* pagination */
//   renderPagination(totalPages);
// }

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

/* ────────────────────────────────
   EVENT HANDLERS
──────────────────────────────── */
function setTab(val) {
  state.tab  = val;
  state.page = 1;
  renderTabs();
  renderList();
}

function setPage(el, page) {
  document.querySelectorAll('.nav-link').forEach(b => b.classList.remove('active'));
  el.classList.add('active');
  if (page !== 'history') showToast(`Trang "${page}" đang được phát triển...`);
}

function onSearch(el) {
  state.search = el.value;
  state.page   = 1;
  document.getElementById('searchClear').style.display = state.search ? 'block' : 'none';
  renderList();
}

function clearSearch() {
  document.getElementById('searchInput').value = '';
  state.search = '';
  state.page   = 1;
  document.getElementById('searchClear').style.display = 'none';
  renderList();
}

function onSort(el) {
  state.sort = el.value;
  state.page = 1;
  renderList();
}

function onVehicleFilter(el) {
  state.vehicle = el.value;
  state.page    = 1;
  renderList();
}

function toggleFilter() {
  state.filterOpen = !state.filterOpen;
  document.getElementById('extFilter').classList.toggle('show', state.filterOpen);
  document.getElementById('filterToggle').classList.toggle('active', state.filterOpen);
}

function clearAllFilters() {
  state.tab     = 'all';
  state.search  = '';
  state.sort    = 'newest';
  state.vehicle = 'all';
  state.page    = 1;

  document.getElementById('searchInput').value        = '';
  document.getElementById('searchClear').style.display = 'none';
  document.getElementById('sortSelect').value         = 'newest';
  document.getElementById('vehicleSelect').value      = 'all';
  document.getElementById('dateFrom').value           = '';
  document.getElementById('dateTo').value             = '';

  renderTabs();
  renderList();
}

function goPage(p) {
  const filtered   = getFiltered();
  const totalPages = Math.max(1, Math.ceil(filtered.length / PER_PAGE));
  state.page = Math.max(1, Math.min(p, totalPages));
  renderList();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/* ────────────────────────────────
   MODAL
──────────────────────────────── */
function openModal(id) {
  const r = rides.find(x => x.id === id);
  if (!r) return;

  const isCar  = r.vehicle === 'GoCar';
  const emoji  = isCar ? '🚗' : '🛵';
  const base   = Math.round(r.fare * 0.85);
  const extra  = Math.round(r.fare * 0.10);
  const vat    = Math.round(r.fare * 0.05);

  const mStatus = {
    completed: { cls: 'status-completed', label: '✅ Hoàn thành' },
    cancelled:  { cls: 'status-cancelled', label: '❌ Đã huỷ' },
    ongoing:    { cls: 'status-ongoing',   label: '⚡ Đang đi' },
  }[r.status];

  const mapDashes = Array(6).fill('<div class="map-dash"></div>').join('');

  document.getElementById('modalContent').innerHTML = `
    <div class="modal-header">
      <button class="modal-close" onclick="closeModal()">✕</button>

      <div class="modal-vehicle-row">
        <div class="modal-vehicle-icon ${isCar ? 'car' : 'bike'}">${emoji}</div>
        <div>
          <div class="modal-vehicle-name">${r.vehicle}</div>
          <div class="modal-booking-code">${r.code}</div>
        </div>
      </div>

      <div class="modal-fare-row">
        <div>
          <div class="modal-fare-label">Tổng tiền</div>
          <div class="modal-fare">${r.fare.toLocaleString('vi-VN')}đ</div>
        </div>
        <span class="modal-status-badge ${mStatus.cls}">${mStatus.label}</span>
      </div>
    </div>

    <div class="modal-body">
      <!-- Time -->
      <div class="modal-time-row">
        🕐 ${r.date}, ${r.time}
        <span class="sep">&middot;</span>
        ${r.duration}
        <span class="sep">&middot;</span>
        ↗ ${r.distance}
      </div>

      <!-- Map -->
      <div class="modal-map">
        <div class="map-grid"></div>
        <div class="map-content">
          <div class="map-dots">
            <div class="map-dot-green"></div>
            <div class="map-dashes">${mapDashes}</div>
            <div class="map-dot-red"></div>
          </div>
          <div class="map-label">Bản đồ hành trình</div>
        </div>
      </div>

      <!-- Route -->
      <div class="info-block">
        <div class="info-block-title">Hành trình</div>
        <div class="route-block">
          <div class="route-block-dots">
            <div class="rb-dot-green"></div>
            <div class="rb-line"></div>
            <span class="rb-dot-red">📍</span>
          </div>
          <div class="route-block-text">
            <div>
              <div class="route-block-item-label">Điểm đón</div>
              <div class="route-block-item-val">${r.pickup}</div>
            </div>
            <div>
              <div class="route-block-item-label">Điểm đến</div>
              <div class="route-block-item-val">${r.dropoff}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Driver -->
      <div class="info-block">
        <div class="info-block-title">Thông tin tài xế</div>
        <div class="driver-block">
          <div class="driver-block-left">
            <img class="driver-block-avatar" src="${r.dAvatar}" alt="${r.driver}" />
            <div>
              <div class="driver-block-name">${r.driver}</div>
              <div class="driver-block-sub">⭐ ${r.dRating} &middot; ${r.plate}</div>
            </div>
          </div>
          <button class="btn-call" onclick="showToast('Đang gọi ${r.driver}...')">📞</button>
        </div>
      </div>

      <!-- Payment -->
      <div class="info-block">
        <div class="info-block-title">Chi tiết thanh toán</div>
        <div class="payment-row"><span>Giá cước cơ bản</span><span>${base.toLocaleString('vi-VN')}đ</span></div>
        <div class="payment-row"><span>Phụ phí</span><span>${extra.toLocaleString('vi-VN')}đ</span></div>
        <div class="payment-row"><span>Thuế VAT (5%)</span><span>${vat.toLocaleString('vi-VN')}đ</span></div>
        <div class="payment-total">
          <span class="payment-total-label">Tổng cộng</span>
          <span class="payment-total-val">${r.fare.toLocaleString('vi-VN')}đ</span>
        </div>
        <div class="payment-method-row">💳 Thanh toán qua: <strong>${PAY_LABELS[r.pay]}</strong></div>
      </div>

      ${r.cancelReason ? `
      <div class="cancel-block">
        <div class="cancel-title">Lý do huỷ</div>
        <div class="cancel-reason">${r.cancelReason}</div>
      </div>` : ''}

      ${r.uRating ? `
      <div class="rating-block">
        <div class="rating-title">Đánh giá của bạn</div>
        <div class="rating-stars">${starsHTML(r.uRating).replace(/⭐/g, '<span class="rating-star">⭐</span>').replace(/☆/g, '<span class="rating-star" style="opacity:.2">⭐</span>')}</div>
      </div>` : ''}

      <!-- Actions -->
      <div class="modal-actions">
        <button class="btn-share" onclick="showToast('Đã sao chép link chia sẻ!')">📤 Chia sẻ</button>
        ${r.status !== 'ongoing' ? `<button class="btn-rebook" onclick="showToast('Đang đặt lại chuyến đi...');closeModal()">🔄 Đặt lại</button>` : ''}
      </div>
    </div>
  `;

  document.getElementById('modal').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  document.getElementById('modal').classList.remove('open');
  document.body.style.overflow = '';
}

function closeModalOutside(e) {
  if (e.target.id === 'modal') closeModal();
}

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
   INIT
──────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  renderTabs();
  renderList();
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });
});
