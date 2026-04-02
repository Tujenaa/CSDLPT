"""pages/book.py — Trang đặt xe"""

import streamlit as st
import uuid
from datetime import date, datetime
from database.connection import get_connection
from utils.region import REGION_LABELS

PAY_OPTIONS = {
    "cash":    "Tiền mặt",
    "momo":    "Ví MoMo",
    "card":    "Thẻ ngân hàng",
    "zalopay": "ZaloPay",
}
VEH_OPTIONS = ["GoCar (Xe 4 chỗ)", "GoBike (Xe máy)"]


def render():
    st.markdown("""
        <p class="page-header">Đặt xe</p>
        <p class="page-subtitle">Đặt chuyến xe mới trong khu vực của bạn</p>
    """, unsafe_allow_html=True)

    region = st.session_state.user_region
    uid    = st.session_state.user_id

    try:
        db = get_connection(region)
    except ConnectionError as e:
        st.markdown(f'<div class="alert alert-err">{e}</div>', unsafe_allow_html=True)
        return

    # ── Chế độ Read-Only (Replica) ──
    if db.is_failover:
        st.markdown("""
            <div class="alert alert-warn">
                <strong>Server đang ở chế độ Read-Only (Replica).</strong><br>
                <span style="font-size:0.85rem; opacity:0.85;">
                    Không thể đặt chuyến mới. Vui lòng thử lại khi Primary server phục hồi.
                </span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="card" style="text-align:center; padding:2.5rem 1.5rem;">
                <div style="width:56px; height:56px; border-radius:14px;
                     background:#fef3c7; border:2px solid #fbbf24;
                     margin:0 auto 1rem; display:flex; align-items:center; justify-content:center;">
                    <svg width="26" height="26" viewBox="0 0 24 24" fill="#b45309">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10
                                 10 10-4.48 10-10S17.52 2 12 2zm1
                                 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
                    </svg>
                </div>
                <p style="font-weight:700; color:#0f172a; font-size:1.05rem; margin:0 0 0.25rem;">
                    Tính năng tạm khoá
                </p>
                <p style="color:#64748b; font-size:0.85rem; margin:0;">
                    Kết nối hiện tại: <strong style="color:#92400e;">{db.server_label}</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)
        return

    st.markdown(
        f'<div class="alert alert-ok">Kết nối: <strong>{db.server_label}</strong></div>',
        unsafe_allow_html=True,
    )

    # ── Bố cục: Form + Bảng thông tin ──
    col_form, col_info = st.columns([2, 1])

    with col_form:
        with st.form("book_form"):
            st.markdown('<p style="font-size:0.95rem; font-weight:700; color:#0f172a; margin-bottom:0.75rem;">Thông tin hành trình</p>', unsafe_allow_html=True)

            pickup  = st.text_input("Điểm đón", placeholder="VD: 121 Nguyễn Huệ, Quận 1, TP.HCM")
            dropoff = st.text_input("Điểm đến", placeholder="VD: Sân bay Tân Sơn Nhất")

            c1, c2 = st.columns(2)
            vehicle = c1.selectbox("Loại xe",    VEH_OPTIONS)
            payment = c2.selectbox("Thanh toán", list(PAY_OPTIONS.values()))

            st.markdown("")
            st.markdown('<p style="font-size:0.95rem; font-weight:700; color:#0f172a; margin-bottom:0.75rem;">Thời gian</p>', unsafe_allow_html=True)

            dc1, dc2 = st.columns(2)
            ride_date = dc1.date_input("Ngày đi", value=date.today())
            ride_time = dc2.time_input("Giờ đi",  value=datetime.now().time())

            st.markdown("")
            submit = st.form_submit_button("Đặt xe ngay", type="primary", use_container_width=True)

    with col_info:
        region_lbl = REGION_LABELS[region]
        st.markdown(f"""
            <div class="card">
                <p class="section-label">Thông tin khu vực</p>
                <p style="font-weight:700; color:#0f172a; font-size:1rem; margin:0 0 0.25rem;">{region_lbl}</p>
                <p style="color:#64748b; font-size:0.82rem; margin:0; line-height:1.5;">
                    Tất cả chuyến đi được xử lý trên server khu vực này.
                </p>
            </div>

            <div class="card">
                <p class="section-label">Bảng giá ước tính</p>
                <div class="stat-grid">
                    <div class="stat-item">
                        <p class="stat-label">GoCar</p>
                        <p class="stat-value">10.000đ/km</p>
                    </div>
                    <div class="stat-item">
                        <p class="stat-label">GoBike</p>
                        <p class="stat-value">7.500đ/km</p>
                    </div>
                    <div class="stat-item">
                        <p class="stat-label">Phí cơ bản</p>
                        <p class="stat-value">5.000đ</p>
                    </div>
                </div>
            </div>

            <div class="card">
                <p class="section-label">Hướng dẫn</p>
                <p style="color:#64748b; font-size:0.82rem; line-height:1.6; margin:0;">
                    Nhập địa chỉ điểm đón và điểm đến chính xác để hệ thống tìm
                    tài xế phù hợp nhất trong khu vực của bạn.
                </p>
            </div>
        """, unsafe_allow_html=True)

    if submit:
        errors = []
        if not pickup.strip():  errors.append("Vui lòng nhập điểm đón.")
        if not dropoff.strip(): errors.append("Vui lòng nhập điểm đến.")
        if pickup.strip() == dropoff.strip():
            errors.append("Điểm đón và điểm đến không được trùng nhau.")

        if errors:
            for e in errors: st.error(e)
            return

        veh_key = "GoCar" if "GoCar" in vehicle else "GoBike"
        pay_key = [k for k, v in PAY_OPTIONS.items() if v == payment][0]

        driver = db.fetchone(
            "SELECT * FROM drivers WHERE region=%s AND vehicle=%s AND is_active=1 ORDER BY RAND() LIMIT 1",
            (region, veh_key),
        )

        import random
        distance  = round(random.uniform(1.5, 15.0), 1)
        duration  = int(distance * 3.5)
        fare      = int(distance * (10000 if veh_key == "GoCar" else 7500) + 5000)
        prefix    = "GX" if region == "south" else "HN"
        code      = f"{prefix}-{ride_date.strftime('%Y%m%d')}-{str(uuid.uuid4())[:3].upper()}"

        try:
            db.execute(
                """INSERT INTO rides (code,user_id,driver_id,pickup_location,dropoff_location,
                   distance_km,duration_min,fare,status,vehicle,payment,region,ride_date,ride_time)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                    code, uid,
                    driver["driver_id"] if driver else None,
                    pickup.strip(), dropoff.strip(),
                    distance, duration, fare,
                    "ongoing", veh_key, pay_key, region,
                    ride_date.strftime("%Y-%m-%d"),
                    ride_time.strftime("%H:%M"),
                ),
            )
            db.commit()

            driver_name   = driver["name"]   if driver else "Đang tìm tài xế..."
            driver_plate  = driver["plate"]  if driver else "—"
            driver_rating = driver["rating"] if driver else "—"

            st.markdown(f"""
                <div class="card" style="border-left:4px solid #10b981; margin-top:1.25rem;">
                    <div style="display:flex; justify-content:space-between;
                         align-items:flex-start; margin-bottom:1.25rem;">
                        <div>
                            <p style="font-size:1.1rem; font-weight:800; color:#047857;
                               margin:0 0 0.2rem;">Đặt xe thành công!</p>
                            <p style="color:#64748b; font-size:0.82rem; margin:0;">
                                Mã chuyến:
                                <code style="background:#f1f5f9; padding:2px 8px;
                                      border-radius:4px; color:#0f172a;
                                      font-weight:600;">{code}</code>
                            </p>
                        </div>
                        <span class="badge badge-green">{veh_key}</span>
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr;
                         gap:1rem; padding-top:1rem; border-top:1px solid #e2e8f0;">
                        <div>
                            <p class="stat-label">Khoảng cách</p>
                            <p class="stat-value">{distance} km</p>
                        </div>
                        <div>
                            <p class="stat-label">Thời gian (ước tính)</p>
                            <p class="stat-value">{duration} phút</p>
                        </div>
                        <div>
                            <p class="stat-label">Cước phí</p>
                            <p class="stat-value green">{fare:,.0f}đ</p>
                        </div>
                        <div>
                            <p class="stat-label">Tài xế</p>
                            <p class="stat-value" style="font-size:0.95rem;">{driver_name}</p>
                            <p style="font-size:0.78rem; color:#64748b; margin:2px 0 0;">
                                {driver_plate} &nbsp;·&nbsp; {driver_rating} sao
                            </p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            if st.button("Xem lịch sử chuyến", use_container_width=False):
                st.session_state.current_page = "history"
                st.rerun()

        except PermissionError as e:
            st.markdown(f'<div class="alert alert-warn">{e}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Lỗi đặt xe: {e}")
