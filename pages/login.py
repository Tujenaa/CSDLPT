"""pages/login.py — Trang đăng nhập"""

import streamlit as st
from utils.region import ALL_PROVINCES, get_region_from_province, REGION_LABELS
from database.connection import get_connection


def render():
    # CSS căn giữa nội dung
    st.markdown("""
        <style>
        div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stVerticalBlock"]) {
            max-width: 520px;
            margin: 0 auto;
        }
        </style>
    """, unsafe_allow_html=True)

    # ── Spacer + Logo ──
    st.markdown("""
        <div style="text-align:center; padding:2rem 0 1.5rem;">
            <div style="
                width:64px; height:64px; border-radius:16px;
                background:linear-gradient(135deg,#0ea5e9,#0284c7);
                margin:0 auto 1.25rem; display:flex; align-items:center;
                justify-content:center;
                box-shadow:0 8px 24px rgba(14,165,233,0.3);">
                <svg width="32" height="32" viewBox="0 0 24 24"
                     fill="white" style="display:block;">
                    <path d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66
                             0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0
                             1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45
                             1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5
                             S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11
                             0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67
                             1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z"/>
                </svg>
            </div>
            <h1 style="font-size:2rem; font-weight:900; color:#0f172a;
                letter-spacing:-0.04em; margin:0 0 0.4rem; line-height:1;">
                GoRide
            </h1>
            <p style="color:#64748b; font-size:0.875rem; margin:0; line-height:1.5;">
                Ứng dụng gọi xe theo vị trí &nbsp;·&nbsp;
                <span style="color:#94a3b8;">Hệ thống CSDL Phân tán</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ── Bố cục 3 cột để căn giữa ──
    left, center, right = st.columns([1, 1.8, 1])

    with center:
        # ── Định tuyến server ──
        st.markdown("""
            <p style="font-size:0.68rem; text-transform:uppercase;
               letter-spacing:0.1em; font-weight:700; color:#94a3b8;
               margin:0 0 0.6rem;">Định tuyến Server theo vị trí</p>
        """, unsafe_allow_html=True)

        province = st.selectbox(
            "Tỉnh / Thành phố",
            ALL_PROVINCES,
            index=ALL_PROVINCES.index("TP. Hồ Chí Minh")
            if "TP. Hồ Chí Minh" in ALL_PROVINCES else 0,
            key="login_province",
        )
        selected_region = get_region_from_province(province)
        rlabel = REGION_LABELS[selected_region]

        st.markdown(
            f'<div class="alert alert-ok" style="margin-bottom:1.25rem;">'
            f'Kết nối tới: <strong>{rlabel}</strong></div>',
            unsafe_allow_html=True,
        )

        # ── Form đăng nhập ──
        st.markdown("""
            <p style="font-size:1.1rem; font-weight:700; color:#0f172a;
               margin:0 0 0.75rem;">Đăng nhập</p>
        """, unsafe_allow_html=True)

        phone    = st.text_input(
            "Số điện thoại",
            placeholder="VD: 0901234567",
            key="login_phone",
        )
        password = st.text_input(
            "Mật khẩu",
            placeholder="Nhập mật khẩu",
            type="password",
            key="login_pass",
        )

        st.markdown("<div style='height:0.25rem;'></div>", unsafe_allow_html=True)
        login_btn = st.button(
            "Đăng nhập",
            type="primary",
            use_container_width=True,
            key="btn_login",
        )

        st.markdown("""
            <div style="display:flex;align-items:center;margin:1rem 0;">
                <div style="flex:1;height:1px;background:#e2e8f0;"></div>
                <span style="padding:0 0.85rem;font-size:0.78rem;
                      color:#94a3b8;font-weight:500;">Chưa có tài khoản?</span>
                <div style="flex:1;height:1px;background:#e2e8f0;"></div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Tạo tài khoản mới", use_container_width=True, key="btn_go_reg"):
            st.session_state.current_page = "register"
            st.rerun()

        # ── Tài khoản demo ──
        with st.expander("Tài khoản demo"):
            st.markdown("""
| Khu vực | Số điện thoại | Mật khẩu |
|---------|-------------|---------|
| Miền Nam | `0123456789` | `123456` |
| Miền Bắc | `0922222222` | `123456` |
            """)

        # ── Xử lý đăng nhập ──
        if login_btn:
            if not phone.strip():
                st.error("Vui lòng nhập số điện thoại.")
                st.stop()
            if not password:
                st.error("Vui lòng nhập mật khẩu.")
                st.stop()

            try:
                db   = get_connection(selected_region)
                user = db.fetchone(
                    "SELECT * FROM users WHERE phone=%s AND password=%s",
                    (phone.strip(), password),
                )
                if user:
                    st.session_state.logged_in    = True
                    st.session_state.user_id      = user["user_id"]
                    st.session_state.user_name    = user["name"]
                    st.session_state.user_phone   = user["phone"]
                    st.session_state.user_region  = user.get("region") or selected_region
                    st.session_state.current_page = "history"
                    st.rerun()
                else:
                    st.error("Sai số điện thoại hoặc mật khẩu.")
            except ConnectionError as e:
                st.markdown(
                    f'<div class="alert alert-err">{e}</div>',
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.error(f"Lỗi kết nối: {e}")
