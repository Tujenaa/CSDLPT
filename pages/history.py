"""pages/history.py — Lịch sử chuyến đi"""

import streamlit as st
from database.connection import get_connection

PAY_LABELS = {"cash": "💵 Tiền mặt", "momo": "🟣 MoMo", "card": "💳 Thẻ", "zalopay": "🔵 ZaloPay"}
STATUS_LABEL = {"completed": "✅ Hoàn thành", "cancelled": "❌ Đã huỷ", "ongoing": "⚡ Đang đi"}
STATUS_CLASS  = {"completed": "badge-completed", "cancelled": "badge-cancelled", "ongoing": "badge-ongoing"}


def render():
    st.markdown('<h2>📋 Lịch sử chuyến đi</h2>', unsafe_allow_html=True)

    region = st.session_state.user_region
    uid    = st.session_state.user_id

    # ── Kết nối & hiển thị trạng thái server ─────────────────────────────────
    try:
        db = get_connection(region)
    except ConnectionError as e:
        st.markdown(f'<div class="alert-err">{e}</div>', unsafe_allow_html=True)
        return

    if db.is_failover:
        st.markdown(
            '<div class="alert-warn">⚠️ <strong>Primary server đang sập.</strong> '
            'Bạn đang kết nối Replica — chỉ xem được lịch sử, không thể đặt chuyến mới.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="alert-ok">🟢 Kết nối: <strong>{db.label}</strong></div>',
            unsafe_allow_html=True,
        )

    # ── Thống kê nhanh ────────────────────────────────────────────────────────
    all_rides = db.fetchall(
        "SELECT r.*, "
        "r.pickup_location AS pickup, "
        "r.dropoff_location AS dropoff, "
        "d.name as driver_name, d.plate, d.rating as d_rating "
        "FROM rides r LEFT JOIN drivers d ON r.driver_id = d.driver_id "
        "WHERE r.user_id=%s ORDER BY r.ride_date DESC, r.ride_time DESC",
        (uid,),
    )

    from datetime import date as _date, time as _time, timedelta as _td

    _DATE_MIN = _date(1900, 1, 1)
    _TIME_MIN = _time(0, 0)

    def _normalize(row):
        r = {k: v for k, v in row.items()}  # plain dict, không phụ thuộc subclass

        # ride_date
        rd = r.get("ride_date")
        if isinstance(rd, _date):
            pass
        elif isinstance(rd, str) and rd:
            try:    r["ride_date"] = _date.fromisoformat(rd[:10])
            except: r["ride_date"] = _DATE_MIN
        else:
            r["ride_date"] = _DATE_MIN

        # ride_time — MySQL trả timedelta
        rt = r.get("ride_time")
        if isinstance(rt, _time):
            pass
        elif isinstance(rt, _td):
            s = int(rt.total_seconds())
            try:    r["ride_time"] = _time(s // 3600 % 24, s % 3600 // 60, s % 60)
            except: r["ride_time"] = _TIME_MIN
        elif isinstance(rt, str) and rt:
            try:
                p = rt.split(":")
                r["ride_time"] = _time(int(p[0]) % 24, int(p[1]), int(p[2]) if len(p) > 2 else 0)
            except: r["ride_time"] = _TIME_MIN
        else:
            r["ride_time"] = _TIME_MIN

        # fare
        try:    r["fare"] = int(r["fare"]) if r.get("fare") is not None else 0
        except: r["fare"] = 0

        # string fields
        for f in ["pickup", "dropoff", "driver_name", "code",
                  "cancel_reason", "payment", "vehicle", "status", "plate"]:
            if not isinstance(r.get(f), str):
                r[f] = "" if r.get(f) is None else str(r[f])

        return r

    all_rides = [_normalize(r) for r in all_rides]

    total      = len(all_rides)
    completed  = sum(1 for r in all_rides if r["status"] == "completed")
    cancelled  = sum(1 for r in all_rides if r["status"] == "cancelled")
    total_fare = sum(r["fare"] for r in all_rides if r["status"] == "completed")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🚗 Tổng chuyến",  total)
    c2.metric("✅ Hoàn thành",   completed)
    c3.metric("❌ Đã huỷ",       cancelled)
    c4.metric("💰 Tổng chi tiêu", f"{total_fare:,.0f}đ")

    st.markdown("---")

    # ── Tìm kiếm ─────────────────────────────────────────────────────────────
    search = st.text_input("🔍 Tìm kiếm", placeholder="Địa chỉ, mã chuyến, tài xế...")

    # ── Lọc & sắp xếp mặc định mới nhất ─────────────────────────────────────
    rides = list(all_rides)

    if search.strip():
        q = search.lower()
        rides = [r for r in rides if any(
            q in str(r[f] or "").lower()
            for f in ["pickup", "dropoff", "driver_name", "code"]
        )]

    rides.sort(key=lambda r: (r["ride_date"], r["ride_time"]), reverse=True)

    st.markdown(f"**{len(rides)} chuyến** (tổng {total})")
    st.markdown("---")

    # ── Danh sách chuyến ─────────────────────────────────────────────────────
    if not rides:
        st.info("Không tìm thấy chuyến đi nào.")
        return

    # Phân trang
    PER_PAGE = 5
    total_pages = max(1, (len(rides) + PER_PAGE - 1) // PER_PAGE)
    if "history_page" not in st.session_state:
        st.session_state.history_page = 1
    page = st.session_state.history_page
    page = max(1, min(page, total_pages))

    page_rides = rides[(page-1)*PER_PAGE : page*PER_PAGE]

    for r in page_rides:
        _render_ride_card(r, db.is_failover)

    # Phân trang controls
    if total_pages > 1:
        p1, p2, p3 = st.columns([1, 2, 1])
        if p1.button("← Trước", disabled=(page <= 1)):
            st.session_state.history_page = page - 1
            st.rerun()
        p2.markdown(f'<p style="text-align:center;">Trang {page} / {total_pages}</p>', unsafe_allow_html=True)
        if p3.button("Sau →", disabled=(page >= total_pages)):
            st.session_state.history_page = page + 1
            st.rerun()


def _render_ride_card(r, readonly: bool):
    vehicle_emoji = "🚗" if r["vehicle"] == "GoCar" else "🛵"
    status_cls    = STATUS_CLASS.get(r["status"], "")
    status_lbl    = STATUS_LABEL.get(r["status"], r["status"])
    pay_lbl       = PAY_LABELS.get(r["payment"], r["payment"] or "—")

    with st.expander(
        f"{vehicle_emoji} {r['code']}  |  {r['ride_date']} {r['ride_time']}  "
        f"|  {r['fare']:,}đ  |  {STATUS_LABEL.get(r['status'], r['status'])}",
        expanded=False,
    ):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**📍 Đón:** {r.get('pickup', '—')}")
            st.markdown(f"**🏁 Đến:** {r.get('dropoff', '—')}")
            st.markdown(f"**📏 Khoảng cách:** {r['distance_km']} km &nbsp;|&nbsp; **⏱️** {r['duration_min']} phút")
        with c2:
            if r["driver_name"]:
                st.markdown(f"**🧑‍✈️ Tài xế:** {r['driver_name']}  ⭐ {r['d_rating']}")
                st.markdown(f"**🚘 Biển số:** {r['plate']}")
            st.markdown(f"**💳 Thanh toán:** {pay_lbl}")
            if r["user_rating"]:
                stars = "⭐" * r["user_rating"] + "☆" * (5 - r["user_rating"])
                st.markdown(f"**Đánh giá:** {stars}")

        if r["cancel_reason"]:
            st.markdown(
                f'<div class="alert-err">⚠️ Lý do huỷ: {r["cancel_reason"]}</div>',
                unsafe_allow_html=True,
            )

        # Chi tiết thanh toán
        base  = round(r["fare"] * 0.85)
        extra = round(r["fare"] * 0.10)
        vat   = round(r["fare"] * 0.05)
        st.markdown(f"**Chi tiết:** Cước cơ bản {base:,}đ + Phụ phí {extra:,}đ + VAT {vat:,}đ = **{r['fare']:,}đ**")

        # Actions
        if not readonly and r["status"] != "ongoing":
            if st.button(f"🔄 Đặt lại chuyến", key=f"rebook_{r['ride_id']}"):
                st.success("Đang chuyển đến trang đặt xe...")
                st.session_state.rebook_from = r['ride_id']
                st.session_state.current_page = "book"
                st.rerun()