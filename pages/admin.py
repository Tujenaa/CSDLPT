"""
pages/admin.py — Hệ thống CSDL Phân tán
Demo kiến trúc Master-Slave Replication + Failover
"""

import streamlit as st
import time
from database.connection import (
    get_connection, get_server_status, set_server_status,
    replicate_all, SERVER_CONFIG, _get_raw_connection,
)
from utils.region import REGION_LABELS


def render():
    st.markdown("""
        <p class="page-header">Hệ thống CSDL Phân tán</p>
        <p class="page-subtitle">Quản lý và demo kiến trúc Master-Slave Replication + Failover theo vị trí</p>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Tổng quan",
        "Failover Demo",
        "Replication",
        "Test Cases",
    ])

    with tab1: _tab_overview()
    with tab2: _tab_failover()
    with tab3: _tab_replication()
    with tab4: _tab_testcases()


# ──────────────────────────────────────────────────────────────
def _dot(is_up: bool) -> str:
    cls   = "dot-up"   if is_up else "dot-down"
    label = "Online" if is_up else "Offline"
    return f'<span class="dot {cls}"></span>{label}'


# ──────────────────────────────────────────────────────────────
def _tab_overview():
    st.markdown(
        '<p style="font-weight:700; font-size:1rem; color:#0f172a; margin-bottom:1rem;">'
        'Trạng thái Server</p>',
        unsafe_allow_html=True,
    )

    st.markdown("""
        <div class="card" style="margin-bottom:1.5rem;">
            <p class="section-label">Kiến trúc hệ thống</p>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem; margin-top:0.5rem;">
                <div>
                    <div style="display:flex; align-items:flex-start; gap:0.5rem; margin-bottom:0.5rem;">
                        <div style="width:10px;height:10px;border-radius:50%;background:#10b981;
                             flex-shrink:0;margin-top:4px;"></div>
                        <p style="color:#334155;font-size:0.875rem;margin:0;line-height:1.4;">
                            2 khu vực: <strong>Miền Nam</strong> (TP.HCM) và <strong>Miền Bắc</strong> (Hà Nội)
                        </p>
                    </div>
                    <div style="display:flex; align-items:flex-start; gap:0.5rem;">
                        <div style="width:10px;height:10px;border-radius:50%;background:#0ea5e9;
                             flex-shrink:0;margin-top:4px;"></div>
                        <p style="color:#334155;font-size:0.875rem;margin:0;line-height:1.4;">
                            Mỗi khu vực: 1 Primary + 1 Replica (Master-Slave)
                        </p>
                    </div>
                </div>
                <div>
                    <div style="display:flex; align-items:flex-start; gap:0.5rem; margin-bottom:0.5rem;">
                        <div style="width:10px;height:10px;border-radius:50%;background:#f59e0b;
                             flex-shrink:0;margin-top:4px;"></div>
                        <p style="color:#334155;font-size:0.875rem;margin:0;line-height:1.4;">
                            Định tuyến tự động theo GPS / Tỉnh-Thành phố
                        </p>
                    </div>
                    <div style="display:flex; align-items:flex-start; gap:0.5rem;">
                        <div style="width:10px;height:10px;border-radius:50%;background:#ef4444;
                             flex-shrink:0;margin-top:4px;"></div>
                        <p style="color:#334155;font-size:0.875rem;margin:0;line-height:1.4;">
                            Primary sập → Failover sang Replica (Read-Only)
                        </p>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    status = get_server_status()

    for region, cfg in SERVER_CONFIG.items():
        region_label = REGION_LABELS[region]
        primary_up   = status.get(f"{region}_primary", True)
        replica_up   = status.get(f"{region}_replica", True)

        st.markdown(
            f'<p style="font-weight:700; color:#0f172a; font-size:0.95rem; margin:1rem 0 0.5rem;">'
            f'{region_label}</p>',
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)
        with c1:
            cls = "online" if primary_up else "offline"
            cap = "Đọc + Ghi (Read / Write)" if primary_up else "Offline — Failover sang Replica"
            st.markdown(f"""
                <div class="server-card {cls}">
                    <p class="server-type">PRIMARY (Master)</p>
                    <p class="server-name">{cfg['label']}</p>
                    <p style="margin:0.3rem 0 0.4rem;">{_dot(primary_up)}</p>
                    <p class="server-detail">{cap}</p>
                </div>
            """, unsafe_allow_html=True)

        with c2:
            cls = "online" if replica_up else "offline"
            cap = "Chỉ đọc (đồng bộ từ Primary)" if replica_up else "Offline"
            st.markdown(f"""
                <div class="server-card {cls}">
                    <p class="server-type">REPLICA (Slave)</p>
                    <p class="server-name">{cfg['label']} — Replica</p>
                    <p style="margin:0.3rem 0 0.4rem;">{_dot(replica_up)}</p>
                    <p class="server-detail">{cap}</p>
                </div>
            """, unsafe_allow_html=True)

        try:
            db    = get_connection(region)
            badge = (
                '<span class="badge badge-amber">Failover</span>'
                if db.is_failover
                else '<span class="badge badge-green">Bình thường</span>'
            )
            st.markdown(
                f'<p style="color:#64748b;font-size:0.8rem;margin:0.5rem 0 0;">'
                f'Kết nối hiện tại: <strong style="color:#0f172a;">{db.server_label}</strong>'
                f' &nbsp; {badge}</p>',
                unsafe_allow_html=True,
            )
        except ConnectionError as e:
            st.markdown(
                f'<div class="alert alert-err" style="margin-top:0.5rem;">{e}</div>',
                unsafe_allow_html=True,
            )

        try:
            raw = _get_raw_connection(cfg["primary"])
            cur = raw.cursor()
            cur.execute("SELECT COUNT(*) FROM rides")
            ride_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM users")
            user_count = cur.fetchone()[0]
            st.caption(f"Primary DB: {ride_count} chuyến đi, {user_count} người dùng")
        except Exception:
            pass

        st.markdown("")


# ──────────────────────────────────────────────────────────────
def _tab_failover():
    st.markdown("""
        <p style="font-weight:700; font-size:1rem; color:#0f172a; margin-bottom:0.25rem;">
            Demo Failover
        </p>
        <p style="color:#64748b; font-size:0.875rem; margin-bottom:1.25rem;">
            Bật / tắt các server để demo
            <strong style="color:#0f172a;">Automatic Failover</strong>.
            Khi Primary sập, ứng dụng tự chuyển sang Replica (Read-Only).
        </p>
    """, unsafe_allow_html=True)

    status = get_server_status()

    servers = [
        ("south_primary", "Miền Nam — Primary (Master)", "#10b981"),
        ("south_replica", "Miền Nam — Replica (Slave)",  "#0ea5e9"),
        ("north_primary", "Miền Bắc — Primary (Master)", "#10b981"),
        ("north_replica", "Miền Bắc — Replica (Slave)",  "#0ea5e9"),
    ]

    # ── Bảng điều khiển ──
    st.markdown("""
        <div style="background:#f8fafc; border:1.5px solid #e2e8f0;
             border-radius:12px; overflow:hidden; margin-bottom:1.5rem;">
            <div style="background:#f1f5f9; padding:0.6rem 1.25rem;
                 display:grid; grid-template-columns:3fr 1.5fr 1.5fr;
                 font-size:0.72rem; font-weight:700; text-transform:uppercase;
                 letter-spacing:0.06em; color:#64748b;">
                <span>Server</span><span>Trạng thái</span><span>Điều khiển</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    for key, label, color in servers:
        is_up = status.get(key, True)
        col_label, col_status, col_btn = st.columns([3, 1.5, 1.5])

        col_label.markdown(f"""
            <p style="color:#0f172a; font-weight:600; font-size:0.875rem;
               margin:0; padding-top:0.4rem;">
                <span style="display:inline-block;width:8px;height:8px;border-radius:50%;
                      background:{color};margin-right:6px;vertical-align:middle;"></span>
                {label}
            </p>
        """, unsafe_allow_html=True)

        col_status.markdown(
            f'<p style="padding-top:0.4rem; font-size:0.875rem;">{_dot(is_up)}</p>',
            unsafe_allow_html=True,
        )

        btn_lbl  = "Tắt server" if is_up else "Bật server"
        btn_type = "secondary"  if is_up else "primary"
        if col_btn.button(btn_lbl, key=f"tog_{key}", type=btn_type):
            set_server_status(key, not is_up)
            st.success(f"Đã {'tắt' if is_up else 'bật'}: {label}")
            st.rerun()

    st.markdown("---")

    # ── Kịch bản nhanh ──
    st.markdown(
        '<p style="font-weight:700; font-size:0.95rem; color:#0f172a; margin-bottom:0.75rem;">'
        'Kịch bản Demo nhanh</p>',
        unsafe_allow_html=True,
    )
    sc1, sc2, sc3 = st.columns(3)

    if sc1.button("Reset — Tất cả Online", use_container_width=True, type="primary"):
        for key, _, _ in servers:
            set_server_status(key, True)
        st.success("Tất cả server đã online.")
        st.rerun()

    if sc2.button("Tắt Primary Miền Nam", use_container_width=True):
        set_server_status("south_primary", False)
        st.warning("Primary Miền Nam đã tắt → Failover sang Replica (Read-Only).")
        st.rerun()

    if sc3.button("Tắt Primary Miền Bắc", use_container_width=True):
        set_server_status("north_primary", False)
        st.warning("Primary Miền Bắc đã tắt → Failover sang Replica (Read-Only).")
        st.rerun()

    st.markdown("---")

    # ── Kiểm chứng Read-Only ──
    st.markdown(
        '<p style="font-weight:700; font-size:0.95rem; color:#0f172a; margin-bottom:0.5rem;">'
        'Kiểm chứng chế độ Read-Only</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#64748b; font-size:0.85rem; margin-bottom:0.75rem;">'
        'Khi Primary sập, thử ghi vào Replica để xem thông báo lỗi:</p>',
        unsafe_allow_html=True,
    )

    demo_region = st.selectbox(
        "Chọn khu vực kiểm tra:",
        ["south", "north"],
        format_func=lambda x: REGION_LABELS[x],
    )

    col_r, col_w = st.columns(2)

    if col_r.button("Thử đọc (SELECT)", use_container_width=True, type="primary"):
        try:
            db   = get_connection(demo_region)
            rows = db.fetchall(
                "SELECT code, status, fare FROM rides WHERE region=%s LIMIT 3",
                (demo_region,),
            )
            st.success(f"Đọc thành công từ **{db.server_label}**")
            for r in rows:
                st.code(f"Mã: {r['code']} | Trạng thái: {r['status']} | Cước: {r['fare']:,}đ")
        except ConnectionError as e:
            st.markdown(f'<div class="alert alert-err">{e}</div>', unsafe_allow_html=True)

    if col_w.button("Thử ghi (INSERT)", use_container_width=True):
        try:
            db = get_connection(demo_region)
            db.execute(
                "INSERT INTO rides (code,user_id,pickup_location,dropoff_location,"
                "fare,status,region) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                ("TEST-000", 1, "Test A", "Test B", 10000, "ongoing", demo_region),
            )
            db.commit()
            st.success("Ghi thành công (Primary đang online).")
            db.execute("DELETE FROM rides WHERE code='TEST-000'")
            db.commit()
        except PermissionError as e:
            st.markdown(f'<div class="alert alert-warn">{e}</div>', unsafe_allow_html=True)
        except ConnectionError as e:
            st.markdown(f'<div class="alert alert-err">{e}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Lỗi: {e}")


# ──────────────────────────────────────────────────────────────
def _tab_replication():
    st.markdown(
        '<p style="font-weight:700; font-size:1rem; color:#0f172a; margin-bottom:0.5rem;">'
        'Master-Slave Replication</p>',
        unsafe_allow_html=True,
    )

    steps = [
        ("#dcfce7", "#166534", "Mọi thao tác <strong>ghi</strong> (INSERT / UPDATE / DELETE) đều vào <strong>Primary</strong>"),
        ("#dbeafe", "#1e40af", "Primary đồng bộ dữ liệu sang <strong>Replica</strong> theo chu kỳ"),
        ("#fef3c7", "#92400e", "Replica chỉ phục vụ <strong>đọc</strong> (SELECT)"),
        ("#fee2e2", "#991b1b", "Thực tế: dùng MySQL Binlog Replication / PostgreSQL Streaming Replication"),
    ]

    st.markdown('<div class="card" style="margin-bottom:1.5rem;"><p class="section-label">Cơ chế hoạt động</p><div style="margin-top:0.5rem;">', unsafe_allow_html=True)
    for i, (bg, color, text) in enumerate(steps, 1):
        st.markdown(f"""
            <div style="display:flex; gap:0.75rem; align-items:flex-start; margin-bottom:0.6rem;">
                <span style="background:{bg};color:{color};font-size:0.72rem;font-weight:800;
                      padding:2px 8px;border-radius:12px;white-space:nowrap;margin-top:1px;">{i}</span>
                <p style="color:#334155; font-size:0.875rem; margin:0; line-height:1.5;">{text}</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

    col_sync, _ = st.columns([1, 2])
    if col_sync.button("Đồng bộ tất cả Replica", type="primary", use_container_width=True):
        with st.spinner("Đang đồng bộ..."):
            replicate_all()
            time.sleep(0.5)
        st.success("Replication hoàn tất! Tất cả Replica đã được cập nhật.")

    st.markdown("---")
    st.markdown(
        '<p style="font-weight:700; font-size:0.95rem; color:#0f172a; margin-bottom:0.75rem;">'
        'So sánh dữ liệu Primary vs Replica</p>',
        unsafe_allow_html=True,
    )

    for region, cfg in SERVER_CONFIG.items():
        st.markdown(
            f'<p style="font-weight:700; color:#0f172a; font-size:0.875rem; margin-top:0.5rem;">'
            f'{REGION_LABELS[region]}</p>',
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns(2)

        for col, db_cfg, label in [(c1, cfg["primary"], "Primary"), (c2, cfg["replica"], "Replica")]:
            try:
                raw = _get_raw_connection(db_cfg)
                cur = raw.cursor(dictionary=True)
                cur.execute("SELECT COUNT(*) AS cnt FROM rides")
                ride_count = cur.fetchone()["cnt"]
                cur.execute("SELECT COUNT(*) AS cnt FROM users")
                user_count = cur.fetchone()["cnt"]
                cur.execute("SELECT code, created_at FROM rides ORDER BY ride_id DESC LIMIT 1")
                latest = cur.fetchone()

                is_primary   = (label == "Primary")
                border_color = "#10b981" if is_primary else "#0ea5e9"
                mode_badge   = (
                    '<span class="badge badge-green">Đọc + Ghi</span>'
                    if is_primary
                    else '<span class="badge badge-blue">Chỉ đọc</span>'
                )

                col.markdown(f"""
                    <div class="server-card" style="border-left:4px solid {border_color};">
                        <div style="display:flex; justify-content:space-between;
                             align-items:center; margin-bottom:0.75rem;">
                            <p class="server-type" style="margin:0;">{label}</p>
                            {mode_badge}
                        </div>
                        <div class="stat-grid" style="grid-template-columns:1fr 1fr;">
                            <div>
                                <p class="stat-label">Chuyến đi</p>
                                <p class="stat-value">{ride_count}</p>
                            </div>
                            <div>
                                <p class="stat-label">Người dùng</p>
                                <p class="stat-value">{user_count}</p>
                            </div>
                        </div>
                        <p style="color:#94a3b8;font-size:0.75rem;margin:0.6rem 0 0;">
                            Mới nhất: {latest['code'] if latest else '—'}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                col.caption(f"{label}: chưa khởi tạo hoặc lỗi ({e})")

        st.markdown("")


# ──────────────────────────────────────────────────────────────
def _tab_testcases():
    st.markdown("""
        <p style="font-weight:700; font-size:1rem; color:#0f172a; margin-bottom:0.25rem;">
            Test Cases
        </p>
        <p style="color:#64748b; font-size:0.875rem; margin-bottom:1.25rem;">
            Kiểm tra các yêu cầu chính của đồ án.
            Nhấn <strong style="color:#0f172a;">Chạy test</strong> để thực thi.
        </p>
    """, unsafe_allow_html=True)

    tests = [
        {"id":"TC-01","name":"Định tuyến theo vị trí — Miền Nam",
         "desc":"Người dùng chọn TP.HCM → kết nối Server Miền Nam","fn":_tc_routing_south},
        {"id":"TC-02","name":"Định tuyến theo vị trí — Miền Bắc",
         "desc":"Người dùng chọn Hà Nội → kết nối Server Miền Bắc","fn":_tc_routing_north},
        {"id":"TC-03","name":"Failover — Đọc khi Primary sập",
         "desc":"Tắt Primary Miền Nam → vẫn đọc được dữ liệu từ Replica","fn":_tc_failover_read},
        {"id":"TC-04","name":"Read-Only — Chặn ghi khi dùng Replica",
         "desc":"Khi dùng Replica, thao tác INSERT phải bị từ chối","fn":_tc_readonly_write},
        {"id":"TC-05","name":"Replication — Dữ liệu đồng bộ Primary → Replica",
         "desc":"Ghi vào Primary, sync, kiểm tra Replica có bản ghi mới","fn":_tc_replication},
        {"id":"TC-06","name":"Cả hai server đều sập — Báo lỗi đúng",
         "desc":"Tắt cả Primary & Replica → phải báo ConnectionError","fn":_tc_both_down},
    ]

    for t in tests:
        with st.expander(f"{t['id']} — {t['name']}", expanded=False):
            st.markdown(
                f'<p style="color:#64748b;font-size:0.85rem;font-style:italic;'
                f'margin-bottom:0.75rem;">{t["desc"]}</p>',
                unsafe_allow_html=True,
            )
            if st.button(f"Chạy {t['id']}", key=f"run_{t['id']}", type="primary"):
                with st.spinner("Đang chạy..."):
                    result, passed, detail = t["fn"]()
                if passed:
                    st.markdown(
                        f'<div class="alert alert-ok"><strong>PASSED</strong> — {result}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="alert alert-err"><strong>FAILED</strong> — {result}</div>',
                        unsafe_allow_html=True,
                    )
                if detail:
                    st.code(detail)


# ── Test implementations ─────────────────────────────────────
def _tc_routing_south():
    try:
        set_server_status("south_primary", True)
        db = get_connection("south")
        return (
            f"Kết nối tới: {db.server_label}",
            not db.is_failover,
            f"server_label = '{db.server_label}'\nis_failover = {db.is_failover}",
        )
    except Exception as e:
        return str(e), False, None


def _tc_routing_north():
    try:
        set_server_status("north_primary", True)
        db = get_connection("north")
        return (
            f"Kết nối tới: {db.server_label}",
            not db.is_failover,
            f"server_label = '{db.server_label}'\nis_failover = {db.is_failover}",
        )
    except Exception as e:
        return str(e), False, None


def _tc_failover_read():
    try:
        set_server_status("south_primary", False)
        set_server_status("south_replica", True)
        replicate_all()
        db   = get_connection("south")
        rows = db.fetchall("SELECT code, status FROM rides WHERE region='south' LIMIT 3")
        set_server_status("south_primary", True)
        detail = "\n".join(f"{r['code']} — {r['status']}" for r in rows)
        return (
            f"Đọc được {len(rows)} bản ghi từ Replica",
            db.is_failover and len(rows) > 0,
            f"Kết nối: {db.server_label}\n---\n{detail}",
        )
    except Exception as e:
        set_server_status("south_primary", True)
        return str(e), False, None


def _tc_readonly_write():
    try:
        set_server_status("south_primary", False)
        set_server_status("south_replica", True)
        replicate_all()
        db = get_connection("south")
        try:
            db.execute(
                "INSERT INTO rides (code,user_id,pickup_location,dropoff_location,"
                "fare,status,region) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                ("TC04-TEST", 1, "A", "B", 1000, "ongoing", "south"),
            )
            set_server_status("south_primary", True)
            return "Ghi thành công — lẽ ra phải bị chặn!", False, None
        except PermissionError as pe:
            set_server_status("south_primary", True)
            return "PermissionError được raise đúng", True, str(pe)
    except Exception as e:
        set_server_status("south_primary", True)
        return str(e), False, None


def _tc_replication():
    import uuid
    test_code = f"SYNC-{uuid.uuid4().hex[:6].upper()}"
    try:
        set_server_status("south_primary", True)
        primary_path = SERVER_CONFIG["south"]["primary"]
        raw_primary  = _get_raw_connection(primary_path)
        cur_primary  = raw_primary.cursor(dictionary=True)
        cur_primary.execute(
            "INSERT IGNORE INTO rides (code,user_id,pickup_location,dropoff_location,"
            "fare,status,region) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (test_code, 1, "Replication Test A", "Replication Test B", 1000, "completed", "south"),
        )
        raw_primary.commit()
        replicate_all()

        replica_path = SERVER_CONFIG["south"]["replica"]
        raw_replica  = _get_raw_connection(replica_path)
        cur_replica  = raw_replica.cursor(dictionary=True)
        cur_replica.execute("SELECT code FROM rides WHERE code=%s", (test_code,))
        row = cur_replica.fetchone()

        cur_primary.execute("DELETE FROM rides WHERE code=%s", (test_code,))
        raw_primary.commit()

        found = row is not None
        return (
            f"Bản ghi '{test_code}' {'tìm thấy' if found else 'KHÔNG tìm thấy'} trong Replica",
            found,
            f"Test code: {test_code}\nReplica result: {dict(row) if row else None}",
        )
    except Exception as e:
        return str(e), False, None


def _tc_both_down():
    try:
        set_server_status("south_primary", False)
        set_server_status("south_replica", False)
        try:
            get_connection("south")
            set_server_status("south_primary", True)
            set_server_status("south_replica", True)
            return "Không raise ConnectionError — lỗi!", False, None
        except ConnectionError as ce:
            set_server_status("south_primary", True)
            set_server_status("south_replica", True)
            return "ConnectionError được raise đúng khi cả hai server sập", True, str(ce)
    except Exception as e:
        set_server_status("south_primary", True)
        set_server_status("south_replica", True)
        return str(e), False, None
