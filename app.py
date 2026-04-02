"""
app.py — GoRide · Ứng dụng Gọi xe Phân tán
Chạy: streamlit run app.py
"""

import streamlit as st
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from utils.region import REGION_LABELS, REGION_COLORS, ALL_PROVINCES, get_region_from_province

st.set_page_config(
    page_title="GoRide — Gọi xe thông minh",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ════════════════════════════════════════════════════════════
# GLOBAL CSS — Professional Light Theme, no icons
# ════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hide auto-generated Streamlit multi-page nav (pages/ folder) ── */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
[data-testid="stSidebarNavSeparator"],
section[data-testid="stSidebar"] nav,
section[data-testid="stSidebar"] ul,
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] > div:first-child > div:first-child > div:first-child > ul {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    overflow: hidden !important;
}

.block-container {
    padding: 1.5rem 2rem 2rem !important;
    max-width: 1280px !important;
}



/* ── ROOT TOKENS ── */
:root {
    --bg:           #f0f4f8;
    --bg-white:     #ffffff;
    --bg-surface:   #f8fafc;
    --sidebar-bg:   #0f172a;
    --border:       #e2e8f0;
    --border-dark:  #cbd5e1;
    --text-head:    #0f172a;
    --text-body:    #334155;
    --text-muted:   #64748b;
    --text-xmuted:  #94a3b8;
    --accent:       #0ea5e9;
    --accent-dark:  #0284c7;
    --accent-dim:   rgba(14,165,233,0.10);
    --green:        #10b981;
    --green-dim:    rgba(16,185,129,0.10);
    --red:          #ef4444;
    --red-dim:      rgba(239,68,68,0.10);
    --amber:        #f59e0b;
    --amber-dim:    rgba(245,158,11,0.10);
    --radius-sm:    8px;
    --radius:       12px;
    --radius-lg:    16px;
    --shadow-sm:    0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04);
    --shadow:       0 4px 16px rgba(0,0,0,0.08);
    --shadow-lg:    0 8px 32px rgba(0,0,0,0.10);
}

/* ── App background ── */
.stApp { background: var(--bg) !important; }

/* ═══════════════════════════════════
   SIDEBAR — Dark Navy
═══════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
section[data-testid="stSidebar"] * { color: #94a3b8 !important; }

/* Override Streamlit sidebar element backgrounds */
section[data-testid="stSidebar"] .stSelectbox > div > div,
section[data-testid="stSidebar"] .stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border-color: rgba(255,255,255,0.1) !important;
    color: #f1f5f9 !important;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.08) !important;
    margin: 0.6rem 0 !important;
}

/* ── Sidebar nav buttons ── */
section[data-testid="stSidebar"] button {
    background: transparent !important;
    border: none !important;
    color: #94a3b8 !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    text-align: left !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.55rem 0.85rem !important;
    transition: all 0.18s ease !important;
    width: 100% !important;
}
section[data-testid="stSidebar"] button:hover {
    background: rgba(14,165,233,0.12) !important;
    color: #e2e8f0 !important;
}
section[data-testid="stSidebar"] button[kind="primary"] {
    background: rgba(14,165,233,0.15) !important;
    color: #38bdf8 !important;
    font-weight: 600 !important;
}

/* ═══════════════════════════════════
   MAIN BUTTONS
═══════════════════════════════════ */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent), var(--accent-dark)) !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    color: white !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.65rem 1.5rem !important;
    letter-spacing: 0.01em !important;
    transition: all 0.22s ease !important;
    box-shadow: 0 2px 8px rgba(14,165,233,0.35) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(14,165,233,0.45) !important;
}
.stButton > button[kind="secondary"] {
    background: var(--bg-white) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-body) !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 500 !important;
    transition: all 0.18s ease !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

/* ═══════════════════════════════════
   FORM ELEMENTS
═══════════════════════════════════ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    background: var(--bg-white) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-body) !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 0.85rem !important;
    transition: all 0.18s ease !important;
    box-shadow: var(--shadow-sm) !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-dim) !important;
    outline: none !important;
}
.stTextInput label, .stTextArea label, .stNumberInput label,
.stSelectbox label, .stDateInput label, .stTimeInput label,
.stRadio label p {
    color: var(--text-body) !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: var(--bg-white) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-body) !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ── Form container ── */
