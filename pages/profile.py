"""pages/profile.py — Hồ sơ người dùng"""

import streamlit as st
from database.connection import get_connection


def render():
    st.markdown('<h2>👤 Hồ sơ cá nhân</h2>', unsafe_allow_html=True)

    region = st.session_state.user_region
    uid    = st.session_state.user_id

    try:
        db = get_connection(region)
    except ConnectionError as e:
        st.markdown(f'<div class="alert-err">{e}</div>', unsafe_allow_html=True)
        return

    st.markdown(f'<div class="alert-ok">🟢 Kết nối: <strong>{db.server_label}</strong></div>', unsafe_allow_html=True)

    user = db.fetchone("SELECT * FROM users WHERE user_id=%s", (uid,))
    if not user:
        st.error("Không tìm thấy thông tin người dùng.")
        return

    # ── Thống kê ─────────────────────────────────────────────────────────────
    rides = db.fetchall("SELECT * FROM rides WHERE user_id=%s", (uid,))
    total      = len(rides)
    completed  = sum(1 for r in rides if r["status"] == "completed")
    total_fare = sum(r["fare"] for r in rides if r["status"] == "completed")
    avg_fare   = total_fare // completed if completed else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🚗 Tổng chuyến",   total)
    c2.metric("✅ Hoàn thành",    completed)
    c3.metric("💰 Tổng chi tiêu", f"{total_fare:,.0f}đ")
    c4.metric("📊 Trung bình",    f"{avg_fare:,.0f}đ")

    st.markdown("---")

    # ── Tabs ─────────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["📋 Thông tin cá nhân", "🔒 Bảo mật", "📊 Thống kê"])

    # ── Tab 1: Thông tin ─────────────────────────────────────────────────────
    with tab1:
        col_info, col_avatar = st.columns([2, 1])

        with col_avatar:
            st.markdown(
                f"""
                <div style="text-align:center;">
                    <div style="width:100px;height:100px;border-radius:50%;background:linear-gradient(135deg,#22c55e,#3b82f6);
                                display:flex;align-items:center;justify-content:center;
                                font-size:2.5rem;margin:0 auto 1rem;">
                        👤
                    </div>
                    <p style="font-weight:600;">{user['name']}</p>
                    <p style="color:#64748b;font-size:12px;">{user['phone']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_info:
            if db.is_failover:
                st.markdown('<div class="alert-warn">⚠️ Chế độ Read-Only — không thể chỉnh sửa.</div>', unsafe_allow_html=True)

            with st.form("profile_form"):
                name    = st.text_input("👤 Họ và tên",      value=user["name"] or "")
                phone   = st.text_input("📱 Số điện thoại",  value=user["phone"] or "", disabled=True)
                email   = st.text_input("📧 Email",          value=user["email"] or "")
                dob     = st.text_input("🎂 Ngày sinh",      value=user["dob"] or "", placeholder="DD/MM/YYYY")
                address = st.text_area ("🏠 Địa chỉ",        value=user["address"] or "", height=80)

                save = st.form_submit_button(
                    "💾 Lưu thay đổi",
                    type="primary",
                    disabled=db.is_failover,
                )

            if save:
                try:
                    db.execute(
                        "UPDATE users SET name=%s, email=%s, dob=%s, address=%s WHERE user_id=%s",
                        (name.strip(), email.strip(), dob.strip(), address.strip(), uid),
                    )
                    db.commit()
                    st.session_state.user_name = name.strip()
                    st.success("✅ Cập nhật thành công!")
                    st.rerun()
                except PermissionError as e:
                    st.markdown(f'<div class="alert-warn">{e}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Lỗi: {e}")

    # ── Tab 2: Bảo mật ───────────────────────────────────────────────────────
    with tab2:
        st.subheader("🔒 Đổi mật khẩu")
        if db.is_failover:
            st.markdown('<div class="alert-warn">⚠️ Chế độ Read-Only — không thể đổi mật khẩu.</div>', unsafe_allow_html=True)
        else:
            with st.form("password_form"):
                old_pass  = st.text_input("Mật khẩu hiện tại",    type="password")
                new_pass  = st.text_input("Mật khẩu mới",         type="password")
                conf_pass = st.text_input("Xác nhận mật khẩu mới", type="password")
                change    = st.form_submit_button("Đổi mật khẩu", type="primary")

            if change:
                if user["password"] != old_pass:
                    st.error("❌ Mật khẩu hiện tại không đúng.")
                elif len(new_pass) < 8:
                    st.error("Mật khẩu mới phải ít nhất 8 ký tự.")
                elif new_pass != conf_pass:
                    st.error("Mật khẩu xác nhận không khớp.")
                else:
                    try:
                        db.execute("UPDATE users SET password=%s WHERE user_id=%s", (new_pass, uid))
                        db.commit()
                        st.success("✅ Đổi mật khẩu thành công!")
                    except Exception as e:
                        st.error(f"Lỗi: {e}")

    # ── Tab 3: Thống kê ──────────────────────────────────────────────────────
    with tab3:
        st.subheader("📊 Thống kê chi tiêu")

        if not rides:
            st.info("Chưa có dữ liệu chuyến đi.")
            return

        # Biểu đồ theo loại xe
        gocar_total  = sum(r["fare"] for r in rides if r["vehicle"] == "GoCar" and r["status"] == "completed")
        gobike_total = sum(r["fare"] for r in rides if r["vehicle"] == "GoBike" and r["status"] == "completed")

        st.markdown("**Chi tiêu theo loại xe:**")
        col_a, col_b = st.columns(2)
        col_a.metric("🚗 GoCar",   f"{gocar_total:,}đ",  f"{sum(1 for r in rides if r['vehicle']=='GoCar' and r['status']=='completed')} chuyến")
        col_b.metric("🛵 GoBike",  f"{gobike_total:,}đ", f"{sum(1 for r in rides if r['vehicle']=='GoBike' and r['status']=='completed')} chuyến")

        st.markdown("**Phương thức thanh toán:**")
        pay_stats = {}
        for r in rides:
            if r["status"] == "completed":
                pay_stats[r["payment"]] = pay_stats.get(r["payment"], 0) + 1

        pay_labels = {"cash": "💵 Tiền mặt", "momo": "🟣 MoMo", "card": "💳 Thẻ", "zalopay": "🔵 ZaloPay"}
        for pay, count in sorted(pay_stats.items(), key=lambda x: -x[1]):
            pct = count / completed * 100 if completed else 0
            st.markdown(f"{pay_labels.get(pay, pay)}: **{count}** chuyến ({pct:.0f}%)")
            st.progress(pct / 100)