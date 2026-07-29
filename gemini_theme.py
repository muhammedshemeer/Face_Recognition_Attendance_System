import streamlit as st
from contextlib import contextmanager

def inject_theme():
    """Injects the Cyprus and Sand Google Fonts and custom CSS styles into the Streamlit session."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        
        /* Main Background & Typography */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #F0EDE4 !important;
            font-family: 'Outfit', sans-serif !important;
            color: #1C2E2C !important;
        }
        
        /* Clean rounded card containers */
        .gemini-card {
            background-color: #FFFFFF;
            border-radius: 20px;
            border: 1px solid #D6D2C4;
            padding: 24px;
            box-shadow: 0 4px 20px rgba(0, 71, 65, 0.03);
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        .gemini-card:hover {
            box-shadow: 0 6px 24px rgba(0, 71, 65, 0.06);
        }
        
        /* Cyprus gradient headers */
        .gemini-gradient-text {
            background: linear-gradient(135deg, #004741 0%, #146C64 50%, #2A6F68 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            font-size: 32px;
            margin-bottom: 12px;
            letter-spacing: -0.5px;
            text-align: center;
        }
        
        .gemini-sparkle-logo {
            width: 70px;
            height: 70px;
            background: linear-gradient(135deg, #E2ECEB 0%, #004741 70%, #0C3833 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px auto;
            box-shadow: 0 4px 15px rgba(0, 71, 65, 0.2);
            animation: pulse 3s infinite alternate;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            100% { transform: scale(1.06); }
        }
        
        /* Custom Status Banner */
        .status-banner {
            padding: 8px 16px;
            border-radius: 24px;
            font-size: 13px;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 20px;
        }
        .status-banner.success {
            background-color: #E6F4EA;
            color: #137333;
            border: 1px solid #CEEAD6;
        }
        .status-banner.warning {
            background-color: #FEF7E0;
            color: #B06000;
            border: 1px solid #FEEFC3;
        }
        .status-banner.error {
            background-color: #FCE8E6;
            color: #C5221F;
            border: 1px solid #FAD2CF;
        }
        
        /* Layout styling for screens */
        .header-bar {
            background-color: #FFFFFF;
            border-radius: 16px;
            border: 1px solid #D6D2C4;
            padding: 16px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.01);
        }
        
        .header-title-text {
            font-size: 20px;
            font-weight: 600;
            color: #1C2E2C;
            background: linear-gradient(120deg, #004741, #2A6F68);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .gemini-badge {
            background-color: #E2ECEB;
            color: #004741;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }
        
        /* Premium Stats Cards */
        .stat-card {
            background: #FFFFFF;
            border: 1px solid #D6D2C4;
            border-radius: 16px;
            padding: 18px 12px;
            text-align: center;
            box-shadow: 0 2px 6px rgba(0,0,0,0.01);
            transition: all 0.3s ease;
        }
        .stat-card:hover {
            border-color: #004741;
            box-shadow: 0 4px 12px rgba(0, 71, 65, 0.06);
        }
        .stat-value {
            font-size: 26px;
            font-weight: 700;
            color: #004741;
            margin-bottom: 2px;
        }
        .stat-label {
            font-size: 12px;
            color: #5F6368;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Pill button overrides for Streamlit baseButton elements */
        button[data-testid="baseButton-primary"] {
            border-radius: 24px !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 500 !important;
            padding: 8px 24px !important;
            background: linear-gradient(135deg, #004741 0%, #125E56 100%) !important;
            border: none !important;
            box-shadow: 0 4px 10px rgba(0, 71, 65, 0.15) !important;
            transition: all 0.3s ease !important;
        }
        button[data-testid="baseButton-primary"]:hover {
            background: linear-gradient(135deg, #003732 0%, #004741 100%) !important;
            box-shadow: 0 6px 15px rgba(0, 71, 65, 0.25) !important;
        }
        button[data-testid="baseButton-secondary"] {
            border-radius: 24px !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 500 !important;
            padding: 8px 24px !important;
            color: #004741 !important;
            border: 1.5px solid #004741 !important;
            background-color: transparent !important;
            transition: all 0.3s ease !important;
        }
        button[data-testid="baseButton-secondary"]:hover {
            background-color: #E2ECEB !important;
            color: #003732 !important;
            border-color: #003732 !important;
        }
        
        /* Styled camera input border */
        .stCameraInput {
            border: 2px solid #D6D2C4 !important;
            border-radius: 20px !important;
            overflow: hidden !important;
        }
        
        /* Global hides for streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def hero(title, subtitle, eyebrow=None):
    """Renders a beautiful Cyprus welcome/hero landing header."""
    eyebrow_html = f'<div style="text-transform: uppercase; font-size: 12px; font-weight: 600; letter-spacing: 1.5px; color: #004741; margin-bottom: 8px;">{eyebrow}</div>' if eyebrow else ''
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; align-items: center; text-align: center; padding: 30px 10px; margin-bottom: 10px;">
        <div class="gemini-sparkle-logo">
            <span style="color: white; font-size: 32px; font-weight: bold;">✦</span>
        </div>
        {eyebrow_html}
        <div class="gemini-gradient-text">{title}</div>
        <p style="color: #5F6368; font-size: 16px; line-height: 1.6; max-width: 500px; margin: 0 auto 10px auto;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

@contextmanager
def card(title=None, subtitle=None, center=False):
    """Context manager for rendering a modern card container."""
    center_style = "text-align: center; display: flex; flex-direction: column; align-items: center;" if center else ""
    st.markdown(f'<div class="gemini-card" style="{center_style}">', unsafe_allow_html=True)
    if title:
        align = "center" if center else "left"
        st.markdown(f'<h3 style="margin-top: 0; margin-bottom: 4px; text-align: {align}; font-weight: 600; font-size: 18px; color: #1C2E2C;">{title}</h3>', unsafe_allow_html=True)
    if subtitle:
        align = "center" if center else "left"
        st.markdown(f'<p style="margin-top: 0; margin-bottom: 20px; text-align: {align}; color: #5F6368; font-size: 13px;">{subtitle}</p>', unsafe_allow_html=True)
    try:
        yield
    finally:
        st.markdown('</div>', unsafe_allow_html=True)

@contextmanager
def drawer(title=None):
    """Context manager representing an administrative control slide-in / section drawer."""
    st.markdown('<div class="gemini-card" style="border-left: 4px solid #004741; margin-top: 15px;">', unsafe_allow_html=True)
    if title:
        st.markdown(f'<h4 style="margin-top: 0; margin-bottom: 20px; font-weight: 600; color: #004741; font-size: 16px;">{title}</h4>', unsafe_allow_html=True)
    try:
        yield
    finally:
        st.markdown('</div>', unsafe_allow_html=True)

def appbar(title, badge=None):
    """Renders a custom application top navigation/header bar."""
    badge_html = f'<span class="gemini-badge">{badge}</span>' if badge else ''
    st.markdown(f"""
    <div class="header-bar">
        <div class="header-title-text">{title}</div>
        <div>
            {badge_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

def banner(message, kind="ok"):
    """Displays a simple status banner. Options for kind: 'ok', 'warn', 'error'."""
    if kind == "ok":
        cls = "success"
        dot = '<span style="color: #34A853;">●</span>'
    elif kind == "warn":
        cls = "warning"
        dot = '<span style="color: #FBBC05;">●</span>'
    else:
        cls = "error"
        dot = '<span style="color: #EA4335;">●</span>'
        
    st.markdown(f"""
    <div class="status-banner {cls}">
        {dot} {message}
    </div>
    """, unsafe_allow_html=True)

def callout(title, message, kind="info"):
    """Creates a custom themed notification/alert panel."""
    if kind == "info":
        border_color = "#004741"
        bg_color = "#E2ECEB"
    elif kind == "success":
        border_color = "#34A853"
        bg_color = "#E6F4EA"
    elif kind == "warn":
        border_color = "#FBBC05"
        bg_color = "#FEF7E0"
    else:
        border_color = "#EA4335"
        bg_color = "#FCE8E6"
        
    st.markdown(f"""
    <div class="gemini-card" style="border-left: 5px solid {border_color}; background-color: {bg_color}; padding: 16px 20px; margin-bottom: 20px;">
        <h5 style="margin-top: 0; margin-bottom: 6px; font-weight: 600; color: #1C2E2C; font-size: 15px;">{title}</h5>
        <p style="margin: 0; font-size: 13px; color: #3C4043;">{message}</p>
    </div>
    """, unsafe_allow_html=True)

def stat_row(stats):
    """Renders a grid-aligned row of statistic values. stats list contains: (label, value, description)."""
    cols = st.columns(len(stats))
    for i, stat in enumerate(stats):
        label, value, desc = stat
        desc_html = f'<div style="font-size: 11px; color: #70757a; margin-top: 2px;">{desc}</div>' if desc else ''
        with cols[i]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{value}</div>
                <div class="stat-label">{label}</div>
                {desc_html}
            </div>
            """, unsafe_allow_html=True)

def chips(options, selected_val=None, key_prefix="chip"):
    """Interactive pill-shaped buttons to select options."""
    cols = st.columns(max(len(options), 1))
    selected = selected_val
    for i, opt in enumerate(options):
        btn_type = "primary" if opt == selected_val else "secondary"
        with cols[i]:
            if st.button(opt, key=f"{key_prefix}_{opt}", type=btn_type, use_container_width=True):
                selected = opt
    return selected

def avatar(image_url, size=100, border_color="#004741"):
    """Displays a circular profile image thumbnail."""
    st.markdown(f"""
    <div style="text-align: center; margin: 15px auto;">
        <img src="{image_url}" style="width: {size}px; height: {size}px; border-radius: 50%; object-fit: cover; border: 3px solid {border_color}; box-shadow: 0 4px 10px rgba(0,0,0,0.1);" />
    </div>
    """, unsafe_allow_html=True)

def kv(key, value):
    """Renders a neat aligned key-value pair row."""
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #F1F3F4; font-size: 14px;">
        <span style="font-weight: 600; color: #5F6368;">{key}</span>
        <span style="font-weight: 500; color: #1C2E2C;">{value}</span>
    </div>
    """, unsafe_allow_html=True)

def helper(text):
    """Outputs modern helper/caption text."""
    st.markdown(f'<p style="color: #5F6368; font-size: 13px; margin-top: -6px; text-align: center; font-weight: 500;">{text}</p>', unsafe_allow_html=True)

def footer(copyright_text="© Face Recognition Attendance System"):
    """Applies a clean footer element to the bottom of the page."""
    st.markdown(f"""
    <hr style="border: 0; border-top: 1px solid #D6D2C4; margin: 40px 0 20px 0;">
    <div style="text-align: center; font-size: 12px; color: #70757a; padding-bottom: 20px;">
        {copyright_text}
    </div>
    """, unsafe_allow_html=True)
