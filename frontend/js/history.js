
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
   INIT
──────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  renderTabs();
  renderList();
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });
});
