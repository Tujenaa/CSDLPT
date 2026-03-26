"""pages/book.py — Trang đặt xe"""

import streamlit as st
import uuid
from datetime import date, datetime
from database.connection import get_connection

PAY_OPTIONS = {"cash": "💵 Tiền mặt", "momo": "🟣 MoMo", "card": "💳 Thẻ ngân hàng", "zalopay": "🔵 ZaloPay"}


def render():
    st.markdown('<h2>🚗 Đặt xe</h2>', unsafe_allow_html=True)

    region = st.session_state.user_region
    uid    = st.session_state.user_id

    try:
        db = get_connection(region)
    except ConnectionError as e:
        st.markdown(f'<div class="alert-err">{e}</div>', unsafe_allow_html=True)
        return

    if db.is_failover:
        st.markdown(
            '<div class="alert-warn">⚠️ <strong>Server đang ở chế độ Read-Only (Replica).</strong> '
            'Không thể đặt chuyến mới. Vui lòng thử lại sau.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f"**Kết nối hiện tại:** {db.server_label}")
        return

    st.markdown(f'<div class="alert-ok">🟢 Kết nối: <strong>{db.server_label}</strong></div>', unsafe_allow_html=True)

    # ── Form đặt xe ───────────────────────────────────────────────────────────
    with st.form("book_form"):
        st.subheader("📍 Thông tin hành trình")

        pickup  = st.text_input("🟢 Điểm đón",  placeholder="VD: 121 Nguyễn Huệ, Quận 1, TP.HCM")
        dropoff = st.text_input("🔴 Điểm đến",  placeholder="VD: Sân bay Tân Sơn Nhất")

        c1, c2 = st.columns(2)
        vehicle  = c1.selectbox("🚘 Loại xe",    ["GoCar 🚗", "GoBike 🛵"])
        payment  = c2.selectbox("💳 Thanh toán", list(PAY_OPTIONS.values()))

        st.subheader("🕐 Thời gian")
        dc1, dc2 = st.columns(2)
        ride_date = dc1.date_input("Ngày đi", value=date.today())
        ride_time = dc2.time_input("Giờ đi",  value=datetime.now().time())

        submit = st.form_submit_button("🚗 Đặt xe ngay", type="primary", use_container_width=True)

    if submit:
        errors = []
        if not pickup.strip():  errors.append("Vui lòng nhập điểm đón.")
        if not dropoff.strip(): errors.append("Vui lòng nhập điểm đến.")
        if pickup.strip() == dropoff.strip(): errors.append("Điểm đón và điểm đến không được trùng nhau.")

        if errors:
            for e in errors: st.error(e)
            return

        # Lấy tài xế ngẫu nhiên cùng khu vực & loại xe
        veh_key = "GoCar" if "GoCar" in vehicle else "GoBike"
        pay_key = [k for k, v in PAY_OPTIONS.items() if v in payment][0]

        driver = db.fetchone(
            "SELECT * FROM drivers WHERE region=%s AND vehicle=%s AND is_active=1 ORDER BY RAND() LIMIT 1",
            (region, veh_key),
        )

        # Tính cước giả lập
        import random
        distance  = round(random.uniform(1.5, 15.0), 1)
        duration  = int(distance * 3.5)
        fare      = int(distance * (10000 if veh_key == "GoCar" else 7500) + 5000)
        code      = f"{'GX' if region == 'south' else 'HN'}-{ride_date.strftime('%Y%m%d')}-{str(uuid.uuid4())[:3].upper()}"

        try:
            db.execute(
                """INSERT INTO rides (code,user_id,driver_id,pickup_location,dropoff_location,distance_km,
                   duration_min,fare,status,vehicle,payment,region,ride_date,ride_time)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                    code, uid,
                    driver["driver_id"] if driver else None,
                    pickup.strip(), dropoff.strip(),
                    distance, duration, fare,
                    "ongoing", veh_key, pay_key,
                    region,
                    ride_date.strftime("%Y-%m-%d"),
                    ride_time.strftime("%H:%M"),
                ),
            )
            db.commit()

            st.success(f"✅ Đặt xe thành công! Mã chuyến: **{code}**")
            st.markdown(f"""
| Thông tin | Chi tiết |
|---|---|
| 🚘 Loại xe | {veh_key} |
| 📏 Khoảng cách (ước tính) | {distance} km |
| ⏱️ Thời gian (ước tính) | {duration} phút |
| 💰 Cước phí | {fare:,}đ |
| 🧑‍✈️ Tài xế | {driver['name'] if driver else 'Đang tìm...'} |
| 🚘 Biển số | {driver['plate'] if driver else '—'} |
            """)

            if st.button("📋 Xem lịch sử chuyến"):
                st.session_state.current_page = "history"
                st.rerun()

        except PermissionError as e:
            st.markdown(f'<div class="alert-warn">{e}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Lỗi đặt xe: {e}")
