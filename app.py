import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="JobScope Analytics",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS  — light glassmorphism, sky-blue/green gradient
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Root tokens ── */
:root {
    --grad-start:   #e0f2fe;
    --grad-mid:     #d1fae5;
    --grad-end:     #e0f2fe;
    --glass-bg:     rgba(255,255,255,0.72);
    --glass-border: rgba(255,255,255,0.90);
    --glass-shadow: 0 8px 32px rgba(31,120,80,0.10), 0 2px 8px rgba(14,116,144,0.08);
    --card-hover:   0 16px 48px rgba(31,120,80,0.16), 0 4px 12px rgba(14,116,144,0.10);
    --teal:         #0d9488;
    --teal-light:   #14b8a6;
    --green:        #059669;
    --green-light:  #10b981;
    --sky:          #0ea5e9;
    --sky-light:    #38bdf8;
    --amber:        #d97706;
    --red:          #dc2626;
    --red-light:    #f87171;
    --text-dark:    #0f172a;
    --text-mid:     #1e293b;
    --text-soft:    #334155;
    --text-muted:   #475569;
    --teal-ink:     #0f766e;
    --green-ink:    #047857;
    --radius-lg:    20px;
    --radius-md:    14px;
    --radius-sm:    10px;
    --nav-h:        72px;
}

/* ── Global reset ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    color: #0f172a !important;
}

/* ── App background — gradient ── */
.stApp {
    background: linear-gradient(135deg, var(--grad-start) 0%, var(--grad-mid) 50%, var(--grad-end) 100%) !important;
    background-attachment: fixed !important;
    min-height: 100vh;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"]  { display: none !important; }
.block-container {
    padding: 0 32px 64px 32px !important;
    max-width: 1400px !important;
}

/* ════════════════════════════════
   FLOATING NAV BAR
════════════════════════════════ */
.nav-bar {
    position: sticky;
    top: 12px;
    z-index: 999;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(255,255,255,0.88);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: 100px;
    padding: 12px 28px;
    margin: 16px 0 32px 0;
    box-shadow: 0 4px 24px rgba(14,116,144,0.12), 0 1px 4px rgba(0,0,0,0.06);
}
.nav-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
}
.nav-brand-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, var(--teal), var(--green));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    box-shadow: 0 4px 12px rgba(13,148,136,0.3);
}
.nav-brand-name {
    font-size: 18px;
    font-weight: 800;
    background: linear-gradient(90deg, var(--teal-ink), var(--green-ink));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.3px;
}
.nav-brand-tag {
    font-size: 10px;
    font-weight: 600;
    color: var(--text-soft);   /* was --text-muted (#94a3b8) — raised to #334155 */
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.nav-links {
    display: flex;
    align-items: center;
    gap: 4px;
}
.nav-link {
    padding: 8px 18px;
    border-radius: 100px;
    font-size: 13px;
    font-weight: 600;
    color: var(--text-soft);
    cursor: pointer;
    transition: all 0.2s ease;
    border: 1.5px solid transparent;
    white-space: nowrap;
}
.nav-link:hover { color: var(--teal-ink); background: rgba(13,148,136,0.08); }
.nav-link.active {
    color: white;
    background: linear-gradient(135deg, var(--teal-ink), var(--green-ink));
    border-color: transparent;
    box-shadow: 0 4px 14px rgba(13,148,136,0.35);
}
.nav-status {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    font-weight: 600;
    color: var(--text-mid);    /* was --text-soft — raised for legibility on glass */
    padding: 6px 14px;
    background: rgba(16,185,129,0.10);
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 100px;
}
.nav-dot {
    width: 7px; height: 7px;
    background: var(--green);
    border-radius: 50%;
    animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.6; transform: scale(0.8); }
}

/* ════════════════════════════════
   HERO SECTION
════════════════════════════════ */
.hero {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 32px;
    padding: 48px 56px;
    background: var(--glass-bg);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1.5px solid var(--glass-border);
    border-radius: var(--radius-lg);
    box-shadow: var(--glass-shadow);
    margin-bottom: 32px;
    overflow: hidden;
    position: relative;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(13,148,136,0.12) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 20%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(5,150,105,0.08) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero-left { flex: 1; min-width: 0; position: relative; z-index: 1; }
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--teal-ink);
    background: rgba(13,148,136,0.1);
    border: 1px solid rgba(13,148,136,0.25);
    border-radius: 100px;
    padding: 5px 14px;
    margin-bottom: 20px;
}
.hero-headline {
    font-size: 42px;
    font-weight: 900;
    line-height: 1.1;
    letter-spacing: -1px;
    color: var(--text-dark);
    margin-bottom: 16px;
}
.hero-headline span {
    background: linear-gradient(135deg, var(--teal), var(--green));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 16px;
    line-height: 1.65;
    color: var(--text-soft);
    max-width: 480px;
    margin-bottom: 28px;
    font-weight: 400;
}
.hero-db-status {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 10px 20px;
    background: rgba(255,255,255,0.8);
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 100px;
    font-size: 13px;
    font-weight: 500;
    color: var(--text-mid);
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.hero-right {
    flex-shrink: 0;
    width: 300px;
    position: relative;
    z-index: 1;
}
.hero-preview {
    background: rgba(255,255,255,0.90);  /* raised from 0.6 — text was washed out */
    border: 1.5px solid rgba(13,148,136,0.15);
    border-radius: var(--radius-md);
    padding: 20px;
    box-shadow: 0 8px 32px rgba(13,148,136,0.12);
}
.hero-preview-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-soft);   /* was --text-muted — raised for readability */
    margin-bottom: 14px;
}
.hero-stat-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid rgba(0,0,0,0.05);
}
.hero-stat-row:last-child { border-bottom: none; }
.hero-stat-label {
    font-size: 13px;
    font-weight: 500;
    color: var(--text-mid);    /* was --text-soft — improved contrast */
    display: flex;
    align-items: center;
    gap: 8px;
}
.hero-stat-val {
    font-size: 15px;
    font-weight: 700;
    color: var(--text-dark);
}

/* ════════════════════════════════
   KPI CARDS
════════════════════════════════ */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 32px;
}
.kpi-card {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1.5px solid var(--glass-border);
    border-radius: var(--radius-md);
    padding: 24px 24px 20px 24px;
    box-shadow: var(--glass-shadow);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    position: relative;
    overflow: hidden;
    cursor: default;
}
.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--card-hover);
}
.kpi-card-glow {
    position: absolute;
    top: -30px; right: -30px;
    width: 100px; height: 100px;
    border-radius: 50%;
    opacity: 0.18;
    pointer-events: none;
}
.kpi-card-glow.blue  { background: var(--sky); }
.kpi-card-glow.teal  { background: var(--teal); }
.kpi-card-glow.green { background: var(--green); }
.kpi-card-glow.red   { background: var(--red); }

.kpi-top {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 16px;
}
.kpi-icon-wrap {
    width: 46px; height: 46px;
    border-radius: 13px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
}
.kpi-icon-wrap.blue  { background: rgba(14,165,233,0.12); }
.kpi-icon-wrap.teal  { background: rgba(13,148,136,0.12); }
.kpi-icon-wrap.green { background: rgba(5,150,105,0.12); }
.kpi-icon-wrap.red   { background: rgba(220,38,38,0.10); }

