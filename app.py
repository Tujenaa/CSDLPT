"""
app.py — Entry point chính của ứng dụng GoX Ride (Streamlit)
──────────────────────────────────────────────────────────────
Chạy:  streamlit run app.py
"""

import streamlit as st
import sys
import os

# Đảm bảo import path đúng
sys.path.insert(0, os.path.dirname(__file__))
from utils.region import REGION_LABELS, REGION_COLORS, ALL_PROVINCES, get_region_from_province

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GoX Ride",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS toàn cục ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Font & base ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Ẩn decoration mặc định ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] { background: #0f172a; }
section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stRadio label { color: #94a3b8 !important; }

/* ── Metric cards ── */
div[data-testid="metric-container"] {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 1rem;
}

/* ── Status badges ── */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}
.badge-completed { background:#dcfce7; color:#166534; }
.badge-cancelled { background:#fee2e2; color:#991b1b; }
.badge-ongoing   { background:#dbeafe; color:#1e40af; }

/* ── Ride card ── */
.ride-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    transition: border-color .2s;
}
.ride-card:hover { border-color: #22c55e; }

/* ── Server status dot ── */
.dot-up   { display:inline-block; width:10px; height:10px; border-radius:50%; background:#22c55e; margin-right:6px; }
.dot-down { display:inline-block; width:10px; height:10px; border-radius:50%; background:#ef4444; margin-right:6px; }

/* ── Alert boxes ── */
.alert-warn {
    background: #fef3c7; border-left: 4px solid #f59e0b;
    padding: .75rem 1rem; border-radius: 6px; color: #92400e;
    margin-bottom: 1rem;
}
.alert-err {
    background: #fee2e2; border-left: 4px solid #ef4444;
    padding: .75rem 1rem; border-radius: 6px; color: #991b1b;
    margin-bottom: 1rem;
}
.alert-ok {
    background: #dcfce7; border-left: 4px solid #22c55e;
    padding: .75rem 1rem; border-radius: 6px; color: #166534;
    margin-bottom: 1rem;
}

/* ── Big title ── */
.app-title {
    font-size: 2rem; font-weight: 700;
    background: linear-gradient(135deg, #22c55e, #3b82f6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)


# ── Khởi tạo session state ────────────────────────────────────────────────────
def init_state():
    defaults = {
        "logged_in":      False,
        "user_id":        None,
        "user_name":      "Khách",
        "user_phone":     "",
        "user_region":    "south",
        "current_page":   "login",
        "location_set":   False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()




# ── Navigation ────────────────────────────────────────────────────────────────
def nav():
    with st.sidebar:
        st.markdown('<p class="app-title">🚗 GoX</p>', unsafe_allow_html=True)
        st.markdown("---")

        current = st.session_state.current_page

        if st.session_state.logged_in:
            region = st.session_state.user_region
            label  = REGION_LABELS[region]
            color  = REGION_COLORS[region]
            st.markdown(f"👤 **{st.session_state.user_name}**")
            st.markdown(
                f'<span style="color:{color};font-weight:600;">{label}</span>',
                unsafe_allow_html=True,
            )
            st.markdown("---")

            auth_pages = {
                "🏠 Đặt xe":         "book",
                "📋 Lịch sử chuyến": "history",
                "👤 Hồ sơ":          "profile",
            }
            for label_page, key in auth_pages.items():
                is_active = current == key
                btn_style = "primary" if is_active else "secondary"
                if st.button(label_page, key=f"nav_{key}", use_container_width=True, type=btn_style):
                    st.session_state.current_page = key
                    st.rerun()

            st.markdown("---")
            if st.button("🚪 Đăng xuất", use_container_width=True):
                for k in ["logged_in", "user_id", "user_name", "user_phone"]:
                    st.session_state[k] = False if k == "logged_in" else None if "id" in k else ""
                st.session_state.current_page = "login"
                st.rerun()
        else:
            if st.button("🔑 Đăng nhập", use_container_width=True):
                st.session_state.current_page = "login"
                st.rerun()
            if st.button("📝 Đăng ký",   use_container_width=True):
                st.session_state.current_page = "register"
                st.rerun()

        # ── Luôn hiển thị nút Hệ thống phân tán ────────────────────────────
        st.markdown("---")
        is_active = current == "admin"
        btn_style = "primary" if is_active else "secondary"
        if st.button("🗄️ Hệ thống phân tán", key="nav_admin", use_container_width=True, type=btn_style):
            st.session_state.current_page = "admin"
            st.rerun()

        st.markdown("---")
        st.caption("CSDL Phân tán — Đồ án")


nav()

# ── Page Router ──────────────────────────────────────────────────────────────
page = st.session_state.current_page

# Bảo vệ route: nếu chưa login và cố truy cập trang cần auth
protected = {"book", "history", "profile"}
if page in protected and not st.session_state.logged_in:
    st.session_state.current_page = "login"
    page = "login"

if   page == "login":    from pages.login    import render; render()
elif page == "register": from pages.register import render; render()
elif page == "book":     from pages.book     import render; render()
elif page == "history":  from pages.history  import render; render()
elif page == "profile":  from pages.profile  import render; render()
elif page == "admin":    from pages.admin    import render; render()
else:
    st.error("Trang không tồn tại.")