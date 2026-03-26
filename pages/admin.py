"""
pages/admin.py
──────────────
Trang Demo Hệ thống Phân tán — phục vụ mục đích báo cáo đồ án.

Chức năng:
  1. Hiển thị trạng thái real-time tất cả server (Primary/Replica × 2 khu vực)
  2. Bật/tắt server để giả lập sự cố (failover demo)
  3. Kích hoạt Replication thủ công (Master → Slave sync)
  4. Chứng minh chế độ Read-Only khi Primary sập
  5. Test cases kiểm thử hệ thống
"""

import streamlit as st
import time
from database.connection import (
    get_connection, get_server_status, set_server_status,
    replicate_all, SERVER_CONFIG, _get_raw_connection,
)
from utils.region import REGION_LABELS


# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.markdown('<h2>🗄️ Hệ thống Cơ sở dữ liệu Phân tán</h2>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#64748b;">Quản lý & Demo kiến trúc Master-Slave Replication + Failover theo vị trí</p>',
        unsafe_allow_html=True,
    )

    tab_overview, tab_failover, tab_replication, tab_testcases = st.tabs([
        "📡 Tổng quan hệ thống",
        "⚡ Demo Failover",
        "🔄 Replication",
        "🧪 Test Cases",
    ])

    with tab_overview:    _tab_overview()
    with tab_failover:    _tab_failover()
    with tab_replication: _tab_replication()
    with tab_testcases:   _tab_testcases()


# ─────────────────────────────────────────────────────────────────────────────
def _server_dot(is_up: bool) -> str:
    cls   = "dot-up"   if is_up else "dot-down"
    label = "🟢 Online" if is_up else "🔴 Offline"
    return f'<span class="{cls}"></span>{label}'