.kpi-badge {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 100px;
}
/* Solid colours for tiny badge text — transparent tints fail at 10px */
.kpi-badge.live  { background: rgba(5,150,105,0.14); color: #047857; border: 1px solid rgba(5,150,105,0.35); }
.kpi-badge.info  { background: rgba(14,165,233,0.14); color: #0369a1; border: 1px solid rgba(14,165,233,0.35); }

.kpi-value {
    font-size: 40px;
    font-weight: 900;
    letter-spacing: -1.5px;
    line-height: 1;
    color: #0f172a;            /* explicit dark, not token — ensure no override */
    margin-bottom: 6px;
}
.kpi-label {
    font-size: 13px;
    font-weight: 700;
    color: #1e293b;            /* darkened from --text-mid */
    margin-bottom: 3px;
}
.kpi-sub {
    font-size: 12px;
    color: #475569;            /* was --text-muted (#94a3b8) — raised to pass AA */
    font-weight: 500;
}
.kpi-bar {
    height: 3px;
    border-radius: 2px;
    margin-top: 16px;
    opacity: 0.6;
}
.kpi-bar.blue  { background: linear-gradient(90deg, var(--sky-light), var(--sky)); }
.kpi-bar.teal  { background: linear-gradient(90deg, var(--teal-light), var(--teal)); }
.kpi-bar.green { background: linear-gradient(90deg, var(--green-light), var(--green)); }
.kpi-bar.red   { background: linear-gradient(90deg, var(--red-light), var(--red)); }

/* ════════════════════════════════
   SECTION HEADERS
════════════════════════════════ */
.sec-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 36px 0 20px 0;
}
.sec-header-left { display: flex; align-items: center; gap: 12px; }
.sec-title {
    font-size: 20px;
    font-weight: 800;
    color: var(--text-dark);
    letter-spacing: -0.3px;
}
.sec-pill {
    font-size: 11px;
    font-weight: 700;
    color: var(--teal-ink);
    background: rgba(13,148,136,0.1);
    border: 1px solid rgba(13,148,136,0.2);
    border-radius: 100px;
    padding: 3px 12px;
    letter-spacing: 0.04em;
}
.sec-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(13,148,136,0.2), transparent);
    margin-left: 16px;
}

/* ════════════════════════════════
   GLASS PANELS (chart wrappers)
════════════════════════════════ */
.glass-panel {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1.5px solid var(--glass-border);
    border-radius: var(--radius-md);
    padding: 6px;
    box-shadow: var(--glass-shadow);
    transition: box-shadow 0.2s ease;
}
.glass-panel:hover { box-shadow: var(--card-hover); }

/* ════════════════════════════════
   CHIPS / BADGES
════════════════════════════════ */
.chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 12px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 100px;
    background: rgba(13,148,136,0.10);
    border: 1px solid rgba(13,148,136,0.25);
    color: #0f766e;            /* darker teal — 4.6:1 on white glass, passes AA */
}
.chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 20px;
}

/* ════════════════════════════════
   FILTERS PANEL
════════════════════════════════ */
.filters-panel {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1.5px solid var(--glass-border);
    border-radius: var(--radius-md);
    padding: 24px 28px;
    box-shadow: var(--glass-shadow);
    margin-bottom: 24px;
}
.filters-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-mid);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ════════════════════════════════
   BUTTONS
════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, var(--teal-ink), var(--green-ink)) !important;
    color: white !important;
    border: none !important;
    border-radius: 100px !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    padding: 10px 24px !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 14px rgba(13,148,136,0.3) !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 20px rgba(13,148,136,0.4) !important;
}
.stDownloadButton > button {
    background: white !important;
    color: var(--teal-ink) !important;
    border: 1.5px solid rgba(13,148,136,0.4) !important;
    border-radius: 100px !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    padding: 10px 24px !important;
    box-shadow: 0 2px 10px rgba(13,148,136,0.1) !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    background: rgba(13,148,136,0.06) !important;
    border-color: var(--teal) !important;
}
.stButton > button, .stDownloadButton > button {
    min-height: 44px !important;
    white-space: nowrap !important;
}

/* ════════════════════════════════
   FORM INPUTS — full contrast stack
════════════════════════════════ */

/* Input wrappers */
.stTextInput > div > div,
.stMultiSelect [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.95) !important;
    border: 1.5px solid rgba(13,148,136,0.25) !important;
    border-radius: var(--radius-sm) !important;
    color: #0f172a !important;
    font-size: 14px !important;
}
.stTextInput > div > div:focus-within,
.stMultiSelect [data-baseweb="select"] > div:focus-within {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 3px rgba(13,148,136,0.12) !important;
}

/* Typed text inside text input */
.stTextInput input {
    color: #0f172a !important;
    background: transparent !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}

