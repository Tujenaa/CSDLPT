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