"""pages/register.py — Trang đăng ký tài khoản"""

import streamlit as st
from utils.region import ALL_PROVINCES, get_region_from_province, REGION_LABELS, REGION_COLORS
from database.connection import get_connection


def render():
    _, col, _ = st.columns([1, 2, 1])

    with col:
        st.markdown('<h1 style="text-align:center;">🚗 GoX Re</h1>', unsafe_allow_html=True)
        st.subheader("📝 Đăng ký tài khoản")
        st.markdown("---")

        name    = st.text_input("👤 Họ và tên", placeholder="Nguyễn Văn A")
        phone   = st.text_input("📱 Số điện thoại", placeholder="09xxxxxxxx")
        email   = st.text_input("📧 Email (tuỳ chọn)", placeholder="email@example.com")
        address = st.text_input("🏠 Địa chỉ", placeholder="123 Đường ABC, Quận X")

        province = st.selectbox(
            "📍 Tỉnh/Thành phố",
            ALL_PROVINCES,
            index=ALL_PROVINCES.index("TP. Hồ Chí Minh"),
        )
        selected_region = get_region_from_province(province)
        st.markdown(
            f'<div class="alert-ok">🗄️ Tài khoản sẽ được tạo tại: <strong>{REGION_LABELS[selected_region]}</strong></div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")
        password = st.text_input("🔒 Mật khẩu",        type="password")
        confirm  = st.text_input("🔒 Xác nhận mật khẩu", type="password")

        # Password strength indicator
        if password:
            score = sum([
                len(password) >= 8,
                any(c.isupper() for c in password),
                any(c.isdigit() for c in password),
                any(c in "!@#$%^&*()" for c in password),
            ])
            levels = ["🔴 Rất yếu", "🟠 Yếu", "🟡 Trung bình", "🟢 Mạnh"]
            st.caption(f"Độ mạnh mật khẩu: {levels[score-1] if score else '🔴 Rất yếu'}")

        terms = st.checkbox("✅ Tôi đồng ý với Điều khoản sử dụng")

        col_btn, col_link = st.columns([1, 1])
        reg_btn = col_btn.button("Tạo tài khoản", type="primary", use_container_width=True)
        if col_link.button("🔑 Đã có tài khoản? Đăng nhập", use_container_width=True):
            st.session_state.current_page = "login"
            st.rerun()

        if reg_btn:
            errors = []
            if not name:    errors.append("Họ tên không được để trống.")
            if not phone or not phone.replace(" ", "").startswith(("0", "+84")) or len(phone.replace(" ", "")) < 10:
                errors.append("Số điện thoại không hợp lệ (VD: 0901234567).")
            if not password or len(password) < 8:
                errors.append("Mật khẩu phải có ít nhất 8 ký tự.")
            if password != confirm:
                errors.append("Mật khẩu xác nhận không khớp.")
            if not terms:
                errors.append("Bạn phải đồng ý Điều khoản sử dụng.")

            if errors:
                for e in errors:
                    st.error(e)
                return

            try:
                db = get_connection(selected_region)
                existing = db.fetchone("SELECT user_id FROM users WHERE phone=%s", (phone.strip(),))
                if existing:
                    st.error("❌ Số điện thoại này đã được đăng ký.")
                    return

                db.execute(
                    "INSERT INTO users (name,phone,email,password,region,address) VALUES (%s,%s,%s,%s,%s,%s)",
                    (name.strip(), phone.strip(), email.strip(), password, selected_region, address.strip()),
                )
                db.commit()
                st.success(f"✅ Đăng ký thành công tại {REGION_LABELS[selected_region]}!")
                st.info("Vui lòng đăng nhập để tiếp tục.")
                import time; time.sleep(1.5)
                st.session_state.current_page = "login"
                st.rerun()
            except PermissionError as e:
                st.markdown(f'<div class="alert-warn">{e}</div>', unsafe_allow_html=True)
            except ConnectionError as e:
                st.markdown(f'<div class="alert-err">{e}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Lỗi: {e}")