/* Placeholder text */
.stTextInput input::placeholder { color: #64748b !important; }

/* Multiselect: typed search text */
.stMultiSelect input {
    color: #0f172a !important;
    font-size: 14px !important;
}

/* Multiselect: selected tag pills */
[data-baseweb="tag"] {
    background: rgba(13,148,136,0.12) !important;
    border: 1px solid rgba(13,148,136,0.3) !important;
    border-radius: 6px !important;
}
[data-baseweb="tag"] span {
    color: #0f766e !important;
    font-weight: 600 !important;
    font-size: 12px !important;
}

/* Multiselect: dropdown option list */
[data-baseweb="menu"] {
    background: white !important;
    border: 1px solid rgba(13,148,136,0.2) !important;
    border-radius: 10px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12) !important;
}
[role="option"] {
    color: #1e293b !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}
[role="option"]:hover, [aria-selected="true"] {
    background: rgba(13,148,136,0.08) !important;
    color: #0f766e !important;
}

/* All form labels */
label {
    color: #1e293b !important;
    font-weight: 700 !important;
    font-size: 13px !important;
}

/* Radio button labels (nav) */
.stRadio label, .stRadio > div > label {
    color: #1e293b !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}

/* ════════════════════════════════
   DATAFRAME — explicit text colours
════════════════════════════════ */
[data-testid="stDataFrame"] {
    border-radius: var(--radius-md) !important;
    overflow: hidden;
    border: 1.5px solid rgba(13,148,136,0.15) !important;
    box-shadow: var(--glass-shadow) !important;
}
/* Column headers */
[data-testid="stDataFrame"] th,
[data-testid="stDataFrame"] [role="columnheader"] {
    color: #0f172a !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    background: rgba(13,148,136,0.07) !important;
}
/* Cell text */
[data-testid="stDataFrame"] td,
[data-testid="stDataFrame"] [role="gridcell"] {
    color: #1e293b !important;
    font-size: 13px !important;
}

/* ════════════════════════════════
   SPINNER / ALERTS
════════════════════════════════ */
.stSpinner { color: var(--teal) !important; }
.stAlert   { border-radius: var(--radius-sm) !important; }

/* ════════════════════════════════
   EXPORT CARD
════════════════════════════════ */
.export-card {
    background: rgba(255,255,255,0.90);
    border: 1.5px solid rgba(13,148,136,0.22);
    border-radius: var(--radius-sm);
    padding: 14px 18px;
    font-size: 13px;
    color: #334155;            /* was --text-soft — explicit darker value */
    line-height: 1.6;
}

/* ════════════════════════════════
   ERROR CARD
════════════════════════════════ */
.error-glass {
    background: rgba(254,242,242,0.85);
    border: 1.5px solid rgba(220,38,38,0.25);
    border-radius: var(--radius-md);
    padding: 32px;
    text-align: center;
    backdrop-filter: blur(16px);
}
.error-glass h3 { color: var(--red); font-weight: 800; margin-bottom: 10px; }
.error-glass p  { color: var(--text-soft); font-size: 14px; line-height: 1.6; }

/* ════════════════════════════════
   STAT SUMMARY ROW
════════════════════════════════ */
.stat-row {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    margin-bottom: 24px;
}
.stat-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 7px 16px;
    background: rgba(255,255,255,0.90);
    border: 1.5px solid rgba(13,148,136,0.18);
    border-radius: 100px;
    font-size: 13px;
    font-weight: 600;
    color: #1e293b;            /* was --text-mid — explicit dark */
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.stat-pill span { color: #0f766e; font-weight: 800; } /* darker teal accent */

/* ════════════════════════════════
   SCROLLBAR
════════════════════════════════ */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(13,148,136,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(13,148,136,0.5); }

/* Premium product system */
:root {
    --grad-start: #f4f7fa;
    --grad-mid: #f4f7fa;
    --grad-end: #f4f7fa;
    --glass-bg: rgba(255,255,255,.94);
    --glass-border: #e2e8f0;
    --glass-shadow: 0 2px 8px rgba(15,23,42,.04), 0 12px 28px rgba(15,23,42,.045);
    --card-hover: 0 6px 14px rgba(15,23,42,.06), 0 18px 38px rgba(15,23,42,.08);
    --teal: #0f766e;
    --green: #059669;
    --text-dark: #111827;
    --text-mid: #1f2937;
    --text-soft: #475569;
    --text-muted: #64748b;
}
html, body, [class*="css"] { color: #111827 !important; }
.stApp { background: #f4f7fa !important; }
.block-container { max-width: 1320px !important; padding: 18px 36px 64px !important; }
.nav-bar {
    position: relative; top: auto; z-index: 2; background: #fff;
    border: 1px solid #e5eaf0; border-radius: 16px; padding: 14px 20px;
    margin: 4px 0 10px; box-shadow: 0 2px 8px rgba(15,23,42,.04);
    backdrop-filter: none;
}
.nav-brand-icon { background: #0f766e; border-radius: 10px; box-shadow: none; }
.nav-brand-name { background: none; color: #111827; -webkit-text-fill-color: #111827; letter-spacing: -.45px; }
.nav-brand-tag { color: #64748b; font-size: 11px; letter-spacing: .025em; text-transform: none; }
.nav-links { display: none; }
.nav-status { background: #f0fdf4; border-color: #bbf7d0; color: #166534; }
.nav-dot { animation: none; }
.stButton > button, .stDownloadButton > button {
    min-height: 42px !important; border-radius: 10px !important;
    font-size: 13px !important; font-weight: 650 !important;
    letter-spacing: 0 !important; box-shadow: none !important;
    transition: background .16s ease, border-color .16s ease, color .16s ease, transform .16s ease !important;
}
.stButton > button { background: #fff !important; color: #334155 !important; border: 1px solid #e2e8f0 !important; }
.stButton > button:hover { color: #0f766e !important; background: #f0fdfa !important; border-color: #99f6e4 !important; transform: translateY(-1px) !important; }
.stButton > button[kind="primary"] { background: #0f766e !important; color: #fff !important; border-color: #0f766e !important; }
.stButton > button[kind="primary"]:hover { background: #115e59 !important; border-color: #115e59 !important; }
.stRadio > label { display: none !important; }
.stRadio div[role="radiogroup"] { display: flex !important; flex-wrap: wrap !important; gap: 6px !important; align-items: center !important; }
.stRadio div[role="radiogroup"] label { margin: 0 !important; padding: 0 !important; }
.stRadio div[role="radiogroup"] label > div:first-child { display: none !important; }
.stRadio div[role="radiogroup"] label > div:last-child { border: 1px solid #e2e8f0; border-radius: 10px; background: #fff; color: #334155; padding: 9px 12px; min-height: 40px; display: flex; align-items: center; }
.stRadio div[role="radiogroup"] label:has(input:checked) > div:last-child { background: #0f766e; color: #fff; border-color: #0f766e; }
.stRadio div[role="radiogroup"] label p { margin: 0 !important; font-size: 13px !important; font-weight: 650 !important; }
.stDownloadButton > button { background: #0f766e !important; color: #fff !important; border: 1px solid #0f766e !important; }
.stDownloadButton > button:hover { background: #115e59 !important; }
button:focus-visible, input:focus-visible, [tabindex]:focus-visible { outline: 3px solid rgba(13,148,136,.35) !important; outline-offset: 2px !important; }
.hero { background: #fff; border: 1px solid #e2e8f0; border-radius: 20px; padding: 36px 42px; box-shadow: var(--glass-shadow); margin: 10px 0 26px; }
.hero::before, .hero::after { display: none; }
.hero-eyebrow { color: #0f766e; background: #f0fdfa; border: 1px solid #ccfbf1; font-size: 10px; letter-spacing: .1em; }
.hero-headline { font-size: 36px; line-height: 1.12; letter-spacing: -1.3px; margin-bottom: 12px; }
.hero-headline span { color: #0f766e; background: none; -webkit-text-fill-color: #0f766e; }
.hero-sub { max-width: 570px; font-size: 15px; color: #475569; margin-bottom: 20px; }
.hero-db-status { font-size: 12px; padding: 8px 14px; }
.hero-refresh { color: #64748b; font-size: 12px; margin-top: 10px; }
.hero-preview { border: 1px solid #e2e8f0; border-radius: 14px; box-shadow: none; background: #f8fafc; }
.hero-preview-title { color: #64748b; font-size: 10px; letter-spacing: .1em; }
.hero-stat-row { border-bottom-color: #e8edf2; }
.hero-stat-label { color: #475569; font-size: 12px; }
.hero-stat-val { font-size: 14px; }
.sec-header { margin: 30px 0 14px; }
.sec-title { color: #111827; font-size: 17px; letter-spacing: -.25px; }
.sec-pill { background: #f0fdfa; border-color: #ccfbf1; color: #0f766e; }
.sec-line { background: linear-gradient(90deg, #e2e8f0, transparent); }
.kpi-grid { gap: 16px; }
.kpi-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 15px; box-shadow: var(--glass-shadow); padding: 20px; }
.kpi-card:hover { transform: translateY(-2px); box-shadow: var(--card-hover); }
.kpi-card-glow { display: none; }
.kpi-icon-wrap { border-radius: 11px; }
.kpi-value { font-size: 34px; letter-spacing: -1px; }
.kpi-label { color: #1f2937; font-size: 13px; }
.kpi-sub { color: #64748b; font-size: 11px; }
.stat-pill { background: #fff; border: 1px solid #e2e8f0; color: #475569; box-shadow: none; }
.glass-panel, [data-testid="stPlotlyChart"], [data-testid="stDataFrame"] { background: #fff; border: 1px solid #e2e8f0; border-radius: 14px; box-shadow: 0 2px 8px rgba(15,23,42,.035); }
.filters-panel { background: #fff; border: 1px solid #e2e8f0; border-radius: 14px; box-shadow: none; }
.filters-title { color: #334155 !important; }
.stTextInput > div > div, .stMultiSelect [data-baseweb="select"] > div { background: #fff !important; border-color: #dbe3eb !important; border-radius: 9px !important; }
.export-card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; }
.chip { background: #f0fdfa; border-color: #ccfbf1; color: #0f766e; }
@keyframes rise-in { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
.hero, .kpi-card, [data-testid="stPlotlyChart"], [data-testid="stDataFrame"] { animation: rise-in .28s ease-out both; }
@media (max-width: 900px) {
    .block-container { padding: 14px 20px 48px !important; }
    .hero { padding: 28px; }
    .hero-headline { font-size: 32px; }
}
@media (max-width: 640px) {
    .block-container { padding: 10px 12px 36px !important; }
    .nav-bar { align-items: flex-start; gap: 10px; padding: 12px 14px; border-radius: 14px; }
    .nav-status { font-size: 0; padding: 8px; }
    .nav-status .nav-dot { width: 8px; height: 8px; }
    .hero { display: block; padding: 24px 20px; }
    .hero-headline { font-size: 29px; }
    .hero-right { width: 100%; margin-top: 22px; }
    .sec-header { margin-top: 24px; }
    [data-testid="stHorizontalBlock"] { flex-wrap: wrap; gap: 8px; }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PLOTLY THEME  — light glass style
# ─────────────────────────────────────────────
CHART_COLORS = [
    "#0f766e", "#059669", "#2563eb", "#6366f1",
    "#d97706", "#8b5cf6", "#0ea5e9", "#14b8a6",
    "#475569", "#65a30d",
]

CHART_LAYOUT = dict(
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    font=dict(family="Inter, sans-serif", color="#334155", size=12),
    xaxis=dict(
        gridcolor="#f1f5f9",
        linecolor="#e2e8f0",
        tickcolor="#64748b",
        tickfont=dict(color="#0f172a", size=12),
        showgrid=True,
    ),
    yaxis=dict(
        gridcolor="#f1f5f9",
        linecolor="#e2e8f0",
        tickcolor="#64748b",
        tickfont=dict(color="#0f172a", size=12),
        showgrid=True,
    ),
    margin=dict(l=16, r=16, t=48, b=16),
    legend=dict(
        bgcolor="#ffffff",
        bordercolor="#e2e8f0",
        borderwidth=1,
        font=dict(size=11, color="#334155"),
    ),
    hoverlabel=dict(
        bgcolor="#ffffff",
        bordercolor="#cbd5e1",
        font=dict(family="Inter, sans-serif", color="#0f172a", size=12),
    ),
    colorway=CHART_COLORS,
)


def apply_chart_theme(fig, title=""):
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(
            text=title,
            font=dict(size=14, color="#0f172a", family="Inter, sans-serif"),
            x=0.02,
            pad=dict(t=8),
        ),
    )
    fig.update_xaxes(tickfont=dict(color="#0f172a", size=12), title_font=dict(color="#0f172a"))
    fig.update_yaxes(tickfont=dict(color="#0f172a", size=12), title_font=dict(color="#0f172a"))
    return fig


# ─────────────────────────────────────────────
#  DATABASE  — unchanged queries and credentials
# ─────────────────────────────────────────────
def get_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        port=st.secrets["mysql"]["port"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
    )


@st.cache_data(ttl=30)
def load_data():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT
            'Jobs' AS record_source,
            j.job_id,
            j.company_id,
            c.company_name,
            c.industry,
            c.location AS company_location,
            j.job_title,
            j.job_location,
            j.posted_date,
            j.expiry_date,
            j.status,
            j.source_url
        FROM jobs j
        LEFT JOIN companies c
        ON j.company_id = c.company_id
        UNION ALL
        SELECT
            'Expired archive' AS record_source,
            e.job_id,
            e.company_id,
            c.company_name,
            c.industry,
            c.location AS company_location,
            e.job_title,
            e.job_location,
            e.posted_date,
            e.expiry_date,
            e.status,
            e.source_url
        FROM expired_jobs e
        LEFT JOIN companies c
        ON e.company_id = c.company_id
    """
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()
    connection.close()
    combined = pd.DataFrame(records)
    if not combined.empty:
        combined = combined.drop_duplicates(subset=["job_id"], keep="first")
        combined = combined.sort_values(["posted_date", "job_id"], ascending=[False, False], na_position="last")
    return combined.reset_index(drop=True)


@st.cache_data(ttl=30)
def load_status_history():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.audit_id, a.job_id, c.company_name, j.job_title,
               a.old_status, a.new_status, a.changed_at
        FROM job_audit_log a
        LEFT JOIN jobs j ON j.job_id = a.job_id
        LEFT JOIN companies c ON c.company_id = j.company_id
        ORDER BY a.changed_at DESC, a.audit_id DESC
    """)
    records = cursor.fetchall()
    cursor.close()
    connection.close()
    return pd.DataFrame(records)


@st.cache_data(ttl=30)
def load_company_count():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM companies")
    result = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return int(result)


# ─────────────────────────────────────────────
#  NAVIGATION STATE
# ─────────────────────────────────────────────
PAGE_LABELS = ("Overview", "Current Listings", "Historical Listings", "Job Lifecycle", "Analytics", "Reports", "About")
if st.session_state.get("page") == "Dashboard":
    st.session_state.page = "Overview"
if "page" not in st.session_state or st.session_state.page not in PAGE_LABELS:
    st.session_state.page = "Overview"
if st.session_state.get("nav_page") not in PAGE_LABELS:
    st.session_state.nav_page = st.session_state.page


def navigate_to(destination):
    st.session_state.page = destination


def navigate_from_radio():
    st.session_state.page = st.session_state.nav_page


def confirm_csv_download(export_label="CSV report"):
    st.session_state.csv_downloaded_label = export_label
    st.session_state.csv_downloaded_at = datetime.now().strftime("%d %b %Y · %H:%M")

now_str = datetime.now().strftime("%d %b %Y · %H:%M")
if "last_refreshed" not in st.session_state:
    st.session_state.last_refreshed = now_str

# ─────────────────────────────────────────────
#  FLOATING NAV BAR
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="nav-bar">
    <div class="nav-brand">
        <div class="nav-brand-icon">💼</div>
        <div>
            <div class="nav-brand-name">JobScope Analytics</div>
            <div class="nav-brand-tag">Job Data Intelligence</div>
        </div>
    </div>
    <div class="nav-status">
        <div class="nav-dot"></div>
        Job Data Intelligence
    </div>
</div>
""", unsafe_allow_html=True)

# Native Streamlit radio navigation keeps all sections accessible and wraps on narrow screens.
nav_col, refresh_col = st.columns([7, 1], gap="small")
with nav_col:
    st.radio("Page navigation", PAGE_LABELS, key="nav_page", horizontal=True,
             label_visibility="collapsed", on_change=navigate_from_radio)
with refresh_col:
    if st.button("Refresh", key="nav_refresh", width="stretch"):
        st.cache_data.clear()
        st.session_state.last_refreshed = datetime.now().strftime("%d %b %Y · %H:%M")
        st.session_state.refresh_notice = True
        st.rerun()

page = st.session_state.page


# ─────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────

try:
    with st.spinner("Connecting to database…"):
        df = load_data()
        company_count = load_company_count()

    db_ok = True

    if "last_refreshed" not in st.session_state:
        st.session_state.last_refreshed = datetime.now().strftime("%d %b %Y · %H:%M")

except Exception as db_error:
    db_ok = False
    df = pd.DataFrame()
    company_count = 0

if db_ok and st.session_state.pop("refresh_notice", False):
    st.success("Latest records fetched from MySQL.")


# ─────────────────────────────────────────────
#  HERO SECTION
# ─────────────────────────────────────────────
if db_ok and not df.empty:
    status_norm = df["status"].fillna("").astype(str).str.strip().str.casefold()
    known_statuses = {"active", "expired", "inactive", "under review", "archived"}
    total_jobs      = len(df)
    total_companies = company_count
    active_jobs     = int(status_norm.eq("active").sum())
    expired_jobs    = int(status_norm.eq("expired").sum())
    inactive_jobs   = int(status_norm.eq("inactive").sum())
    under_review_jobs = int(status_norm.eq("under review").sum())
    archived_records  = int((df["record_source"].eq("Expired archive") | status_norm.eq("archived")).sum())
    unknown_status_jobs = int((~status_norm.isin(known_statuses)).sum())
    db_status_html  = f'<div class="nav-dot"></div> MySQL · job_data_management · {total_jobs:,} records'
    db_status_color = "rgba(16,185,129,0.08)"
    db_border_color = "rgba(16,185,129,0.25)"
else:
    total_jobs = total_companies = active_jobs = expired_jobs = 0
    inactive_jobs = under_review_jobs = archived_records = unknown_status_jobs = 0
    db_status_html  = "⚠️ Database connection failed"
    db_status_color = "rgba(220,38,38,0.08)"
    db_border_color = "rgba(220,38,38,0.25)"

st.markdown(f"""
<div class="hero">
    <div class="hero-left">
        <div class="hero-eyebrow">JOB DATA INTELLIGENCE</div>
        <div class="hero-headline">
            Make Every Job<br>
            <span>Record Count.</span>
        </div>
        <div class="hero-sub">
            One intelligent workspace to manage job listings, understand hiring patterns and turn structured data into actionable insights.
        </div>
        <div class="hero-db-status" style="background:{db_status_color}; border-color:{db_border_color};">
            {db_status_html}
        </div>
        <div class="hero-refresh">Last refreshed · {st.session_state.last_refreshed}</div>
    </div>
    <div class="hero-right">
        <div class="hero-preview">
            <div class="hero-preview-title">Dataset snapshot</div>
            <div class="hero-stat-row">
                <div class="hero-stat-label">Total records</div>
                <div class="hero-stat-val">{total_jobs:,}</div>
            </div>
            <div class="hero-stat-row">
                <div class="hero-stat-label">Companies</div>
                <div class="hero-stat-val">{total_companies:,}</div>
            </div>
            <div class="hero-stat-row">
                <div class="hero-stat-label">Active jobs</div>
                <div class="hero-stat-val" style="color:#047857;">{active_jobs:,}</div>
            </div>
            <div class="hero-stat-row">
                <div class="hero-stat-label">Expired jobs</div>
                <div class="hero-stat-val" style="color:#dc2626;">{expired_jobs:,}</div>
            </div>
            <div class="hero-stat-row">
                <div class="hero-stat-label">Archive records</div>
                <div class="hero-stat-val">{archived_records:,}</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DATABASE ERROR STATE
# ─────────────────────────────────────────────
if not db_ok:
    st.markdown(f"""
    <div class="error-glass">
        <h3>⚠️ Database Connection Error</h3>
        <p><code>{db_error}</code></p>
        <p style="margin-top:14px;">
            • Verify MySQL Server is running<br>
            • Check credentials in <code>.streamlit/secrets.toml</code><br>
            • Confirm database <code>job_data_management</code> is accessible<br>
            • Ensure tables <code>jobs</code> and <code>companies</code> exist
        </p>
    </div>
    """, unsafe_allow_html=True)
    with st.expander("🔧 Troubleshooting Guide"):
        st.markdown("""
**Check MySQL status:**
```bash
mysql.server status
brew services list | grep mysql
```
**Test connection:**
```bash
mysql -u <user> -p -h <host> -P <port> job_data_management
```
**secrets.toml format:**
```toml
[mysql]
host     = "localhost"
port     = 3306
user     = "your_user"
password = "your_password"
database = "job_data_management"
```
        """)
    st.stop()

if df.empty:
    st.markdown("""
    <div class="error-glass">
        <h3>⚠️ No Records Found</h3>
        <p>The <code>jobs</code> table appears to be empty.<br>
           Add records and click <strong>Refresh</strong>.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────
#  FILTERS  (always visible, above content)
# ─────────────────────────────────────────────
st.markdown("""
<div class="filters-title" style="font-size:13px;font-weight:700;color:#334155;
     letter-spacing:0.06em;text-transform:uppercase;margin-bottom:0;padding:0;">
     🔍 &nbsp;Search & Filter
</div>
""", unsafe_allow_html=True)

if page == "Current Listings":
    page_dataset = df[df["record_source"].eq("Jobs")].copy()
elif page == "Historical Listings":
    historical_mask = (
        df["record_source"].eq("Expired archive")
        | df["status"].fillna("").astype(str).str.strip().str.casefold().isin({"expired", "inactive", "archived"})
    )
    page_dataset = df[historical_mask].copy()
else:
    page_dataset = df.copy()

f1, f2, f3, f4, f5, f6 = st.columns([1.55, 1.1, 1.25, 1, 1, 1.1])
with f1:
    search_term = st.text_input("Search", placeholder="Company or job title…", label_visibility="collapsed")
with f2:
    company_filter = st.multiselect("Company", sorted(page_dataset["company_name"].dropna().unique()), placeholder="All companies")
with f3:
    title_filter = st.multiselect("Job title", sorted(page_dataset["job_title"].dropna().unique()), placeholder="All job titles")
with f4:
    status_filter = st.multiselect("Status", sorted(page_dataset["status"].dropna().unique()), placeholder="All statuses")
with f5:
    location_filter = st.multiselect("Location", sorted(page_dataset["job_location"].dropna().unique()), placeholder="All locations")
with f6:
    source_filter = st.multiselect("Record source", sorted(page_dataset["record_source"].dropna().unique()), placeholder="All sources")

posted_range = expiry_range = ()
if page == "Historical Listings":
    date_col1, date_col2 = st.columns(2)
    with date_col1:
        posted_range = st.date_input("Posting date range", value=(), key="historical_posted_range")
    with date_col2:
        expiry_range = st.date_input("Expiry date range", value=(), key="historical_expiry_range")

# Apply filters
filtered_df = page_dataset.copy()
if search_term:
    mask = (
        filtered_df["job_title"].astype("string").str.contains(search_term, case=False, na=False)
        | filtered_df["company_name"].astype("string").str.contains(search_term, case=False, na=False)
    )
    filtered_df = filtered_df[mask]
if company_filter:
    filtered_df = filtered_df[filtered_df["company_name"].isin(company_filter)]
if title_filter:
    filtered_df = filtered_df[filtered_df["job_title"].isin(title_filter)]
if status_filter:
    filtered_df = filtered_df[filtered_df["status"].isin(status_filter)]
if location_filter:
    filtered_df = filtered_df[filtered_df["job_location"].isin(location_filter)]
if source_filter:
    filtered_df = filtered_df[filtered_df["record_source"].isin(source_filter)]


def filter_by_date_range(frame, column, selected_range):
    if isinstance(selected_range, tuple):
        if not selected_range:
            return frame
        start_date = selected_range[0]
        end_date = selected_range[-1]
    elif selected_range:
        start_date = end_date = selected_range
    else:
        return frame
    values = pd.to_datetime(frame[column], errors="coerce").dt.date
    return frame[values.notna() & values.ge(start_date) & values.le(end_date)]


if page == "Historical Listings":
    filtered_df = filter_by_date_range(filtered_df, "posted_date", posted_range)
    filtered_df = filter_by_date_range(filtered_df, "expiry_date", expiry_range)

filtered_count = len(filtered_df)

# KPI calculations from full dataset
active_pct  = round(active_jobs  / total_jobs * 100) if total_jobs else 0
expired_pct = round(expired_jobs / total_jobs * 100) if total_jobs else 0


def render_records_table(records, key):
    display_columns = ["job_id", "company_name", "industry", "company_location", "job_title", "job_location",
                       "posted_date", "expiry_date", "status", "record_source", "source_url"]
    display_df = records[[column for column in display_columns if column in records.columns]].copy()
    for column in ("posted_date", "expiry_date"):
        if column in display_df:
            parsed_dates = pd.to_datetime(display_df[column], errors="coerce")
            display_df[column] = parsed_dates.dt.strftime("%d %b %Y").fillna("—")
    display_df.columns = [column.replace("_", " ").title() for column in display_df.columns]
    status_palette = {
        "active": "background-color:#dcfce7;color:#166534;font-weight:650;border-radius:6px",
        "expired": "background-color:#fee2e2;color:#991b1b;font-weight:650;border-radius:6px",
        "inactive": "background-color:#f1f5f9;color:#475569;font-weight:650;border-radius:6px",
        "under review": "background-color:#fef3c7;color:#92400e;font-weight:650;border-radius:6px",
        "archived": "background-color:#dbeafe;color:#1d4ed8;font-weight:650;border-radius:6px",
    }
    if "Status" in display_df.columns:
        styled_df = display_df.style.map(
            lambda value: status_palette.get(str(value).strip().casefold(), "background-color:#f1f5f9;color:#334155"),
            subset=["Status"],
        )
    else:
        styled_df = display_df
    st.dataframe(styled_df, width="stretch", hide_index=True,
                 height=min(600, 56 + len(display_df) * 35), key=key)


def csv_download_button(records, label, key, filename):
    st.download_button(
        label=label,
        data=records.to_csv(index=False).encode("utf-8"),
        file_name=filename,
        mime="text/csv",
        width="stretch",
        key=key,
        on_click=confirm_csv_download,
        args=(label,),
    )


# ════════════════════════════════════════════
#  PAGE: OVERVIEW
# ════════════════════════════════════════════
if filtered_df.empty and page not in ("About", "Reports", "Overview"):
    st.markdown("""
    <div class="error-glass" style="background:#fff;border-color:#e2e8f0;text-align:left">
        <h3 style="color:#111827">No matching job records</h3>
        <p>Try a different search term or clear one or more filters to see records and analytics.</p>
    </div>
    """, unsafe_allow_html=True)

elif page == "Overview":

    if filtered_df.empty:
        st.info("No records match the current filters. The KPI cards below continue to show the complete dataset.")

    # ── KPI Cards ──
    st.markdown("""
    <div class="sec-header">
        <div class="sec-header-left">
            <div class="sec-title">Key Metrics</div>
            <div class="sec-pill">Live from Database</div>
        </div>
        <div class="sec-line"></div>
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)

    def render_kpi(col, icon, label, value, sub, color, badge="live"):
        col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-card-glow {color}"></div>
            <div class="kpi-top">
                <div class="kpi-icon-wrap {color}">{icon}</div>
                <div class="kpi-badge {badge}">{'Live' if badge == 'live' else 'Info'}</div>
            </div>
            <div class="kpi-value">{value:,}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-sub">{sub}</div>
            <div class="kpi-bar {color}"></div>
        </div>
        """, unsafe_allow_html=True)

    render_kpi(k1, "▤", "Total Job Records", total_jobs, "All accessible listings", "blue", "info")
    render_kpi(k2, "✓", "Active Jobs", active_jobs, "Current database status", "green", "live")
    render_kpi(k3, "–", "Expired Jobs", expired_jobs, "Stored status: Expired", "red", "info")
    render_kpi(k4, "○", "Inactive Jobs", inactive_jobs, "Explicitly marked inactive", "teal", "info")
    k5, k6, k7 = st.columns(3)
    render_kpi(k5, "…", "Under Review", under_review_jobs, "Current database status", "blue", "info")
    render_kpi(k6, "▣", "Archived Records", archived_records, "Rows held in archive", "teal", "info")
    render_kpi(k7, "◎", "Total Companies", total_companies, "Company records in MySQL", "green", "info")
    if unknown_status_jobs:
        st.info(f"{unknown_status_jobs:,} record(s) have an unclassified status. Their original values remain in Job Lifecycle and exports.")

    # ── Stat pills row ──
    n_industries = df["industry"].nunique() if "industry" in df.columns else "—"
    n_locations  = df["job_location"].nunique()
    n_roles      = df["job_title"].nunique()
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-pill">🏭 Industries &nbsp;<span>{n_industries}</span></div>
        <div class="stat-pill">📍 Locations &nbsp;<span>{n_locations}</span></div>
        <div class="stat-pill">💼 Unique Roles &nbsp;<span>{n_roles}</span></div>
        <div class="stat-pill">🟢 Active Rate &nbsp;<span>{active_pct}%</span></div>
        <div class="stat-pill">🔴 Expired Rate &nbsp;<span>{expired_pct}%</span></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Quick Insight Charts ──
    st.markdown("""
    <div class="sec-header">
        <div class="sec-header-left">
            <div class="sec-title">Quick Insights</div>
        </div>
        <div class="sec-line"></div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        status_counts = (filtered_df.assign(status=filtered_df["status"].fillna("Unclassified"))
                         .groupby("status").size().reset_index(name="Count"))
        status_colors = {
            "Active": "#059669", "Expired": "#dc2626",
            "Pending": "#d97706", "Closed": "#6366f1",
        }
        s_colors = [status_colors.get(s, "#94a3b8") for s in status_counts["status"]]
        fig_s = go.Figure(go.Pie(
            labels=status_counts["status"],
            values=status_counts["Count"],
            hole=0.58,
            marker=dict(colors=s_colors, line=dict(color="white", width=3)),
            textfont=dict(color="#334155", size=12),
            textposition="outside",
            textinfo="label+percent",
        ))
        fig_s = apply_chart_theme(fig_s, "Job Status Distribution")
        fig_s.update_layout(showlegend=True, height=320, margin=dict(l=64, r=64, t=50, b=20))
        st.plotly_chart(fig_s, width="stretch", theme=None, config={"displayModeBar": False})

    with col_b:
        top_loc = (
            filtered_df.assign(job_location=filtered_df["job_location"].fillna("Unspecified location")).groupby("job_location").size()
            .reset_index(name="Count")
            .sort_values("Count", ascending=False)
            .head(8)
        )
        fig_loc = px.bar(
            top_loc, x="Count", y="job_location",
            orientation="h",
            color="Count",
            color_continuous_scale=["#d1fae5", "#059669", "#0d9488"],
        )
        fig_loc.update_traces(marker_line_color="rgba(0,0,0,0)")
        fig_loc = apply_chart_theme(fig_loc, "Top Locations by Postings")
        fig_loc.update_layout(
            coloraxis_showscale=False, height=320,
            xaxis_title="", yaxis_title="",
            margin=dict(l=125, r=20, t=50, b=24),
        )
        fig_loc.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_loc, width="stretch", theme=None, config={"displayModeBar": False})


# ════════════════════════════════════════════
#  PAGE: JOB LIFECYCLE
# ════════════════════════════════════════════
elif page == "Job Lifecycle":
    st.markdown(f"""
    <div class="sec-header"><div class="sec-header-left">
        <div class="sec-title">Job Lifecycle</div><div class="sec-pill">{filtered_count:,} filtered records</div>
    </div><div class="sec-line"></div></div>
    """, unsafe_allow_html=True)
    lifecycle_norm = filtered_df["status"].fillna("").astype(str).str.strip().str.casefold()
    lifecycle_archive = int((filtered_df["record_source"].eq("Expired archive") | lifecycle_norm.eq("archived")).sum())
    lc1, lc2, lc3, lc4, lc5 = st.columns(5)
    for col, label, value, help_text in [
        (lc1, "Active", int(lifecycle_norm.eq("active").sum()), "Explicitly stored as Active"),
        (lc2, "Expired", int(lifecycle_norm.eq("expired").sum()), "Explicitly stored as Expired"),
        (lc3, "Inactive", int(lifecycle_norm.eq("inactive").sum()), "Explicitly stored as Inactive"),
        (lc4, "Under Review", int(lifecycle_norm.eq("under review").sum()), "Explicitly stored as Under Review"),
        (lc5, "Archived records", lifecycle_archive, "Rows in expired_jobs or marked Archived"),
    ]:
        col.metric(label, f"{value:,}", help=help_text)

    st.caption("Status values are preserved as stored. Expiry dates do not automatically change a listing’s status. Archive source records can also carry an Expired status.")
    lifecycle_summary = (filtered_df.assign(status=filtered_df["status"].fillna("Unclassified"))
                         .groupby(["status", "record_source"], dropna=False).size()
                         .rename("Records").reset_index()
                         .rename(columns={"status": "Status", "record_source": "Record source"})
                         .sort_values(["Status", "Record source"]))
    st.markdown("#### Current status by data source")
    st.dataframe(lifecycle_summary, width="stretch", hide_index=True)
    render_records_table(filtered_df, key="lifecycle_records")

    st.markdown("#### Status-change history")
    st.caption("Changes recorded by the existing MySQL audit trigger. This history is separate from each listing’s current status.")
    try:
        audit_df = load_status_history()
        if audit_df.empty:
            st.info("No status changes are recorded in the audit log.")
        else:
            audit_df = audit_df.rename(columns={
                "audit_id": "Audit ID", "job_id": "Job ID", "company_name": "Company",
                "job_title": "Job title", "old_status": "Previous status",
                "new_status": "New status", "changed_at": "Changed at",
            })
            st.dataframe(audit_df, width="stretch", hide_index=True)
    except Exception as audit_error:
        st.warning(f"Status history is unavailable: {audit_error}")


# ════════════════════════════════════════════
#  PAGE: ANALYTICS
# ════════════════════════════════════════════
elif page == "Analytics":

    if any([search_term, company_filter, title_filter, status_filter, location_filter, source_filter, posted_range, expiry_range]):
        st.markdown(f"""
        <div class="chip-row">
            <div class="chip">🔽 Filters active — {filtered_count:,} of {total_jobs:,} records shown</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Chart 1 & 2: Company & Role ──
    st.markdown("""
    <div class="sec-header">
        <div class="sec-header-left">
            <div class="sec-title">Company &amp; Role Analysis</div>
        </div>
        <div class="sec-line"></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        company_data = (
            filtered_df.assign(company_name=filtered_df["company_name"].fillna("Unlinked company")).groupby("company_name").size()
            .reset_index(name="Job Count")
            .sort_values("Job Count", ascending=False)
        )
        fig1 = px.bar(
            company_data, x="company_name", y="Job Count",
            color="Job Count",
            color_continuous_scale=["#d1fae5", "#059669", "#0d9488"],
        )
        fig1.update_traces(marker_line_color="rgba(0,0,0,0)", width=0.6)
        fig1 = apply_chart_theme(fig1, "Jobs Posted by Company")
        fig1.update_layout(
            xaxis_tickangle=-35, coloraxis_showscale=False,
            height=380, xaxis_title="", yaxis_title="Job Count",
            margin=dict(l=24, r=20, t=50, b=100),
        )
        st.plotly_chart(fig1, width="stretch", theme=None, config={"displayModeBar": False})

    with col2:
        role_data = (
            filtered_df.assign(job_title=filtered_df["job_title"].fillna("Unspecified title")).groupby("job_title").size()
            .reset_index(name="Postings")
            .sort_values("Postings", ascending=False)
        )
        fig2 = px.pie(
            role_data, names="job_title", values="Postings",
            hole=0.42,
            color_discrete_sequence=CHART_COLORS,
        )
        fig2.update_traces(
            textposition="inside",
            textinfo="percent+label",
            textfont_size=11,
            marker=dict(line=dict(color="white", width=2)),
        )
        fig2 = apply_chart_theme(fig2, "Job Role Distribution")
        fig2.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig2, width="stretch", theme=None, config={"displayModeBar": False})

    # ── Chart 3: Location ──
    st.markdown("""
    <div class="sec-header">
        <div class="sec-header-left">
            <div class="sec-title">Geographic Distribution</div>
        </div>
        <div class="sec-line"></div>
    </div>
    """, unsafe_allow_html=True)

    location_data = (
        filtered_df.assign(job_location=filtered_df["job_location"].fillna("Unspecified location")).groupby("job_location").size()
        .reset_index(name="Job Count")
        .sort_values("Job Count", ascending=False)
    )
    fig3 = px.bar(
        location_data, x="job_location", y="Job Count",
        color="Job Count",
        color_continuous_scale=["#e0f2fe", "#0ea5e9", "#0d9488"],
    )
    fig3.update_traces(marker_line_color="rgba(0,0,0,0)", width=0.65)
    fig3 = apply_chart_theme(fig3, "Job Distribution by Location")
    fig3.update_layout(
        xaxis_tickangle=-30, coloraxis_showscale=False,
        height=360, xaxis_title="", yaxis_title="Number of Jobs",
        margin=dict(l=48, r=20, t=50, b=90),
    )
    st.plotly_chart(fig3, width="stretch", theme=None, config={"displayModeBar": False})

    # ── Chart 4: Status Breakdown ──
    st.markdown("""
    <div class="sec-header">
        <div class="sec-header-left">
            <div class="sec-title">Status Breakdown</div>
        </div>
        <div class="sec-line"></div>
    </div>
    """, unsafe_allow_html=True)

    col_s1, col_s2 = st.columns([1, 2])

    with col_s1:
        status_summary = (
            filtered_df.assign(status=filtered_df["status"].fillna("Unclassified")).groupby("status").size()
            .reset_index(name="Count")
        )
        status_summary["Share %"] = (
            status_summary["Count"] / status_summary["Count"].sum() * 100
        ).round(1)
        st.dataframe(status_summary, width="stretch", hide_index=True)

    with col_s2:
        status_data = (filtered_df.assign(status=filtered_df["status"].fillna("Unclassified"))
                       .groupby("status").size().reset_index(name="Count"))
        status_color_map = {
            "Active":  "#059669", "Expired": "#dc2626",
            "Pending": "#d97706", "Closed":  "#6366f1",
        }
        colors4 = [status_color_map.get(s, "#94a3b8") for s in status_data["status"]]
        fig4 = go.Figure(go.Pie(
            labels=status_data["status"],
            values=status_data["Count"],
            hole=0.60,
            marker=dict(colors=colors4, line=dict(color="white", width=3)),
            textfont=dict(color="#334155", size=13),
        ))
        fig4.update_traces(textposition="outside", textinfo="label+value")
        fig4 = apply_chart_theme(fig4, "Job Status Overview")
        fig4.update_layout(height=300, showlegend=True, margin=dict(l=64, r=64, t=50, b=20))
        st.plotly_chart(fig4, width="stretch", theme=None, config={"displayModeBar": False})

    if "industry" in filtered_df.columns and filtered_df["industry"].notna().any():
        st.markdown("""
        <div class="sec-header">
            <div class="sec-header-left"><div class="sec-title">Industry Distribution</div></div>
            <div class="sec-line"></div>
        </div>
        """, unsafe_allow_html=True)
        industry_data = (filtered_df.dropna(subset=["industry"]).groupby("industry").size()
                         .reset_index(name="Job Count").sort_values("Job Count", ascending=True))
        industry_fig = px.bar(industry_data, x="Job Count", y="industry", orientation="h",
                              color_discrete_sequence=["#0f766e"])
        industry_fig = apply_chart_theme(industry_fig, "Job Postings by Industry")
        industry_fig.update_layout(height=max(250, 42 * len(industry_data)), xaxis_title="Job postings",
                                   yaxis_title="", showlegend=False, bargap=.35)
        industry_fig.update_traces(marker_line_color="rgba(0,0,0,0)")
        st.plotly_chart(industry_fig, width="stretch", theme=None, config={"displayModeBar": False})

    st.markdown("""
    <div class="sec-header"><div class="sec-header-left"><div class="sec-title">Historical Activity</div></div>
    <div class="sec-line"></div></div>
    """, unsafe_allow_html=True)
    analytics_norm = filtered_df["status"].fillna("").astype(str).str.strip().str.casefold()
    historical_mask = (
        filtered_df["record_source"].eq("Expired archive")
        | analytics_norm.isin({"expired", "inactive", "archived"})
    )
    historical_df = filtered_df[historical_mask].copy()
    active_expired = pd.DataFrame({
        "Status": ["Active", "Expired"],
        "Records": [int(analytics_norm.eq("active").sum()), int(analytics_norm.eq("expired").sum())],
    })
    active_expired = active_expired[active_expired["Records"] > 0]
    hist_col1, hist_col2 = st.columns(2)
    with hist_col1:
        active_expired_fig = px.pie(active_expired, names="Status", values="Records", hole=.58,
                                    color="Status", color_discrete_map={"Active": "#059669", "Expired": "#dc2626"})
        active_expired_fig.update_traces(textinfo="label+value", marker=dict(line=dict(color="white", width=2)))
        active_expired_fig = apply_chart_theme(active_expired_fig, "Active vs Expired Listings")
        active_expired_fig.update_layout(height=330, showlegend=False)
        st.plotly_chart(active_expired_fig, width="stretch", theme=None, config={"displayModeBar": False})
    with hist_col2:
        posted_dates = pd.to_datetime(filtered_df["posted_date"], errors="coerce")
        posting_trend = (filtered_df.assign(posting_month=posted_dates.dt.to_period("M").dt.to_timestamp())
                         .dropna(subset=["posting_month"]).groupby("posting_month").size()
                         .rename("Postings").reset_index())
        if posting_trend.empty:
            st.info("Posting trend is unavailable because no posting dates are recorded.")
        else:
            trend_fig = px.line(posting_trend, x="posting_month", y="Postings", markers=True,
                                color_discrete_sequence=["#0f766e"])
            trend_fig = apply_chart_theme(trend_fig, "Job Postings by Month")
            trend_fig.update_layout(height=330, xaxis_title="Posting month", yaxis_title="Listings")
            trend_fig.update_traces(line_width=3, marker_size=8, hovertemplate="%{x|%b %Y}<br>%{y} listings<extra></extra>")
            st.plotly_chart(trend_fig, width="stretch", theme=None, config={"displayModeBar": False})

    durations = (pd.to_datetime(filtered_df["expiry_date"], errors="coerce")
                 - pd.to_datetime(filtered_df["posted_date"], errors="coerce")).dt.days
    valid_durations = durations[durations.ge(0)]
    duration_value = f"{valid_durations.mean():.1f} days" if not valid_durations.empty else "Unavailable"
    st.metric("Average listing duration", duration_value,
              help=f"Calculated from {len(valid_durations):,} records with valid posting and expiry dates; negative or missing durations are excluded.")

    hist_col3, hist_col4 = st.columns(2)
    with hist_col3:
        if historical_df.empty:
            st.info("No historical records match the current filters.")
        else:
            historical_company = (historical_df.assign(company_name=historical_df["company_name"].fillna("Unlinked company"))
                                  .groupby("company_name").size().rename("Historical listings")
                                  .sort_values(ascending=True).rename_axis("Company").reset_index())
            hist_company_fig = px.bar(historical_company, x="Historical listings", y="Company", orientation="h",
                                      color_discrete_sequence=["#2563eb"])
            hist_company_fig = apply_chart_theme(hist_company_fig, "Historical Listings by Company")
            hist_company_fig.update_layout(height=max(270, 42 * len(historical_company)), xaxis_title="Historical listings",
                                           yaxis_title="", showlegend=False)
            st.plotly_chart(hist_company_fig, width="stretch", theme=None, config={"displayModeBar": False})
    with hist_col4:
        expired_rows = filtered_df[analytics_norm.eq("expired")].copy()
        expiry_dates = pd.to_datetime(expired_rows["expiry_date"], errors="coerce")
        expired_trend = (expired_rows.assign(expiry_month=expiry_dates.dt.to_period("M").dt.to_timestamp())
                         .dropna(subset=["expiry_month"]).groupby("expiry_month").size()
                         .rename("Expired listings").reset_index())
        if expired_trend.empty:
            st.info("Expired listing trend is unavailable because no expired records with expiry dates match these filters.")
        else:
            expired_fig = px.bar(expired_trend, x="expiry_month", y="Expired listings",
                                 color_discrete_sequence=["#dc2626"])
            expired_fig = apply_chart_theme(expired_fig, "Expired Listings by Month")
            expired_fig.update_layout(height=330, xaxis_title="Expiry month", yaxis_title="Expired listings", showlegend=False)
            st.plotly_chart(expired_fig, width="stretch", theme=None, config={"displayModeBar": False})


# ════════════════════════════════════════════
#  PAGE: JOB RECORDS
# ════════════════════════════════════════════
elif page in ("Current Listings", "Historical Listings"):

    st.markdown(f"""
    <div class="sec-header">
        <div class="sec-header-left">
            <div class="sec-title">{page}</div>
            <div class="sec-pill">{filtered_count:,} records</div>
        </div>
        <div class="sec-line"></div>
    </div>
    """, unsafe_allow_html=True)

    # Active filter chips
    if any([search_term, company_filter, status_filter, location_filter]):
        chips = []
        if search_term:
            chips.append(f'🔍 "{search_term}"')
        for c in company_filter:
            chips.append(f"🏢 {c}")
        for title in title_filter:
            chips.append(f"💼 {title}")
        for s in status_filter:
            chips.append(f"📌 {s}")
        for loc in location_filter:
            chips.append(f"📍 {loc}")
        for source in source_filter:
            chips.append(f"▣ {source}")
        chip_html = "".join(f'<div class="chip">{ch}</div>' for ch in chips)
        st.markdown(f'<div class="chip-row">{chip_html}</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="chip-row">
            <div class="chip">MySQL listings · use the filters above to narrow results</div>
        </div>
        """, unsafe_allow_html=True)

    render_records_table(filtered_df, key=f"records_{page.lower().replace(' ', '_')}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CSV Export ──
    st.markdown("""
    <div class="sec-header">
        <div class="sec-header-left">
            <div class="sec-title">Export Data</div>
        </div>
        <div class="sec-line"></div>
    </div>
    """, unsafe_allow_html=True)

    exp_col1, exp_col2 = st.columns([2, 3])
    with exp_col1:
        csv_download_button(filtered_df, f"Download {filtered_count:,} Filtered Records", "filtered_records_download",
                            f"jobscope_filtered_{datetime.now().strftime('%Y%m%d_%H%M')}.csv")
    with exp_col2:
        st.markdown(f"""
        <div class="export-card">
            📄 Export includes all visible columns with current filters applied.<br>
            <span style="font-size:11.5px; color:#475569; font-weight:500;">
                {filtered_count:,} records · Generated {datetime.now().strftime('%d %b %Y %H:%M')}
            </span>
        </div>
        """, unsafe_allow_html=True)
    if st.session_state.get("csv_downloaded_at"):
        st.success(f"{st.session_state.get('csv_downloaded_label', 'CSV report')} downloaded · {st.session_state.csv_downloaded_at}")

elif page == "Reports":
    st.markdown(f"""
    <div class="sec-header">
        <div class="sec-header-left">
            <div class="sec-title">Reports &amp; Export</div>
            <div class="sec-pill">{filtered_count:,} filtered records</div>
        </div>
        <div class="sec-line"></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("Export the current job records using the search and filters above.")
    report_df = filtered_df.copy()
    report_stamp = datetime.now().strftime("%Y%m%d_%H%M")
    csv_download_button(report_df, f"Download {len(report_df):,} Filtered Records", "reports_download_csv",
                        f"jobscope_filtered_{report_stamp}.csv")
    status_norm_all = df["status"].fillna("").astype(str).str.strip().str.casefold()
    export_sets = [
        ("Download Complete Dataset", df.copy(), "complete_dataset"),
        ("Download Active Listings", df[status_norm_all.eq("active")].copy(), "active_listings"),
        ("Download Expired Listings", df[status_norm_all.eq("expired")].copy(), "expired_listings"),
        ("Download Inactive Listings", df[status_norm_all.eq("inactive")].copy(), "inactive_listings"),
        ("Download Archived Records", df[df["record_source"].eq("Expired archive") | status_norm_all.eq("archived")].copy(), "archived_records"),
    ]
    export_cols = st.columns(3)
    for index, (label, export_df, export_key) in enumerate(export_sets):
        with export_cols[index % 3]:
            csv_download_button(export_df, f"{label} · {len(export_df):,}", f"reports_{export_key}",
                                f"jobscope_{export_key}_{report_stamp}.csv")
    if st.session_state.get("csv_downloaded_at"):
        st.success(f"{st.session_state.get('csv_downloaded_label', 'CSV report')} downloaded · {st.session_state.csv_downloaded_at}")

    report_a, report_b, report_c = st.columns(3)
    with report_a:
        st.metric("Records in report", f"{len(report_df):,}")
    with report_b:
        st.metric("Companies represented", f"{report_df['company_name'].nunique():,}" if "company_name" in report_df else "0")
    with report_c:
        st.metric("Industries represented", f"{report_df['industry'].nunique():,}" if "industry" in report_df else "0")

    report_left, report_right = st.columns(2)
    company_report = (report_df.assign(company_name=report_df["company_name"].fillna("Unlinked company"))
                      .groupby("company_name").size().rename("Job postings")
                      .sort_values(ascending=False).rename_axis("Company").reset_index())
    with report_left:
        st.markdown("#### Company-wise job counts")
        st.dataframe(company_report, width="stretch", hide_index=True)
        csv_download_button(company_report, "Download Company-wise Report", "company_report_download",
                            f"jobscope_company_report_{report_stamp}.csv")
    with report_right:
        st.markdown("#### Status distribution")
        status_report = (report_df.assign(status=report_df["status"].fillna("Unclassified"))
                         .groupby("status").size().rename("Records")
                         .sort_values(ascending=False).rename_axis("Status").reset_index())
        st.dataframe(status_report, width="stretch", hide_index=True)
    st.markdown(f"""
    <div class="export-card" style="margin-top:16px">
        The report includes the visible job fields and respects the active search, company, status, and location filters.
        <br><strong>{len(report_df):,}</strong> records included.
    </div>
    """, unsafe_allow_html=True)

elif page == "About":
    st.markdown("""
    <div class="sec-header">
        <div class="sec-header-left"><div class="sec-title">About JobScope Analytics</div></div>
        <div class="sec-line"></div>
    </div>
    <div class="export-card">
        JobScope Analytics is a MySQL powered dashboard for exploring job listings,
        comparing employers and locations, monitoring listing status, and exporting
        filtered records. Dashboard and analytics views use the live records loaded
        from the configured MySQL database.
    </div>
    """, unsafe_allow_html=True)
