"""pages/profile.py — Hồ sơ người dùng"""

import streamlit as st
from database.connection import get_connection
from utils.region import REGION_LABELS


def render():
    st.markdown("""
        <p class="page-header">Hồ sơ cá nhân</p>
        <p class="page-subtitle">Quản lý thông tin tài khoản của bạn</p>
    """, unsafe_allow_html=True)

    region = st.session_state.user_region
    uid    = st.session_state.user_id

    try:
        db = get_connection(region)
    except ConnectionError as e:
        st.markdown(f'<div class="alert alert-err">{e}</div>', unsafe_allow_html=True)
        return

    mode_badge = (
        '<span class="badge badge-amber">Read-Only</span>'
        if db.is_failover
        else '<span class="badge badge-green">Bình thường</span>'
    )
    st.markdown(
        f'<div class="alert alert-ok">Kết nối: <strong>{db.server_label}</strong>'
        f' &nbsp; {mode_badge}</div>',
        unsafe_allow_html=True,
    )

    user = db.fetchone("SELECT * FROM users WHERE user_id=%s", (uid,))
    if not user:
        st.error("Không tìm thấy thông tin người dùng.")
        return

    # ── Thống kê ──
    rides      = db.fetchall("SELECT * FROM rides WHERE user_id=%s", (uid,))
    total      = len(rides)
    completed  = sum(1 for r in rides if r["status"] == "completed")
    total_fare = sum(r["fare"] for r in rides if r["status"] == "completed")
    avg_fare   = total_fare // completed if completed else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tổng chuyến",   total)
    c2.metric("Hoàn thành",    completed)
    c3.metric("Tổng chi tiêu", f"{total_fare:,.0f}đ")
    c4.metric("Trung bình",    f"{avg_fare:,.0f}đ")

    st.markdown("---")

    # ── Tabs ──
    tab1, tab2, tab3 = st.tabs(["Thông tin", "Bảo mật", "Thống kê"])

    # ══════════════════════════════════
    # Tab 1 — Thông tin
    # ══════════════════════════════════
    with tab1:
        col_form, col_avatar = st.columns([2, 1])

        with col_avatar:
            name_parts = (user["name"] or "U").split()
            initials   = "".join(p[0].upper() for p in name_parts[:2])
            region_lbl = REGION_LABELS.get(region, region)

            st.markdown(f"""
                <div class="card" style="text-align:center; padding:2rem 1.5rem;">
                    <div style="width:88px; height:88px; border-radius:50%;
                         background:linear-gradient(135deg, #0ea5e9, #10b981);
                         display:flex; align-items:center; justify-content:center;
                         font-size:1.9rem; font-weight:800; color:white;
                         margin:0 auto 1rem;
                         box-shadow:0 8px 24px rgba(14,165,233,0.3);">
                        {initials}
                    </div>
                    <p style="font-weight:800; color:#0f172a; font-size:1.05rem;
                       margin:0 0 0.2rem;">{user['name']}</p>
                    <p style="color:#64748b; font-size:0.82rem; margin:0 0 0.75rem;">
                        {user['phone']}
                    </p>
                    <span class="badge badge-blue">{region_lbl}</span>
                    <div style="margin-top:1rem; padding-top:1rem;
                         border-top:1px solid #e2e8f0;">
                        <p class="stat-label">Chuyến hoàn thành</p>
                        <p style="font-size:1.5rem; font-weight:800; color:#0f172a;
                           margin:4px 0 0;">{completed}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with col_form:
            if db.is_failover:
                st.markdown(
                    '<div class="alert alert-warn">Chế độ Read-Only — không thể chỉnh sửa.</div>',
                    unsafe_allow_html=True,
                )

            with st.form("profile_form"):
                name  = st.text_input("Họ và tên",     value=user["name"]    or "")
                phone = st.text_input("Số điện thoại", value=user["phone"]   or "",
                                      disabled=True)
                col_a, col_b = st.columns(2)
                email = col_a.text_input("Email",      value=user["email"]   or "")
                dob   = col_b.text_input("Ngày sinh",  value=user["dob"]     or "",
                                          placeholder="DD/MM/YYYY")
                address = st.text_area("Địa chỉ",      value=user["address"] or "",
                                       height=80)
                save = st.form_submit_button(
                    "Lưu thay đổi", type="primary",
                    disabled=db.is_failover, use_container_width=True,
                )

            if save:
                try:
                    db.execute(
                        "UPDATE users SET name=%s, email=%s, dob=%s, address=%s "
                        "WHERE user_id=%s",
                        (name.strip(), email.strip(), dob.strip(),
                         address.strip(), uid),
                    )
                    db.commit()
                    st.session_state.user_name = name.strip()
                    st.success("Cập nhật thành công!")
                    st.rerun()
                except PermissionError as e:
                    st.markdown(f'<div class="alert alert-warn">{e}</div>',
                                unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Lỗi: {e}")

    # ══════════════════════════════════
    # Tab 2 — Bảo mật
    # ══════════════════════════════════
    with tab2:
        st.markdown(
            '<p style="font-weight:700; font-size:1rem; color:#0f172a; margin-bottom:0.75rem;">'
            'Đổi mật khẩu</p>',
            unsafe_allow_html=True,
        )

        if db.is_failover:
            st.markdown(
                '<div class="alert alert-warn">Chế độ Read-Only — không thể đổi mật khẩu.</div>',
                unsafe_allow_html=True,
            )
        else:
            col_pw, _ = st.columns([2, 1])
            with col_pw:
                with st.form("password_form"):
                    old_pass  = st.text_input("Mật khẩu hiện tại",     type="password")
                    new_pass  = st.text_input("Mật khẩu mới",          type="password")
                    conf_pass = st.text_input("Xác nhận mật khẩu mới", type="password")

                    if new_pass:
                        score  = sum([
                            len(new_pass) >= 8,
                            any(c.isupper() for c in new_pass),
                            any(c.isdigit() for c in new_pass),
                            any(c in "!@#$%^&*()" for c in new_pass),
                        ])
                        colors = ["#ef4444","#f59e0b","#eab308","#10b981"]
                        labels = ["Rất yếu","Yếu","Trung bình","Mạnh"]
                        idx    = max(0, score - 1)
                        segs   = []
                        for i in range(4):
                            bg = colors[idx] if i < score else "#e2e8f0"
                            segs.append(
                                f'<div style="flex:1;height:5px;background:{bg};'
                                f'border-radius:3px;"></div>'
                            )
                        st.markdown(f"""
                            <div style="margin:0.25rem 0 0.6rem;">
                                <div style="display:flex;gap:4px;margin-bottom:4px;">
                                    {''.join(segs)}
                                </div>
                                <p style="font-size:0.73rem;color:{colors[idx]};
                                   font-weight:600;margin:0;">
                                    Độ mạnh: {labels[idx]}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)

                    change = st.form_submit_button(
                        "Đổi mật khẩu", type="primary", use_container_width=True,
                    )

                if change:
                    if user["password"] != old_pass:
                        st.error("Mật khẩu hiện tại không đúng.")
                    elif len(new_pass) < 8:
                        st.error("Mật khẩu mới phải có ít nhất 8 ký tự.")
                    elif new_pass != conf_pass:
                        st.error("Mật khẩu xác nhận không khớp.")
                    else:
                        try:
                            db.execute(
                                "UPDATE users SET password=%s WHERE user_id=%s",
                                (new_pass, uid),
                            )
                            db.commit()
                            st.success("Đổi mật khẩu thành công!")
                        except Exception as e:
                            st.error(f"Lỗi: {e}")

    # ══════════════════════════════════
    # Tab 3 — Thống kê
    # ══════════════════════════════════
    with tab3:
        st.markdown(
            '<p style="font-weight:700; font-size:1rem; color:#0f172a; margin-bottom:0.75rem;">'
            'Thống kê chi tiêu</p>',
            unsafe_allow_html=True,
        )

        if not rides:
            st.markdown("""
                <div class="card" style="text-align:center; padding:2.5rem;">
                    <p style="color:#64748b;">Chưa có dữ liệu chuyến đi</p>
                </div>
            """, unsafe_allow_html=True)
            return

        gocar_count  = sum(1 for r in rides if r["vehicle"] == "GoCar"  and r["status"] == "completed")
        gobike_count = sum(1 for r in rides if r["vehicle"] == "GoBike" and r["status"] == "completed")
        gocar_total  = sum(r["fare"] for r in rides if r["vehicle"] == "GoCar"  and r["status"] == "completed")
        gobike_total = sum(r["fare"] for r in rides if r["vehicle"] == "GoBike" and r["status"] == "completed")

        col_a, col_b = st.columns(2)
        col_a.markdown(f"""
            <div class="card">
                <p class="section-label">GoCar — Xe 4 chỗ</p>
                <p style="font-size:1.5rem;font-weight:800;color:#0f172a;margin:0.25rem 0;">
                    {gocar_total:,.0f}đ
                </p>
                <p style="color:#64748b;font-size:0.82rem;margin:0;">
                    {gocar_count} chuyến hoàn thành
                </p>
            </div>
        """, unsafe_allow_html=True)
        col_b.markdown(f"""
            <div class="card">
                <p class="section-label">GoBike — Xe máy</p>
                <p style="font-size:1.5rem;font-weight:800;color:#0f172a;margin:0.25rem 0;">
                    {gobike_total:,.0f}đ
                </p>
                <p style="color:#64748b;font-size:0.82rem;margin:0;">
                    {gobike_count} chuyến hoàn thành
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        st.markdown(
            '<p style="font-weight:700;font-size:0.95rem;color:#0f172a;margin-bottom:0.75rem;">'
            'Phương thức thanh toán</p>',
            unsafe_allow_html=True,
        )

        pay_stats  = {}
        for r in rides:
            if r["status"] == "completed":
                pay_stats[r["payment"]] = pay_stats.get(r["payment"], 0) + 1

        pay_labels = {
            "cash":    "Tiền mặt",
            "momo":    "Ví MoMo",
            "card":    "Thẻ ngân hàng",
            "zalopay": "ZaloPay",
        }

        col_prog, _ = st.columns([2, 1])
        with col_prog:
            for pay, count in sorted(pay_stats.items(), key=lambda x: -x[1]):
                pct = count / completed * 100 if completed else 0
                st.markdown(f"""
                    <div style="margin-bottom:0.75rem;">
                        <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                            <span style="color:#334155;font-size:0.85rem;font-weight:500;">
                                {pay_labels.get(pay, pay)}
                            </span>
                            <span style="color:#64748b;font-size:0.82rem;">
                                {count} chuyến ({pct:.0f}%)
                            </span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                st.progress(pct / 100)