[data-testid="stForm"] {
    background: var(--bg-white) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.75rem !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ── Radio ── */
.stRadio > div { gap: 0.5rem !important; }
.stRadio > div > label {
    background: var(--bg-white) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.5rem 1rem !important;
    cursor: pointer !important;
    transition: all 0.18s ease !important;
}
.stRadio > div > label:has(input:checked) {
    border-color: var(--accent) !important;
    background: var(--accent-dim) !important;
    color: var(--accent-dark) !important;
}

/* ── Metrics ── */
div[data-testid="metric-container"] {
    background: var(--bg-white) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1.25rem 1.5rem !important;
    box-shadow: var(--shadow-sm) !important;
    transition: all 0.2s ease !important;
}
div[data-testid="metric-container"]:hover {
    box-shadow: var(--shadow) !important;
    transform: translateY(-1px) !important;
}
div[data-testid="metric-container"] label {
    color: var(--text-muted) !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.04em !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--text-head) !important;
    font-weight: 700 !important;
    font-size: 1.6rem !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--bg-white) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-body) !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    transition: all 0.18s ease !important;
}
.streamlit-expanderHeader:hover { border-color: var(--accent) !important; }
.streamlit-expanderContent {
    background: var(--bg-white) !important;
    border: 1.5px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius-sm) var(--radius-sm) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-white);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 4px;
    gap: 2px !important;
    box-shadow: var(--shadow-sm);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 6px !important;
    color: var(--text-muted) !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 0.45rem 1.1rem !important;
    background: transparent !important;
    border: none !important;
    transition: all 0.18s ease !important;
}
.stTabs [aria-selected="true"] {
    background: var(--accent-dim) !important;
    color: var(--accent-dark) !important;
    font-weight: 600 !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Checkbox ── */
.stCheckbox label span { color: var(--text-body) !important; font-size: 0.875rem !important; }

/* ── Progress ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent), var(--green)) !important;
    border-radius: 10px !important;
}

/* ── Markdown ── */
.stMarkdown p   { color: var(--text-body); font-size: 0.9rem; }
.stMarkdown strong { color: var(--text-head); }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: var(--text-head) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-dark); border-radius: 3px; }


/* ════════════════════════════════════
   CUSTOM COMPONENTS
════════════════════════════════════ */

/* Page header */
.page-header {
    font-size: 1.65rem;
    font-weight: 800;
    color: var(--text-head);
    margin: 0 0 0.25rem;
    letter-spacing: -0.02em;
}
.page-subtitle {
    font-size: 0.875rem;
    color: var(--text-muted);
    margin: 0 0 1.5rem;
}

/* Card */
.card {
    background: var(--bg-white);
    border: 1.5px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 1rem;
}
.card-sm {
    background: var(--bg-white);
    border: 1.5px solid var(--border);
    border-radius: var(--radius);
    padding: 1.1rem 1.3rem;
    box-shadow: var(--shadow-sm);
}
.card:hover, .card-sm:hover {
    box-shadow: var(--shadow);
}

/* Section label */
.section-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 700;
    color: var(--text-xmuted);
    margin-bottom: 0.6rem;
}