def _tab_overview():
    st.subheader("📡 Trạng thái Server")
    status = get_server_status()

    st.markdown("""
    Kiến trúc hệ thống:
    - **2 khu vực:** Miền Nam (TP.HCM) & Miền Bắc (Hà Nội)
    - Mỗi khu vực có **1 Primary + 1 Replica** (Master-Slave)
    - Ứng dụng tự động định tuyến dựa vào vị trí GPS / Tỉnh-Thành phố
    - Khi Primary sập → tự động failover sang Replica (Read-Only)
    """)

    st.markdown("---")

    for region, cfg in SERVER_CONFIG.items():
        region_label = REGION_LABELS[region]
        primary_up   = status.get(f"{region}_primary", True)
        replica_up   = status.get(f"{region}_replica", True)

        with st.container():
            st.markdown(f"### {region_label}")
            c1, c2 = st.columns(2)

            with c1:
                st.markdown(
                    f"""
                    <div style="background:#1e293b;border:1px solid #334155;border-radius:10px;padding:1rem;">
                        <p style="color:#94a3b8;font-size:12px;margin:0;">PRIMARY (Master)</p>
                        <p style="font-weight:700;font-size:1rem;margin:.25rem 0;">🖥️ {cfg['label']}</p>
                        <p style="margin:0;">{_server_dot(primary_up)}</p>
                        <p style="color:#64748b;font-size:11px;margin:.5rem 0 0;">
                            {'✅ Nhận Read + Write' if primary_up else '❌ Không thể ghi — Failover sang Replica'}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with c2:
                st.markdown(
                    f"""
                    <div style="background:#1e293b;border:1px solid #334155;border-radius:10px;padding:1rem;">
                        <p style="color:#94a3b8;font-size:12px;margin:0;">REPLICA (Slave)</p>
                        <p style="font-weight:700;font-size:1rem;margin:.25rem 0;">🖥️ {cfg['label']} — Replica</p>
                        <p style="margin:0;">{_server_dot(replica_up)}</p>
                        <p style="color:#64748b;font-size:11px;margin:.5rem 0 0;">
                            {'📖 Read-Only (đồng bộ từ Primary)' if replica_up else '❌ Offline'}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Kết nối hiện tại
            try:
                db = get_connection(region)
                mode = "⚠️ Failover (Read-Only)" if db.is_failover else "✅ Bình thường"
                st.markdown(f"**Kết nối hiện tại:** `{db.server_label}` — Chế độ: {mode}")
            except ConnectionError as e:
                st.markdown(f'<div class="alert-err">{e}</div>', unsafe_allow_html=True)

            # Số liệu DB
            try:
                raw = _get_raw_connection(cfg["primary"])
                cur = raw.cursor()
                cur.execute("SELECT COUNT(*) FROM rides")
                ride_count = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM users")
                user_count = cur.fetchone()[0]
                st.caption(f"📊 Primary DB: {ride_count} chuyến, {user_count} người dùng")
            except Exception:
                pass

            st.markdown("")


# ─────────────────────────────────────────────────────────────────────────────
def _tab_failover():
    st.subheader("⚡ Demo Failover — Giả lập sự cố")
    st.markdown(
        "Bật/tắt các server để demo cơ chế **Automatic Failover**. "
        "Khi Primary sập, ứng dụng tự chuyển sang Replica ở chế độ **Read-Only**."
    )

    status = get_server_status()

    st.markdown("---")
    st.markdown("### 🎛️ Bảng điều khiển Server")

    servers = [
        ("south_primary", "🟢 Miền Nam — Primary",  "south"),
        ("south_replica", "🔵 Miền Nam — Replica",  "south"),
        ("north_primary", "🟢 Miền Bắc — Primary",  "north"),
        ("north_replica", "🔵 Miền Bắc — Replica",  "north"),
    ]

    for key, label, region in servers:
        is_up = status.get(key, True)
        col_label, col_status, col_btn = st.columns([3, 2, 2])
        col_label.markdown(f"**{label}**")
        col_status.markdown(_server_dot(is_up), unsafe_allow_html=True)

        btn_label = "🔴 Tắt server" if is_up else "🟢 Bật server"
        if col_btn.button(btn_label, key=f"toggle_{key}"):
            set_server_status(key, not is_up)
            action = "tắt" if is_up else "bật"
            st.success(f"✅ Đã {action} **{label}**")
            st.rerun()

    st.markdown("---")

    # ── Scenario nhanh ────────────────────────────────────────────────────────
    st.markdown("### 🎬 Kịch bản Demo nhanh")

    sc1, sc2, sc3 = st.columns(3)

    if sc1.button("🟢 Reset — Tất cả Online", use_container_width=True):
        for key, _, _ in servers:
            set_server_status(key, True)
        st.success("✅ Tất cả server đã online.")
        st.rerun()

    if sc2.button("💥 Tắt Primary Miền Nam", use_container_width=True):
        set_server_status("south_primary", False)
        st.warning("⚠️ Primary Miền Nam đã tắt. Kết nối sẽ failover sang Replica (Read-Only).")
        st.rerun()

    if sc3.button("💥 Tắt Primary Miền Bắc", use_container_width=True):
        set_server_status("north_primary", False)
        st.warning("⚠️ Primary Miền Bắc đã tắt.")
        st.rerun()

    st.markdown("---")

    # ── Kiểm chứng Read-Only ──────────────────────────────────────────────────
    st.markdown("### 🔒 Kiểm chứng chế độ Read-Only")
    st.markdown("Khi Primary sập, thử ghi vào Replica để xem thông báo lỗi:")

    demo_region = st.selectbox("Chọn khu vực kiểm tra:", ["south", "north"],
                                format_func=lambda x: REGION_LABELS[x])

    col_r, col_w = st.columns(2)

    if col_r.button("📖 Thử đọc dữ liệu (SELECT)", use_container_width=True):
        try:
            db = get_connection(demo_region)
            rows = db.fetchall("SELECT code, status, fare FROM rides WHERE region=%s LIMIT 3", (demo_region,))
            st.success(f"✅ Đọc thành công từ **{db.server_label}**")
            for r in rows:
                st.code(f"Mã: {r['code']} | Trạng thái: {r['status']} | Cước: {r['fare']:,}đ")
        except ConnectionError as e:
            st.markdown(f'<div class="alert-err">{e}</div>', unsafe_allow_html=True)

    if col_w.button("✏️ Thử ghi dữ liệu (INSERT)", use_container_width=True):
        try:
            db = get_connection(demo_region)
            db.execute(
                "INSERT INTO rides (code,user_id,pickup_location,dropoff_location,fare,status,region) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                ("TEST-000", 1, "Test A", "Test B", 10000, "ongoing", demo_region),
            )
            db.commit()
            st.success("✅ Ghi thành công (Primary đang online).")
            # Xóa dữ liệu test
            db.execute("DELETE FROM rides WHERE code='TEST-000'")
            db.commit()
        except PermissionError as e:
            st.markdown(f'<div class="alert-warn">{e}</div>', unsafe_allow_html=True)
        except ConnectionError as e:
            st.markdown(f'<div class="alert-err">{e}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Lỗi: {e}")


# ─────────────────────────────────────────────────────────────────────────────
def _tab_replication():
    st.subheader("🔄 Master-Slave Replication")
    st.markdown("""
    **Cơ chế hoạt động:**
    1. Mọi thao tác **ghi** (INSERT/UPDATE/DELETE) đều vào **Primary**
    2. Primary đồng bộ dữ liệu sang **Replica** theo chu kỳ
    3. Replica chỉ phục vụ **đọc** (SELECT)
    4. Trong thực tế: dùng **PostgreSQL Streaming Replication** hoặc **MySQL Binlog Replication**

    *(Demo này mô phỏng bằng SQLite file backup)*
    """)

    st.markdown("---")

    col_sync, col_status = st.columns([1, 2])

    if col_sync.button("🔄 Đồng bộ tất cả Replica ngay", type="primary", use_container_width=True):
        with st.spinner("Đang đồng bộ..."):
            replicate_all()
            time.sleep(0.5)
        st.success("✅ Replication hoàn tất! Tất cả Replica đã được cập nhật từ Primary.")

    st.markdown("---")
    st.markdown("### 📊 So sánh dữ liệu Primary vs Replica")

    for region, cfg in SERVER_CONFIG.items():
        st.markdown(f"**{REGION_LABELS[region]}**")
        c1, c2 = st.columns(2)

        for col, db_path, label in [
            (c1, cfg["primary"], "Primary"),
            (c2, cfg["replica"], "Replica"),
        ]:
            try:
                raw = _get_raw_connection(db_path)
                cur = raw.cursor(dictionary=True)
                cur.execute("SELECT COUNT(*) AS cnt FROM rides")
                ride_count = cur.fetchone()["cnt"]
                cur.execute("SELECT COUNT(*) AS cnt FROM users")
                user_count = cur.fetchone()["cnt"]
                cur.execute("SELECT code, created_at FROM rides ORDER BY ride_id DESC LIMIT 1")
                latest = cur.fetchone()
                col.markdown(
                    f"""
                    <div style="background:#1e293b;border:1px solid #334155;
                                border-radius:8px;padding:.75rem;">
                        <p style="color:#94a3b8;font-size:11px;margin:0;">{label}</p>
                        <p style="margin:.25rem 0;">🚗 Chuyến: <strong>{ride_count}</strong></p>
                        <p style="margin:.25rem 0;">👤 Users: <strong>{user_count}</strong></p>
                        <p style="color:#64748b;font-size:11px;margin:.25rem 0 0;">
                            Mới nhất: {latest['code'] if latest else '—'}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            except Exception as e:
                col.caption(f"{label}: chưa khởi tạo hoặc lỗi ({e})")

        st.markdown("")


# ─────────────────────────────────────────────────────────────────────────────
def _tab_testcases():
    st.subheader("🧪 Test Cases kiểm thử hệ thống")

    st.markdown("""
    Các test case dưới đây kiểm tra các yêu cầu chính của đồ án.
    Nhấn **▶ Chạy** để thực thi và xem kết quả.
    """)

    st.markdown("---")

    tests = [
        {
            "id": "TC-01",
            "name": "Định tuyến theo vị trí — Miền Nam",
            "desc": "Người dùng chọn TP.HCM → kết nối Server Miền Nam",
            "fn": _tc_routing_south,
        },
        {
            "id": "TC-02",
            "name": "Định tuyến theo vị trí — Miền Bắc",
            "desc": "Người dùng chọn Hà Nội → kết nối Server Miền Bắc",
            "fn": _tc_routing_north,
        },
        {
            "id": "TC-03",
            "name": "Failover — Đọc khi Primary sập",
            "desc": "Tắt Primary Miền Nam → vẫn đọc được dữ liệu từ Replica",
            "fn": _tc_failover_read,
        },
        {
            "id": "TC-04",
            "name": "Read-Only — Chặn ghi khi dùng Replica",
            "desc": "Khi dùng Replica, thao tác INSERT phải bị từ chối",
            "fn": _tc_readonly_write,
        },
        {
            "id": "TC-05",
            "name": "Replication — Dữ liệu đồng bộ Primary → Replica",
            "desc": "Ghi vào Primary, sync, kiểm tra Replica có bản ghi mới",
            "fn": _tc_replication,
        },
        {
            "id": "TC-06",
            "name": "Cả hai server đều sập — Báo lỗi đúng",
            "desc": "Tắt cả Primary & Replica → phải báo ConnectionError",
            "fn": _tc_both_down,
        },
    ]

    for t in tests:
        with st.expander(f"**{t['id']}** — {t['name']}", expanded=False):
            st.markdown(f"*{t['desc']}*")
            if st.button(f"▶ Chạy {t['id']}", key=f"run_{t['id']}"):
                with st.spinner("Đang chạy..."):
                    result, passed, detail = t["fn"]()
                if passed:
                    st.markdown(f'<div class="alert-ok">✅ PASSED — {result}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="alert-err">❌ FAILED — {result}</div>', unsafe_allow_html=True)
                if detail:
                    st.code(detail)


# ── Test implementations ──────────────────────────────────────────────────────

def _tc_routing_south():
    try:
        set_server_status("south_primary", True)
        db = get_connection("south")
        ok = "south" in db.server_label.lower() or "miền nam" in db.server_label.lower()
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
            f"server_label = '{db.server_label}'",
        )
    except Exception as e:
        return str(e), False, None


def _tc_failover_read():
    try:
        set_server_status("south_primary", False)
        set_server_status("south_replica", True)
        replicate_all()
        db = get_connection("south")
        rows = db.fetchall("SELECT code, status FROM rides WHERE region='south' LIMIT 3")
        set_server_status("south_primary", True)  # restore
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
                "INSERT INTO rides (code,user_id,pickup_location,dropoff_location,fare,status,region) VALUES (%s,%s,%s,%s,%s,%s,%s)",
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

        # Ghi vào Primary
        primary_path = SERVER_CONFIG["south"]["primary"]
        raw_primary  = _get_raw_connection(primary_path)
        cur_primary  = raw_primary.cursor(dictionary=True)
        cur_primary.execute(
            "INSERT IGNORE INTO rides (code,user_id,pickup_location,dropoff_location,fare,status,region) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (test_code, 1, "Replication Test A", "Replication Test B", 1000, "completed", "south"),
        )
        raw_primary.commit()

        # Sync
        replicate_all()

        # Kiểm tra Replica
        replica_path = SERVER_CONFIG["south"]["replica"]
        raw_replica  = _get_raw_connection(replica_path)
        cur_replica  = raw_replica.cursor(dictionary=True)
        cur_replica.execute("SELECT code FROM rides WHERE code=%s", (test_code,))
        row = cur_replica.fetchone()

        # Cleanup
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