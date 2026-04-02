"""pages/register.py — Trang đăng ký"""

import streamlit as st
from utils.region import ALL_PROVINCES, get_region_from_province, REGION_LABELS
from database.connection import get_connection


def render():
    _, col, _ = st.columns([1, 1.8, 1])

    with col:
        # ── Header ──
        st.markdown("""
            <div style="text-align:center; padding: 2rem 0 1.75rem;">
                <h1 style="font-size:2rem; font-weight:900; color:#0f172a;
                    letter-spacing:-0.04em; margin:0 0 0.4rem;">GoRide</h1>
                <p style="color:#64748b; font-size:0.875rem; margin:0;">
                    Tạo tài khoản mới
                </p>
            </div>
        """, unsafe_allow_html=True)

        # ════════════════════════════════════
        # BƯỚC 1: Thông tin cá nhân
        # ════════════════════════════════════
        st.markdown("""
            <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.75rem;">
                <div style="width:22px; height:22px; border-radius:50%;
                     background:linear-gradient(135deg,#0ea5e9,#0284c7);
                     display:flex; align-items:center; justify-content:center;
                     font-size:0.65rem; font-weight:800; color:white; flex-shrink:0;">1</div>
                <p style="font-weight:700; font-size:0.95rem; color:#0f172a; margin:0;">
                    Thông tin cá nhân
                </p>
            </div>
        """, unsafe_allow_html=True)

        name  = st.text_input("Họ và tên *",       placeholder="Nguyễn Văn A",        key="reg_name")
        phone = st.text_input("Số điện thoại *",   placeholder="09xxxxxxxx",           key="reg_phone")

        col_a, col_b = st.columns(2)
        email   = col_a.text_input("Email",         placeholder="email@example.com",    key="reg_email")
        address = col_b.text_input("Địa chỉ",       placeholder="123 Đường ABC, Quận X",key="reg_addr")

        st.markdown("<div style='height:0.25rem;'></div>", unsafe_allow_html=True)

        # ════════════════════════════════════
        # BƯỚC 2: Khu vực
        # ════════════════════════════════════
        st.markdown("""
            <div style="width:100%; height:1px; background:#e2e8f0; margin:0.75rem 0;"></div>
            <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.75rem;">
                <div style="width:22px; height:22px; border-radius:50%;
                     background:linear-gradient(135deg,#0ea5e9,#0284c7);
                     display:flex; align-items:center; justify-content:center;
                     font-size:0.65rem; font-weight:800; color:white; flex-shrink:0;">2</div>
                <p style="font-weight:700; font-size:0.95rem; color:#0f172a; margin:0;">
                    Khu vực đăng ký
                </p>
            </div>
        """, unsafe_allow_html=True)

        province = st.selectbox(
            "Tỉnh / Thành phố",
            ALL_PROVINCES,
            index=ALL_PROVINCES.index("TP. Hồ Chí Minh") if "TP. Hồ Chí Minh" in ALL_PROVINCES else 0,
        )
        selected_region = get_region_from_province(province)
        rlabel = REGION_LABELS[selected_region]
        st.markdown(
            f'<div class="alert alert-info" style="margin-top:0.5rem; font-size:0.85rem;">'
            f'Tài khoản sẽ được tạo tại: <strong>{rlabel}</strong></div>',
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:0.25rem;'></div>", unsafe_allow_html=True)

        # ════════════════════════════════════
        # BƯỚC 3: Bảo mật
        # ════════════════════════════════════
        st.markdown("""
            <div style="width:100%; height:1px; background:#e2e8f0; margin:0.75rem 0;"></div>
            <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.75rem;">
                <div style="width:22px; height:22px; border-radius:50%;
                     background:linear-gradient(135deg,#0ea5e9,#0284c7);
                     display:flex; align-items:center; justify-content:center;
                     font-size:0.65rem; font-weight:800; color:white; flex-shrink:0;">3</div>
                <p style="font-weight:700; font-size:0.95rem; color:#0f172a; margin:0;">
                    Bảo mật
                </p>
            </div>
        """, unsafe_allow_html=True)

        col_pw1, col_pw2 = st.columns(2)
        password = col_pw1.text_input("Mật khẩu *",         type="password", placeholder="Tối thiểu 8 ký tự", key="reg_pw")
        confirm  = col_pw2.text_input("Xác nhận mật khẩu *", type="password", placeholder="Nhập lại mật khẩu", key="reg_pw_c")

        # ── Password strength ──
        if password:
            score = sum([
                len(password) >= 8,
                any(c.isupper() for c in password),
                any(c.isdigit() for c in password),
                any(c in "!@#$%^&*()" for c in password),
            ])
            colors = ["#ef4444", "#f59e0b", "#eab308", "#10b981"]
            labels = ["Rất yếu", "Yếu", "Trung bình", "Mạnh"]
            idx    = max(0, score - 1)
            segs   = []
            for i in range(4):
                bg = colors[idx] if i < score else "#e2e8f0"
                segs.append(f'<div style="flex:1; height:5px; background:{bg}; border-radius:3px;"></div>')
            st.markdown(f"""
                <div style="margin:0.5rem 0 0.75rem;">
                    <div style="display:flex; gap:4px; margin-bottom:4px;">{''.join(segs)}</div>
                    <p style="font-size:0.73rem; color:{colors[idx]}; font-weight:600; margin:0;">
                        Độ mạnh: {labels[idx]}
                    </p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.25rem;'></div>", unsafe_allow_html=True)

        # ── Điều khoản ──
        terms = st.checkbox("Tôi đồng ý với Điều khoản sử dụng và Chính sách bảo mật")

        st.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)

        # ── Buttons ──
        reg_btn = st.button("Tạo tài khoản", type="primary", use_container_width=True, key="btn_reg")

        st.markdown("""
            <div style="display:flex; align-items:center; margin:0.85rem 0;">
                <div style="flex:1; height:1px; background:#e2e8f0;"></div>
                <span style="padding:0 0.85rem; font-size:0.78rem; color:#94a3b8; font-weight:500;">
                    Đã có tài khoản?
                </span>
                <div style="flex:1; height:1px; background:#e2e8f0;"></div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Đăng nhập ngay", use_container_width=True, key="btn_go_login"):
            st.session_state.current_page = "login"
            st.rerun()

        # ── Validate & Submit ──
        if reg_btn:
            errors = []
            if not name.strip():
                errors.append("Họ tên không được để trống.")
            if not phone.strip() or not phone.strip().startswith(("0", "+84")) or len(phone.strip()) < 10:
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
                    st.error("Số điện thoại này đã được đăng ký.")
                    return

                db.execute(
                    "INSERT INTO users (name,phone,email,password,region,address) VALUES (%s,%s,%s,%s,%s,%s)",
                    (name.strip(), phone.strip(), email.strip(), password, selected_region, address.strip()),
                )
                db.commit()
                st.success(f"Đăng ký thành công tại {rlabel}! Vui lòng đăng nhập để tiếp tục.")
                import time; time.sleep(1.5)
                st.session_state.current_page = "login"
                st.rerun()
            except PermissionError as e:
                st.markdown(f'<div class="alert alert-warn">{e}</div>', unsafe_allow_html=True)
            except ConnectionError as e:
                st.markdown(f'<div class="alert alert-err">{e}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Lỗi: {e}")
