"""pages/login.py — Trang đăng nhập với định tuyến theo vị trí"""

import streamlit as st
from utils.region import ALL_PROVINCES, get_region_from_province, REGION_LABELS, REGION_COLORS
from database.connection import get_connection


def render():
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        st.markdown('<h1 style="text-align:center;">🚗 GoX Ride</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center;color:#64748b;">Ứng dụng Gọi xe theo Vị trí</p>', unsafe_allow_html=True)
        st.markdown("---")
        st.subheader("🔑 Đăng nhập")

        # ── Chọn vị trí (định tuyến server) ──────────────────────────────────
        st.markdown("**📍 Vị trí của bạn** *(dùng để định tuyến tới Server khu vực)*")

        location_mode = st.radio(
            "Chọn cách xác định vị trí:",
            ["🏙️ Chọn Tỉnh/Thành phố", "🌐 Nhập toạ độ GPS"],
            horizontal=True,
            label_visibility="collapsed",
        )

        selected_region = "south"

        if location_mode == "🏙️ Chọn Tỉnh/Thành phố":
            province = st.selectbox(
                "Tỉnh/Thành phố",
                ALL_PROVINCES,
                index=ALL_PROVINCES.index("TP. Hồ Chí Minh"),
            )
            selected_region = get_region_from_province(province)
        else:
            c1, c2 = st.columns(2)
            lat = c1.number_input("Vĩ độ (Latitude)",  value=10.8231, format="%.4f")
            lon = c2.number_input("Kinh độ (Longitude)", value=106.6297, format="%.4f")
            from utils.region import get_region_from_coords
            selected_region = get_region_from_coords(lat, lon)

        color = REGION_COLORS[selected_region]
        st.markdown(
            f'<div class="alert-ok">🔀 Sẽ kết nối tới: <strong>{REGION_LABELS[selected_region]}</strong></div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # ── Form đăng nhập ────────────────────────────────────────────────────
        phone    = st.text_input("📱 Số điện thoại", placeholder="0901234567")
        password = st.text_input("🔒 Mật khẩu",      type="password")

        col_btn, col_link = st.columns([1, 1])
        login_btn = col_btn.button("Đăng nhập", type="primary", use_container_width=True)
        if col_link.button("📝 Chưa có tài khoản? Đăng ký", use_container_width=True):
            st.session_state.current_page = "register"
            st.rerun()

        # Demo hint
        with st.expander("💡 Tài khoản demo"):
            st.markdown("""
| Khu vực | SĐT | Mật khẩu |
|---|---|---|
| Miền Nam | `0123456789` | `123456` |
| Miền Bắc | `0922222222` | `123456` |
            """)

        if login_btn:
            if not phone or not password:
                st.error("Vui lòng nhập đầy đủ thông tin.")
                return

            try:
                db = get_connection(selected_region)
                user = db.fetchone(
                    "SELECT * FROM users WHERE phone=%s AND password=%s",
                    (phone.strip(), password),
                )
                if user:
                    st.session_state.logged_in    = True
                    st.session_state.user_id      = user["user_id"]
                    st.session_state.user_name    = user["name"]
                    st.session_state.user_phone   = user["phone"]
                    st.session_state.user_region  = user["region"] or selected_region
                    st.session_state.current_page = "history"
                    st.success(f"✅ Đăng nhập thành công! Kết nối: {db.label}")
                    st.rerun()
                else:
                    st.error("❌ Sai số điện thoại hoặc mật khẩu.")
            except ConnectionError as e:
                st.markdown(f'<div class="alert-err">{e}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Lỗi kết nối: {e}")