/* Status badges */
.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}
.badge-green  { background: var(--green-dim);  color: #047857; }
.badge-red    { background: var(--red-dim);    color: #b91c1c; }
.badge-blue   { background: var(--accent-dim); color: #0369a1; }
.badge-amber  { background: var(--amber-dim);  color: #92400e; }

/* Alert strips */
.alert {
    padding: 0.75rem 1rem;
    border-radius: var(--radius-sm);
    border-left: 4px solid;
    font-size: 0.875rem;
    font-weight: 500;
    margin-bottom: 1rem;
}
.alert-ok     { background: var(--green-dim); border-color: var(--green); color: #065f46; }
.alert-warn   { background: var(--amber-dim); border-color: var(--amber); color: #78350f; }
.alert-err    { background: var(--red-dim);   border-color: var(--red);   color: #7f1d1d; }
.alert-info   { background: var(--accent-dim);border-color: var(--accent);color: #0c4a6e; }

/* Dot status */
.dot { display:inline-block; width:8px; height:8px; border-radius:50%; margin-right:6px; }
.dot-up   { background: var(--green); box-shadow: 0 0 0 3px var(--green-dim); }
.dot-down { background: var(--red);   box-shadow: 0 0 0 3px var(--red-dim); }

/* Server card */
.server-card {
    background: var(--bg-white);
    border: 1.5px solid var(--border);
    border-radius: var(--radius);
    padding: 1.1rem 1.25rem;
    box-shadow: var(--shadow-sm);
}
.server-card.online  { border-left: 4px solid var(--green); }
.server-card.offline { border-left: 4px solid var(--red);   }
.server-type  { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-xmuted); font-weight: 700; margin: 0; }
.server-name  { font-size: 0.95rem; font-weight: 700; color: var(--text-head); margin: 0.3rem 0 0.1rem; }
.server-detail{ font-size: 0.78rem; color: var(--text-muted); margin: 0; }

/* User badge in sidebar */
.user-badge {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: var(--radius-sm);
    padding: 0.75rem 0.9rem;
    margin-bottom: 0.5rem;
}
.user-badge .u-name   { font-weight: 700; font-size: 0.95rem; color: #f1f5f9 !important; }
.user-badge .u-region { font-size: 0.78rem; font-weight: 600; margin-top: 2px; }
.user-badge .u-phone  { font-size: 0.75rem; color: #64748b !important; margin-top: 1px; }

/* Ride card */
.ride-card {
    background: var(--bg-white);
    border: 1.5px solid var(--border);
    border-radius: var(--radius);
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.6rem;
    transition: all 0.2s ease;
    box-shadow: var(--shadow-sm);
}
.ride-card:hover { box-shadow: var(--shadow); border-color: var(--accent); }

/* Logo / Brand */
.brand-logo {
    font-size: 1.5rem;
    font-weight: 900;
    letter-spacing: -0.04em;
    color: #38bdf8 !important;
    margin: 0;
    line-height: 1;
}
.brand-sub {
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #475569 !important;
    font-weight: 500;
    margin: 2px 0 0;
}

/* Stat row inside cards */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    gap: 0.75rem;
    margin-top: 0.75rem;
}
.stat-item {}
.stat-label { font-size: 0.73rem; color: var(--text-xmuted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; margin: 0; }
.stat-value { font-size: 1.1rem; font-weight: 700; color: var(--text-head); margin: 0.15rem 0 0; }
.stat-value.green { color: var(--green); }
.stat-value.blue  { color: var(--accent-dark); }
</style>
""", unsafe_allow_html=True)


# ── Session state ───────────────────────────────────────────────────────────
def _init():
    defaults = {
        "logged_in":    False,
        "user_id":      None,
        "user_name":    "Khách",
        "user_phone":   "",
        "user_region":  "south",
        "current_page": "login",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()


# ── Navigation ──────────────────────────────────────────────────────────────
def _nav():
    with st.sidebar:
        st.markdown("""
            <div style="padding: 1.25rem 0.5rem 0.5rem;">
                <p class="brand-logo">GoRide</p>
                <p class="brand-sub">Gọi xe theo vị trí</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

        cur = st.session_state.current_page

        if st.session_state.logged_in:
            region = st.session_state.user_region
            label  = REGION_LABELS[region]
            color  = REGION_COLORS[region]
            st.markdown(f"""
                <div class="user-badge">
                    <p class="u-name">{st.session_state.user_name}</p>
                    <p class="u-phone">{st.session_state.user_phone}</p>
                    <p class="u-region" style="color:{color};">{label}</p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("")

            nav_items = [
                ("Đặt xe",          "book"),
                ("Lịch sử chuyến",  "history"),
                ("Hồ sơ",           "profile"),
            ]
            for lbl, key in nav_items:
                t = "primary" if cur == key else "secondary"
                if st.button(lbl, key=f"nav_{key}", use_container_width=True, type=t):
                    st.session_state.current_page = key
                    st.rerun()

            st.markdown("---")
            if st.button("Đăng xuất", use_container_width=True):
                for k in ["logged_in","user_id","user_name","user_phone"]:
                    st.session_state[k] = False if k == "logged_in" else (None if "id" in k else "")
                st.session_state.current_page = "login"
                st.rerun()
        else:
            if st.button("Đăng nhập", use_container_width=True,
                         type="primary" if cur == "login" else "secondary"):
                st.session_state.current_page = "login"
                st.rerun()
            if st.button("Đăng ký", use_container_width=True,
                         type="primary" if cur == "register" else "secondary"):
                st.session_state.current_page = "register"
                st.rerun()

        st.markdown("---")
        t = "primary" if cur == "admin" else "secondary"
        if st.button("Hệ thống phân tán", key="nav_admin", use_container_width=True, type=t):
            st.session_state.current_page = "admin"
            st.rerun()

        st.markdown("""
            <div style="padding: 1rem 0.25rem 0.5rem; border-top: 1px solid rgba(255,255,255,0.06); margin-top: 1rem;">
                <p style="font-size:0.7rem; color:#475569; margin:0; font-weight:600; letter-spacing:0.04em;">
                    CSDL PHÂN TÁN — ĐỒ ÁN
                </p>
                <p style="font-size:0.65rem; color:#475569; margin:3px 0 0; opacity:0.7;">
                    Master-Slave Replication · Failover
                </p>
            </div>
        """, unsafe_allow_html=True)


_nav()

# ── Router ─────────────────────────────────────────────────────────────────
page = st.session_state.current_page
if page in {"book", "history", "profile"} and not st.session_state.logged_in:
    st.session_state.current_page = "login"
    page = "login"

if   page == "login":    from pages.login    import render; render()
elif page == "register": from pages.register import render; render()
elif page == "book":     from pages.book     import render; render()
elif page == "history":  from pages.history  import render; render()
elif page == "profile":  from pages.profile  import render; render()
elif page == "admin":    from pages.admin    import render; render()
else: st.error("Trang không tồn tại.")

