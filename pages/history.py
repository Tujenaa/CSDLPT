"""pages/history.py — Lịch sử chuyến đi"""

import streamlit as st
from database.connection import get_connection

PAY_LABELS   = {
    "cash":    "Tiền mặt",
    "momo":    "Ví MoMo",
    "card":    "Thẻ ngân hàng",
    "zalopay": "ZaloPay",
}
STATUS_LABEL = {"completed": "Hoàn thành", "cancelled": "Đã huỷ", "ongoing": "Đang đi"}
STATUS_BADGE = {"completed": "badge-green",  "cancelled": "badge-red", "ongoing": "badge-blue"}


def render():
    st.markdown("""
        <p class="page-header">Lịch sử chuyến đi</p>
        <p class="page-subtitle">Theo dõi tất cả các chuyến xe của bạn</p>
    """, unsafe_allow_html=True)

    region = st.session_state.user_region
    uid    = st.session_state.user_id

    try:
        db = get_connection(region)
    except ConnectionError as e:
        st.markdown(f'<div class="alert alert-err">{e}</div>', unsafe_allow_html=True)
        return

    if db.is_failover:
        st.markdown("""
            <div class="alert alert-warn">
                <strong>Primary server đang sập.</strong>
                Bạn đang kết nối Replica — chỉ xem được lịch sử,
                không thể đặt chuyến mới.
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class="alert alert-ok">Kết nối: <strong>{db.label}</strong></div>',
            unsafe_allow_html=True,
        )

    # ── Query ──
    all_rides = db.fetchall(
        "SELECT r.*, r.pickup_location AS pickup, r.dropoff_location AS dropoff, "
        "d.name as driver_name, d.plate, d.rating as d_rating "
        "FROM rides r LEFT JOIN drivers d ON r.driver_id = d.driver_id "
        "WHERE r.user_id=%s ORDER BY r.ride_date DESC, r.ride_time DESC",
        (uid,),
    )

    from datetime import date as _date, time as _time, timedelta as _td
    _DATE_MIN = _date(1900, 1, 1)
    _TIME_MIN = _time(0, 0)

    def _norm(row):
        r  = dict(row)
        rd = r.get("ride_date")
        if isinstance(rd, str) and rd:
            try:    r["ride_date"] = _date.fromisoformat(rd[:10])
            except: r["ride_date"] = _DATE_MIN
        elif not isinstance(rd, _date):
            r["ride_date"] = _DATE_MIN

        rt = r.get("ride_time")
        if isinstance(rt, _td):
            s = int(rt.total_seconds())
            try:    r["ride_time"] = _time(s // 3600 % 24, s % 3600 // 60, s % 60)
            except: r["ride_time"] = _TIME_MIN
        elif isinstance(rt, str) and rt:
            try:
                p = rt.split(":")
                r["ride_time"] = _time(int(p[0]) % 24, int(p[1]),
                                        int(p[2]) if len(p) > 2 else 0)
            except: r["ride_time"] = _TIME_MIN
        elif not isinstance(rt, _time):
            r["ride_time"] = _TIME_MIN

        try:    r["fare"] = int(r["fare"]) if r.get("fare") is not None else 0
        except: r["fare"] = 0

        for f in ["pickup","dropoff","driver_name","code",
                  "cancel_reason","payment","vehicle","status","plate"]:
            if not isinstance(r.get(f), str):
                r[f] = "" if r.get(f) is None else str(r[f])
        return r

    all_rides = [_norm(r) for r in all_rides]

    total      = len(all_rides)
    completed  = sum(1 for r in all_rides if r["status"] == "completed")
    cancelled  = sum(1 for r in all_rides if r["status"] == "cancelled")
    total_fare = sum(r["fare"] for r in all_rides if r["status"] == "completed")

    # ── Stat cards ──
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tổng chuyến",    total)
    c2.metric("Hoàn thành",     completed)
    c3.metric("Đã huỷ",         cancelled)
    c4.metric("Tổng chi tiêu",  f"{total_fare:,.0f}đ")

    st.markdown("---")

    # ── Thanh lọc ──
    fcol1, fcol2, fcol3 = st.columns([3, 1, 1])
    search = fcol1.text_input(
        "Tìm kiếm",
        placeholder="Địa chỉ, mã chuyến, tài xế...",
        label_visibility="collapsed",
    )
    status_filter = fcol2.selectbox(
        "Trạng thái",
        ["Tất cả", "Hoàn thành", "Đang đi", "Đã huỷ"],
        label_visibility="collapsed",
    )
    sort_order = fcol3.selectbox(
        "Sắp xếp",
        ["Mới nhất", "Cũ nhất"],
        label_visibility="collapsed",
    )

    rides = list(all_rides)
    if search.strip():
        q = search.lower()
        rides = [r for r in rides if any(
            q in str(r[f] or "").lower()
            for f in ["pickup","dropoff","driver_name","code"]
        )]
    if status_filter == "Hoàn thành":
        rides = [r for r in rides if r["status"] == "completed"]
    elif status_filter == "Đang đi":
        rides = [r for r in rides if r["status"] == "ongoing"]
    elif status_filter == "Đã huỷ":
        rides = [r for r in rides if r["status"] == "cancelled"]

    rides.sort(key=lambda r: (r["ride_date"], r["ride_time"]),
               reverse=(sort_order == "Mới nhất"))

    st.markdown(f"""
        <p style="color:#64748b; font-size:0.85rem; margin-bottom:0.75rem;">
            Hiển thị <strong style="color:#0f172a;">{len(rides)}</strong> / {total} chuyến
        </p>
    """, unsafe_allow_html=True)

    if not rides:
        st.markdown("""
            <div class="card" style="text-align:center; padding:3rem 1.5rem;">
                <div style="width:56px;height:56px;border-radius:14px;
                     background:#f1f5f9;border:2px solid #e2e8f0;
                     margin:0 auto 1rem;display:flex;align-items:center;justify-content:center;">
                    <svg width="26" height="26" viewBox="0 0 24 24" fill="#94a3b8">
                        <path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5
                                 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59
                                 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6
                                 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5
                                 14 7.01 14 9.5 11.99 14 9.5 14z"/>
                    </svg>
                </div>
                <p style="font-weight:700;color:#0f172a;font-size:1rem;margin:0 0 0.3rem;">
                    Không tìm thấy chuyến đi nào
                </p>
                <p style="color:#64748b;font-size:0.85rem;margin:0;">
                    Thử tìm kiếm với từ khoá khác hoặc đặt chuyến mới
                </p>
            </div>
        """, unsafe_allow_html=True)
        return

    # ── Phân trang ──
    PER_PAGE    = 6
    total_pages = max(1, (len(rides) + PER_PAGE - 1) // PER_PAGE)
    if "history_page" not in st.session_state:
        st.session_state.history_page = 1
    page = max(1, min(st.session_state.history_page, total_pages))
    page_rides = rides[(page-1)*PER_PAGE : page*PER_PAGE]

    for r in page_rides:
        _render_ride_card(r, db.is_failover)

    if total_pages > 1:
        st.markdown("")
        p1, p2, p3 = st.columns([1, 3, 1])
        if p1.button("Trang trước", disabled=(page <= 1), use_container_width=True):
            st.session_state.history_page = page - 1
            st.rerun()
        p2.markdown(
            f'<p style="text-align:center; color:#64748b; font-size:0.85rem; padding-top:0.5rem;">'
            f'Trang <strong style="color:#0f172a;">{page}</strong> / {total_pages}</p>',
            unsafe_allow_html=True,
        )
        if p3.button("Trang sau", disabled=(page >= total_pages), use_container_width=True):
            st.session_state.history_page = page + 1
            st.rerun()


def _render_ride_card(r, readonly: bool):
    status_lbl = STATUS_LABEL.get(r["status"], r["status"])
    status_cls = STATUS_BADGE.get(r["status"], "badge-blue")
    pay_lbl    = PAY_LABELS.get(r["payment"], r["payment"] or "—")

    date_str = r["ride_date"].strftime("%d/%m/%Y") if r["ride_date"] else "—"
    time_str = r["ride_time"].strftime("%H:%M")    if r["ride_time"] else "—"

    with st.expander(
        f"{r['code']}  ·  {date_str} {time_str}  ·  {r['fare']:,.0f}đ  ·  {status_lbl}",
        expanded=False,
    ):
        base  = round(r["fare"] * 0.85)
        extra = round(r["fare"] * 0.10)
        vat   = round(r["fare"] * 0.05)

        # ── Header: mã chuyến + badge trạng thái ──
        h_col1, h_col2 = st.columns([4, 1])
        with h_col1:
            st.markdown(
                f'<p style="font-size:0.75rem;color:#64748b;margin:0 0 2px;">Mã chuyến</p>'
                f'<p style="font-weight:700;color:#0f172a;margin:0;font-size:0.9rem;">{r["code"]}</p>',
                unsafe_allow_html=True,
            )
        with h_col2:
            st.markdown(
                f'<div style="text-align:right;padding-top:2px;">'
                f'<span class="{status_cls} badge">{status_lbl}</span></div>',
                unsafe_allow_html=True,
            )

        st.markdown("<div style='margin-bottom:0.5rem;'></div>", unsafe_allow_html=True)

        # ── Route: điểm đón → điểm trả ──
        st.markdown(
            f"""
            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;
                 padding:0.75rem 1rem;margin-bottom:0.75rem;">
                <div style="display:grid;grid-template-columns:20px 1fr;
                     gap:0 0.75rem;align-items:start;">
                    <div style="display:flex;flex-direction:column;
                         align-items:center;padding-top:4px;">
                        <div style="width:10px;height:10px;border-radius:50%;
                             background:#10b981;flex-shrink:0;"></div>
                        <div style="width:2px;flex:1;background:#e2e8f0;
                             margin:4px 0;min-height:24px;"></div>
                        <div style="width:10px;height:10px;border-radius:50%;
                             background:#ef4444;flex-shrink:0;"></div>
                    </div>
                    <div>
                        <p style="color:#0f172a;font-weight:500;font-size:0.875rem;
                           margin:0 0 0.85rem;">{r.get('pickup', '—')}</p>
                        <p style="color:#0f172a;font-weight:500;font-size:0.875rem;
                           margin:0;">{r.get('dropoff', '—')}</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Thông tin chi tiết (st.columns để tránh dùng grid trong markdown) ──
        num_cols = 4 if r["driver_name"] else 3
        cols = st.columns(num_cols)

        with cols[0]:
            dist_val = f"{r['distance_km']} km" if r.get("distance_km") is not None else "—"
            st.markdown(
                f'<p style="font-size:0.75rem;color:#64748b;margin:0 0 2px;">Khoảng cách</p>'
                f'<p style="font-weight:600;color:#0f172a;margin:0;font-size:0.9rem;">{dist_val}</p>',
                unsafe_allow_html=True,
            )
        with cols[1]:
            dur_val = f"{r['duration_min']} phút" if r.get("duration_min") is not None else "—"
            st.markdown(
                f'<p style="font-size:0.75rem;color:#64748b;margin:0 0 2px;">Thời gian</p>'
                f'<p style="font-weight:600;color:#0f172a;margin:0;font-size:0.9rem;">{dur_val}</p>',
                unsafe_allow_html=True,
            )
        with cols[2]:
            st.markdown(
                f'<p style="font-size:0.75rem;color:#64748b;margin:0 0 2px;">Thanh toán</p>'
                f'<p style="font-weight:600;color:#0f172a;margin:0;font-size:0.9rem;">{pay_lbl}</p>',
                unsafe_allow_html=True,
            )
        if r["driver_name"] and num_cols == 4:
            with cols[3]:
                st.markdown(
                    f'<p style="font-size:0.75rem;color:#64748b;margin:0 0 2px;">Tài xế</p>'
                    f'<p style="font-weight:600;color:#0f172a;margin:0;font-size:0.9rem;">{r["driver_name"]}</p>'
                    f'<p style="font-size:0.78rem;color:#64748b;margin:2px 0 0;">'
                    f'{r["plate"]} · {r["d_rating"] or "—"} sao</p>',
                    unsafe_allow_html=True,
                )

        st.markdown("<div style='margin-top:0.75rem;'></div>", unsafe_allow_html=True)

        # ── Breakdown giá ──
        st.markdown(
            f"""
            <div style="padding:0.75rem 1rem;background:#f8fafc;border-radius:8px;
                 border:1px solid #e2e8f0;font-size:0.8rem;color:#64748b;">
                Cước cơ bản: <strong style="color:#0f172a;">{base:,.0f}đ</strong>
                &nbsp;+&nbsp; Phụ phí: <strong style="color:#0f172a;">{extra:,.0f}đ</strong>
                &nbsp;+&nbsp; VAT 5%: <strong style="color:#0f172a;">{vat:,.0f}đ</strong>
                &nbsp;=&nbsp;
                <strong style="color:#0ea5e9;font-size:0.9rem;">{r['fare']:,.0f}đ</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Lý do huỷ ──
        if r["cancel_reason"]:
            st.markdown(
                f'<div class="alert alert-err" style="margin-top:0.75rem;">'
                f'Lý do huỷ: {r["cancel_reason"]}</div>',
                unsafe_allow_html=True,
            )

        if not readonly and r["status"] != "ongoing":
            if st.button("Đặt lại chuyến này", key=f"rebook_{r['ride_id']}"):
                st.session_state.rebook_from  = r["ride_id"]
                st.session_state.current_page = "book"
                st.rerun()