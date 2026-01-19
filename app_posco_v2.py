#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════════╗
║          REKARBON × POSCO HOLDINGS (포스코홀딩스)                                 ║
║          Edge-Native MRV Platform for Green Steel & Decarbonization              ║
╠═══════════════════════════════════════════════════════════════════════════════════╣
║  Company: POSCO Holdings Inc. - Korea's Largest Steel Manufacturer                ║
║  HQ: Pohang/Seoul, South Korea 🇰🇷 | Founded: 1968 (56+ years)                   ║
║  Revenue: ₩73T ($60B) • 36,000 Employees • 42 Mt Steel/Year (6th World)          ║
╠═══════════════════════════════════════════════════════════════════════════════════╣
║  SECTORS:                                                                         ║
║  ├─ Steelmaking (60%) - BF-BOF 38Mt, EAF 4Mt, HyREX Pilot 2024                   ║
║  ├─ Chemical (15%) - Lithium 85Kt, Hydrogen 125Kt (2030), Cathodes               ║
║  ├─ Construction (15%) - Steel Structures, Infrastructure, Plants                ║
║  └─ Energy (10%) - LNG Terminals, Renewables, Cogeneration                       ║
╠═══════════════════════════════════════════════════════════════════════════════════╣
║  VALUATION FRAMEWORK:                                                             ║
║  ├─ Level 1: ₩610B/year ($488M) - K-ETS, Green Steel, Scrap Recycling            ║
║  ├─ Level 2: ₩3.2T/year ($2.6B) - Total Economic Value                           ║
║  └─ Level 3: ₩7.0T/year ($5.6B) - With HyREX Commercial, H2, Batteries           ║
╠═══════════════════════════════════════════════════════════════════════════════════╣
║  COMPLIANCE: K-ETS Phase 3 • ResponsibleSteel • ISO 14064 • TCFD • CDP A-        ║
║  Version: 2.0.0-production | Languages: 한국어 + English                          ║
║  © 2026 Rekarbon SAS - Paris • La Réunion                                        ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np
import time

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="POSCO × Rekarbon MRV | 포스코 × 리카본",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS - POSCO PREMIUM DESIGN
# =============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --posco-blue: #003DA5;
        --posco-blue-dark: #001F5B;
        --posco-red: #E4002B;
        --posco-red-dark: #B8001F;
        --posco-gray: #58595B;
        --success: #00B894;
        --warning: #F39C12;
    }
    
    * { font-family: 'Noto Sans KR', 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(180deg, #F5F7FA 0%, #EEF2F7 100%);
    }
    
    /* Premium Header */
    .posco-header {
        background: linear-gradient(135deg, #003DA5 0%, #001F5B 30%, #0A0A1A 100%);
        padding: 2.5rem 3rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(0, 61, 165, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .posco-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(228,0,43,0.2) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .posco-header h1 {
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .posco-header .subtitle {
        font-size: 1.15rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        border-left: 5px solid #003DA5;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 60px rgba(0,61,165,0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #003DA5;
        line-height: 1.1;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .metric-delta {
        font-size: 0.85rem;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        margin-top: 0.5rem;
        font-weight: 600;
    }
    
    .metric-delta.positive { background: rgba(0,184,148,0.15); color: #00B894; }
    .metric-delta.warning { background: rgba(228,0,43,0.15); color: #E4002B; }
    
    /* Level Badges */
    .level-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.7rem 1.5rem;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.95rem;
        margin: 0.4rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }
    
    .level-1 { background: linear-gradient(135deg, #003DA5, #001F5B); color: white; }
    .level-2 { background: linear-gradient(135deg, #E4002B, #B8001F); color: white; }
    .level-3 { background: linear-gradient(135deg, #00B894, #00A085); color: white; }
    
    /* Certification Badges */
    .cert-badge {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(135deg, #001F5B, #003DA5);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        margin: 0.25rem;
        font-weight: 600;
        font-size: 0.8rem;
        box-shadow: 0 3px 10px rgba(0,61,165,0.3);
    }
    
    /* Steel Box */
    .steel-box {
        background: linear-gradient(135deg, #003DA5 0%, #0A0A1A 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        position: relative;
        overflow: hidden;
        box-shadow: 0 15px 50px rgba(0,61,165,0.25);
    }
    
    /* HyREX Box (Green Steel) */
    .hyrex-box {
        background: linear-gradient(135deg, #00B894 0%, #00A085 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        box-shadow: 0 15px 50px rgba(0,184,148,0.25);
        border: 3px solid #FFD700;
    }
    
    /* Korea Box */
    .korea-box {
        background: linear-gradient(135deg, #E4002B 0%, #003DA5 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        box-shadow: 0 15px 50px rgba(228,0,43,0.25);
    }
    
    /* Success/Info/Warning Boxes */
    .success-box { background: #E8F5E9; border-left: 4px solid #00B894; padding: 1.5rem; border-radius: 12px; margin: 1rem 0; }
    .info-box { background: #E3F2FD; border-left: 4px solid #003DA5; padding: 1.5rem; border-radius: 12px; margin: 1rem 0; }
    .warning-box { background: #FFEBEE; border-left: 4px solid #E4002B; padding: 1.5rem; border-radius: 12px; margin: 1rem 0; }
    
    /* Live Indicator */
    .live-dot {
        width: 12px; height: 12px;
        background: #00B894;
        border-radius: 50%;
        display: inline-block;
        margin-right: 10px;
        animation: pulse 2s infinite;
        box-shadow: 0 0 10px #00B894;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.1); }
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# TRANSLATIONS KO/EN
# =============================================================================

def lang():
    return st.session_state.get('lang', 'en')

def is_ko():
    return lang() == 'ko'

TR = {
    'ko': {
        'home': '🏠 대시보드',
        'live': '📡 실시간 모니터링',
        'greensteel': '🌱 그린스틸',
        'credits': '💰 환경 크레딧',
        'business': '📊 비즈니스 케이스',
        'simulation': '🎮 시뮬레이션',
        'hyrex': '⚗️ HyREX 기술',
        'carbon_neutral': '🇰🇷 2050 탄소중립',
        'compliance': '📋 컴플라이언스',
        'mrv': '🔗 MRV 아키텍처',
        'year': '년',
        'days': '일',
        'sensors': '센서',
        'employees': '직원',
        'payback': '투자회수',
        'total_value': '총 환경경제가치',
    },
    'en': {
        'home': '🏠 Dashboard',
        'live': '📡 Live Monitoring',
        'greensteel': '🌱 Green Steel',
        'credits': '💰 Environmental Credits',
        'business': '📊 Business Case',
        'simulation': '🎮 Simulation',
        'hyrex': '⚗️ HyREX Technology',
        'carbon_neutral': '🇰🇷 2050 Carbon Neutral',
        'compliance': '📋 Compliance',
        'mrv': '🔗 MRV Architecture',
        'year': 'year',
        'days': 'days',
        'sensors': 'sensors',
        'employees': 'employees',
        'payback': 'Payback',
        'total_value': 'Total Environmental Economic Value',
    }
}

def t(key):
    return TR[lang()].get(key, key)

# =============================================================================
# POSCO DATA - 4 DIVISIONS
# =============================================================================

POSCO_DATA = {
    'company': {
        'name': 'POSCO Holdings',
        'name_ko': '포스코홀딩스',
        'founded': 1968,
        'revenue_krw': 73000000000000,  # ₩73T
        'revenue_usd': 60000000000,     # $60B
        'employees': 36000,
        'production_mt': 42,
        'world_rank': 6,
        'hq': 'Pohang/Seoul, Korea',
    },
    
    'divisions': {
        'steelmaking': {
            'name': 'Steelmaking' if not is_ko() else '제철',
            'emoji': '🏭',
            'pct': 60,
            'revenue_krw': 43800000000000,
            'production_mt': 42,
            'bf_bof_mt': 38,
            'eaf_mt': 4,
            'intensity_kg_co2': 1857,
            'credits_krw': 350000000000,  # ₩350B
            'sensors': 25,
        },
        'chemical': {
            'name': 'Chemical' if not is_ko() else '화학',
            'emoji': '⚗️',
            'pct': 15,
            'revenue_krw': 10950000000000,
            'lithium_kt': 85,
            'hydrogen_kt': 125,
            'credits_krw': 120000000000,  # ₩120B
            'sensors': 15,
        },
        'construction': {
            'name': 'Construction' if not is_ko() else '건설',
            'emoji': '🏗️',
            'pct': 15,
            'revenue_krw': 10950000000000,
            'credits_krw': 80000000000,  # ₩80B
            'sensors': 10,
        },
        'energy': {
            'name': 'Energy' if not is_ko() else '에너지',
            'emoji': '⚡',
            'pct': 10,
            'revenue_krw': 7300000000000,
            'lng_mt': 3.5,
            'renewable_mw': 80,
            'credits_krw': 60000000000,  # ₩60B
            'sensors': 10,
        },
    },
    
    'credits': {
        'level_1': {
            'carbon_k_ets': 157500000000,      # ₩157.5B - K-ETS
            'green_steel_premium': 246000000000,  # ₩246B - HyREX + EAF premium
            'scrap_recycling': 127500000000,   # ₩127.5B - Circular steel
            'hydrogen': 79000000000,            # ₩79B - Green H2
            'total': 610000000000,              # ₩610B
        },
        'level_2': {
            'operational': 1200000000000,       # ₩1.2T
            'technology': 900000000000,         # ₩900B
            'compliance': 750000000000,         # ₩750B
            'social': 350000000000,             # ₩350B
            'total': 3200000000000,             # ₩3.2T
        },
        'level_3': {
            'hyrex_commercial': 1500000000000,  # ₩1.5T - HyREX 5Mt
            'hydrogen_scale': 800000000000,    # ₩800B - 125Kt H2
            'battery_materials': 950000000000, # ₩950B - Lithium, cathodes
            'ccus': 550000000000,              # ₩550B - 10Mt CO2
            'total': 3800000000000,            # ₩3.8T
        },
    },
    
    'green_steel': {
        'hyrex': {
            'pilot_year': 2024,
            'pilot_kt': 50,
            'commercial_year': 2030,
            'commercial_mt': 5.0,
            'co2_reduction': 95,
            'h2_per_tonne': 50,
        },
        'eaf': {
            'current_mt': 4.0,
            'target_mt': 8.0,
            'scrap_rate': 100,
            'kwh_per_tonne': 450,
        },
        'ccus': {
            'pilot_mt': 0.1,
            'target_2030_mt': 1.0,
            'target_2050_mt': 10.0,
        },
    },
    
    'compliance': {
        'k_ets': {'name': 'K-ETS Phase 3', 'score': 96, 'status': '✅'},
        'responsible_steel': {'name': 'ResponsibleSteel', 'score': 94, 'status': '✅'},
        'iso14064': {'name': 'ISO 14064-1:2018', 'score': 100, 'status': '✅'},
        'iso50001': {'name': 'ISO 50001:2018', 'score': 100, 'status': '✅'},
        'ghg': {'name': 'GHG Protocol', 'score': 98, 'status': '✅'},
        'tcfd': {'name': 'TCFD', 'score': 95, 'status': '✅'},
        'cdp': {'name': 'CDP A-', 'score': 92, 'status': '🏆'},
        'sbti': {'name': 'SBTi Committed', 'score': 88, 'status': '🎯'},
    },
    
    'korea_2050': {
        'emissions_reduction': {'current': 18, 'target': 40, 'year': 2030, 'unit': '%'},
        'renewable_steel': {'current': 10, 'target': 50, 'year': 2030, 'unit': '%'},
        'hydrogen_steel': {'current': 0.1, 'target': 12, 'year': 2030, 'unit': '%'},
        'recycling_rate': {'current': 20, 'target': 40, 'year': 2030, 'unit': '%'},
        'ccus_capacity': {'current': 0.1, 'target': 1.0, 'year': 2030, 'unit': 'Mt'},
    },
}

# =============================================================================
# SESSION STATE
# =============================================================================

if 'lang' not in st.session_state:
    st.session_state.lang = 'en'
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'sim' not in st.session_state:
    st.session_state.sim = {'hyrex': 100, 'eaf': 100, 'scrap': 100, 'h2': 100, 'ccus': 100}

# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    # Language Toggle
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🇰🇷 한국어", use_container_width=True, 
                    type="primary" if is_ko() else "secondary"):
            st.session_state.lang = 'ko'
            st.rerun()
    with col2:
        if st.button("🇬🇧 English", use_container_width=True,
                    type="primary" if not is_ko() else "secondary"):
            st.session_state.lang = 'en'
            st.rerun()
    
    st.markdown("---")
    
    # POSCO Logo
    st.markdown(f"""
    <div style='text-align:center;padding:1rem;background:white;border-radius:15px;margin-bottom:1rem;'>
        <div style='font-size:2.5rem;'>🏭</div>
        <h2 style='color:#003DA5;margin:0.5rem 0 0 0;font-size:1.3rem;'>
            {'포스코' if is_ko() else 'POSCO'}
        </h2>
        <p style='color:#666;font-size:0.8rem;margin:0;'>× Rekarbon MRV</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    pages = ['home', 'live', 'greensteel', 'credits', 'business', 'simulation', 'hyrex', 'carbon_neutral', 'compliance', 'mrv']
    
    for page in pages:
        if st.button(t(page), use_container_width=True,
                    type="primary" if st.session_state.page == page else "secondary"):
            st.session_state.page = page
            st.rerun()
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown(f"""
    <div style='background:rgba(0,61,165,0.1);padding:1rem;border-radius:10px;'>
        <p style='margin:0;font-size:0.85rem;'>
            <strong>{'설립' if is_ko() else 'Founded'}:</strong> 1968<br>
            <strong>{'매출' if is_ko() else 'Revenue'}:</strong> ₩73T<br>
            <strong>{'생산량' if is_ko() else 'Production'}:</strong> 42 Mt<br>
            <strong>{'세계순위' if is_ko() else 'World Rank'}:</strong> #6<br>
            <strong>{'센서' if is_ko() else 'Sensors'}:</strong> 60 IoT
        </p>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# PAGE: HOME / DASHBOARD
# =============================================================================

if st.session_state.page == 'home':
    # Header
    st.markdown(f"""
    <div class='posco-header'>
        <h1>{'포스코홀딩스 × 리카본' if is_ko() else 'POSCO HOLDINGS × REKARBON'}</h1>
        <p class='subtitle'>{'그린스틸 및 탈탄소화를 위한 엣지 네이티브 MRV 플랫폼 • 60 IoT 센서 • 4개 사업부문' if is_ko() else 'Edge-Native MRV Platform for Green Steel & Decarbonization • 60 IoT Sensors • 4 Divisions'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Top Level Metrics
    l1 = POSCO_DATA['credits']['level_1']['total']
    l2 = l1 + POSCO_DATA['credits']['level_2']['total']
    l3 = l2 + POSCO_DATA['credits']['level_3']['total']
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>{'레벨1: 거래가능 크레딧' if is_ko() else 'LEVEL 1: TRADEABLE CREDITS'}</div>
            <div class='metric-value'>₩{l1/1e12:.2f}T</div>
            <span class='level-badge level-1'>/{t('year')}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>{'레벨2: 총경제가치' if is_ko() else 'LEVEL 2: ECONOMIC VALUE'}</div>
            <div class='metric-value'>₩{l2/1e12:.2f}T</div>
            <span class='level-badge level-2'>/{t('year')}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with c3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>{'레벨3: 미래시장 포함' if is_ko() else 'LEVEL 3: FUTURE MARKETS'}</div>
            <div class='metric-value'>₩{l3/1e12:.2f}T</div>
            <span class='level-badge level-3'>/{t('year')}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with c4:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>{'USD 환산' if is_ko() else 'USD EQUIVALENT'}</div>
            <div class='metric-value'>${l3/1250/1e9:.1f}B</div>
            <span class='metric-delta positive'>/{t('year')}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 4 Divisions
    st.markdown(f"### {'4개 사업부문' if is_ko() else '4 Business Divisions'}")
    
    cols = st.columns(4)
    divs = list(POSCO_DATA['divisions'].items())
    
    for i, (key, div) in enumerate(divs):
        with cols[i]:
            st.markdown(f"""
            <div class='metric-card' style='text-align:center;'>
                <div style='font-size:3rem;'>{div['emoji']}</div>
                <h4 style='color:#003DA5;margin:0.5rem 0;'>{div['name']}</h4>
                <p style='font-size:0.85rem;color:#666;'>{div['pct']}% {'매출' if is_ko() else 'Revenue'}</p>
                <div style='font-size:1.8rem;font-weight:800;color:#001F5B;'>₩{div['credits_krw']/1e9:.0f}B</div>
                <p style='font-size:0.75rem;color:#00B894;margin-top:0.5rem;'>{div['sensors']} {t('sensors')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Green Steel Technologies
    st.markdown(f"### {'그린스틸 기술' if is_ko() else 'Green Steel Technologies'}")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"""
        <div class='hyrex-box'>
            <h4 style='color:white;margin:0;'>⚗️ HyREX {'(수소환원제철)' if is_ko() else '(Hydrogen DRI)'}</h4>
            <div style='font-size:4rem;font-weight:800;text-align:center;margin:1rem 0;'>95%</div>
            <p style='color:rgba(255,255,255,0.9);text-align:center;'>CO₂ {'감축' if is_ko() else 'Reduction'} vs BF-BOF</p>
            <p style='color:rgba(255,255,255,0.7);text-align:center;font-size:0.85rem;'>{'파일럿 2024 • 상용 2030' if is_ko() else 'Pilot 2024 • Commercial 2030'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown(f"""
        <div class='steel-box'>
            <h4 style='color:white;margin:0;'>♻️ {'전기로 (EAF)' if is_ko() else 'Electric Arc Furnace'}</h4>
            <div style='font-size:4rem;font-weight:800;text-align:center;margin:1rem 0;'>8Mt</div>
            <p style='color:rgba(255,255,255,0.9);text-align:center;'>{'2030년 목표' if is_ko() else '2030 Target'}</p>
            <p style='color:rgba(255,255,255,0.7);text-align:center;font-size:0.85rem;'>{'100% 스크랩 재활용' if is_ko() else '100% Scrap Recycling'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with c3:
        st.markdown(f"""
        <div class='korea-box'>
            <h4 style='color:white;margin:0;'>🔒 CCUS {'(탄소포집)' if is_ko() else '(Carbon Capture)'}</h4>
            <div style='font-size:4rem;font-weight:800;text-align:center;margin:1rem 0;'>10Mt</div>
            <p style='color:rgba(255,255,255,0.9);text-align:center;'>{'2050년 목표' if is_ko() else '2050 Target'}</p>
            <p style='color:rgba(255,255,255,0.7);text-align:center;font-size:0.85rem;'>{'동해 해저 저장' if is_ko() else 'East Sea Storage'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Certifications
    st.markdown(f"### {'인증 및 표준' if is_ko() else 'Certifications'}")
    
    certs = ['K-ETS', 'ResponsibleSteel', 'ISO 14064', 'ISO 50001', 'GHG Protocol', 'TCFD', 'CDP A-', 'SBTi']
    cert_html = " ".join([f"<span class='cert-badge'>{c}</span>" for c in certs])
    st.markdown(f"<div style='text-align:center;'>{cert_html}</div>", unsafe_allow_html=True)

# =============================================================================
# PAGE: LIVE MONITORING
# =============================================================================

elif st.session_state.page == 'live':
    st.markdown(f"""
    <div class='posco-header'>
        <h1>📡 {'실시간 모니터링' if is_ko() else 'Live Monitoring'}</h1>
        <p class='subtitle'><span class='live-dot'></span>{'60개 IoT 센서 실시간 데이터 • CERBERE 보안' if is_ko() else 'Real-time data from 60 IoT sensors • CERBERE Protected'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-refresh
    auto_refresh = st.checkbox("🔄 Auto-refresh (5s)", value=False)
    if auto_refresh:
        time.sleep(0.1)
        st.rerun()
    
    # CERBERE Status
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#001F5B,#003DA5);padding:1rem;border-radius:10px;margin-bottom:1rem;'>
        <span style='color:#00B894;font-weight:bold;'>🛡️ CERBERE</span>
        <span style='color:white;margin-left:1rem;'>{'상태' if is_ko() else 'Status'}:</span>
        <span style='color:#00B894;margin-left:0.5rem;'>● ACTIVE</span>
        <span style='color:rgba(255,255,255,0.7);margin-left:2rem;'>Last scan: {datetime.now().strftime('%H:%M:%S')}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Real-Time Gauges
    st.markdown(f"### {'실시간 게이지' if is_ko() else 'Real-Time Gauges'}")
    
    cols = st.columns(4)
    
    with cols[0]:
        val = 42000 + np.random.randint(-500, 500)
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=val,
            title={'text': "Steel Production (t/day)", 'font': {'size': 14}},
            gauge={'axis': {'range': [35000, 50000]}, 'bar': {'color': "#003DA5"}}
        ))
        fig.update_layout(height=250, margin=dict(t=50, b=0, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with cols[1]:
        val = 1857 + np.random.uniform(-50, 50)
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=val,
            title={'text': "CO₂ Intensity (kg/t)", 'font': {'size': 14}},
            delta={'reference': 1857, 'decreasing': {'color': "#00B894"}},
            gauge={'axis': {'range': [1000, 2500]}, 'bar': {'color': "#E4002B"},
                   'steps': [{'range': [1000, 1500], 'color': "#E8F5E9"}, {'range': [1500, 2000], 'color': "#FFF3E0"},
                             {'range': [2000, 2500], 'color': "#FFEBEE"}]}
        ))
        fig.update_layout(height=250, margin=dict(t=50, b=0, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with cols[2]:
        val = 20 + np.random.uniform(-2, 2)
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=val,
            title={'text': "Scrap Rate (%)", 'font': {'size': 14}},
            delta={'reference': 20},
            gauge={'axis': {'range': [0, 50]}, 'bar': {'color': "#00B894"}}
        ))
        fig.update_layout(height=250, margin=dict(t=50, b=0, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with cols[3]:
        val = 96.5 + np.random.uniform(-1, 1)
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=val,
            title={'text': "K-ETS Compliance (%)", 'font': {'size': 14}},
            gauge={'axis': {'range': [80, 100]}, 'bar': {'color': "#003DA5"}}
        ))
        fig.update_layout(height=250, margin=dict(t=50, b=0, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Blast Furnace Dashboard
    st.markdown(f"### 🏭 {'고로 모니터링 대시보드' if is_ko() else 'Blast Furnace Monitoring Dashboard'}")
    
    bf_data = []
    bf_names = ["BF-1 Pohang", "BF-2 Pohang", "BF-3 Pohang", "BF-4 Pohang", "BF-1 Gwangyang", 
                "BF-2 Gwangyang", "BF-3 Gwangyang", "BF-4 Gwangyang", "BF-5 Gwangyang"]
    
    for i, name in enumerate(bf_names):
        output = 8000 + np.random.randint(-500, 1000)
        intensity = 1800 + np.random.randint(-100, 100)
        bf_data.append({
            "🏭 Furnace": name,
            "Output (t/day)": f"{output:,}",
            "Temp (°C)": f"{1500 + np.random.randint(-20, 20):,}",
            "CO₂ (kg/t)": intensity,
            "Efficiency": f"{92 + np.random.uniform(-2, 3):.1f}%",
            "Status": np.random.choice(["🟢 Running", "🟢 Running", "🟢 Running", "🟡 Maintenance"])
        })
    
    df_bf = pd.DataFrame(bf_data)
    st.dataframe(df_bf, use_container_width=True, hide_index=True)
    
    # Production Charts
    c1, c2 = st.columns(2)
    
    with c1:
        hours = list(range(24))
        bf_prod = [38000 + np.random.randint(-2000, 2000) for _ in hours]
        eaf_prod = [4000 + np.random.randint(-500, 500) for _ in hours]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hours, y=bf_prod, name='BF-BOF', fill='tozeroy', fillcolor='rgba(0,61,165,0.3)', line=dict(color='#003DA5', width=2)))
        fig.add_trace(go.Scatter(x=hours, y=eaf_prod, name='EAF', fill='tozeroy', fillcolor='rgba(0,184,148,0.3)', line=dict(color='#00B894', width=2)))
        
        fig.update_layout(
            title={'text': 'Production by Route (t/day)' if not is_ko() else '생산경로별 생산량 (t/일)', 'x': 0.5},
            height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title='Hour', yaxis_title='Tonnes'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        times = pd.date_range(end=datetime.now(), periods=60, freq='1min')
        emissions = 1857 + np.cumsum(np.random.randn(60) * 5)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=times, y=emissions, name='Intensity',
                                 line=dict(color='#E4002B', width=2), fill='tozeroy',
                                 fillcolor='rgba(228,0,43,0.1)'))
        fig.add_hline(y=1650, line_dash="dash", line_color="#00B894", annotation_text="2030 Target")
        
        fig.update_layout(
            title={'text': 'CO₂ Intensity (kg/t steel)' if not is_ko() else 'CO₂ 집약도 (kg/t 철강)', 'x': 0.5},
            height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PAGE: GREEN STEEL
# =============================================================================

elif st.session_state.page == 'greensteel':
    st.markdown(f"""
    <div class='posco-header'>
        <h1>🌱 {'그린스틸' if is_ko() else 'Green Steel'}</h1>
        <p class='subtitle'>{'HyREX + EAF + CCUS로 탈탄소 철강 실현' if is_ko() else 'Decarbonizing Steel with HyREX + EAF + CCUS'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Green Steel Roadmap
    st.markdown(f"### {'그린스틸 로드맵' if is_ko() else 'Green Steel Roadmap'}")
    
    years = [2024, 2026, 2028, 2030, 2040, 2050]
    bf_bof = [38, 36, 32, 25, 10, 0]
    eaf = [4, 5, 6, 8, 15, 20]
    hyrex = [0.05, 0.5, 2, 5, 15, 22]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=years, y=bf_bof, name='BF-BOF', marker_color='#E4002B'))
    fig.add_trace(go.Bar(x=years, y=eaf, name='EAF', marker_color='#003DA5'))
    fig.add_trace(go.Bar(x=years, y=hyrex, name='HyREX', marker_color='#00B894'))
    
    fig.update_layout(
        title={'text': 'Steel Production Mix (Mt/year)' if not is_ko() else '철강 생산믹스 (Mt/년)', 'x': 0.5},
        barmode='stack', height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # CO2 Intensity Comparison
    c1, c2 = st.columns(2)
    
    with c1:
        routes = ['BF-BOF', 'EAF (Grid)', 'EAF (Renewable)', 'HyREX']
        intensities = [1857, 650, 450, 100]
        colors = ['#E4002B', '#003DA5', '#0066CC', '#00B894']
        
        fig = go.Figure(data=[go.Bar(x=routes, y=intensities, marker_color=colors)])
        fig.update_layout(
            title={'text': 'CO₂ Intensity by Route (kg/t)' if not is_ko() else '생산경로별 CO₂ 집약도 (kg/t)', 'x': 0.5},
            height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.markdown(f"""
        <div class='hyrex-box'>
            <h4 style='color:white;margin:0;'>⚗️ HyREX {'기술 핵심' if is_ko() else 'Technology'}</h4>
            <ul style='color:rgba(255,255,255,0.9);margin-top:1rem;'>
                <li><strong>{'원리' if is_ko() else 'Principle'}:</strong> {'수소로 철광석 환원' if is_ko() else 'H₂ reduces iron ore'}</li>
                <li><strong>{'효율' if is_ko() else 'Efficiency'}:</strong> 50 kg H₂/t {'철강' if is_ko() else 'steel'}</li>
                <li><strong>CO₂:</strong> 95% {'감축' if is_ko() else 'reduction'} vs BF-BOF</li>
                <li><strong>{'파일럿' if is_ko() else 'Pilot'}:</strong> 2024 (50 kt/{'년' if is_ko() else 'year'})</li>
                <li><strong>{'상용화' if is_ko() else 'Commercial'}:</strong> 2030 (5 Mt/{'년' if is_ko() else 'year'})</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# PAGE: CREDITS
# =============================================================================

elif st.session_state.page == 'credits':
    st.markdown(f"""
    <div class='posco-header'>
        <h1>💰 {'환경 크레딧' if is_ko() else 'Environmental Credits'}</h1>
        <p class='subtitle'>{'3단계 가치평가 프레임워크' if is_ko() else '3-Level Valuation Framework'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Level 1
    st.markdown(f"### {'레벨1: 거래가능 크레딧' if is_ko() else 'Level 1: Tradeable Credits'}")
    
    l1 = POSCO_DATA['credits']['level_1']
    cols = st.columns(4)
    items = [('K-ETS Carbon', l1['carbon_k_ets']), ('Green Steel Premium', l1['green_steel_premium']),
             ('Scrap Recycling', l1['scrap_recycling']), ('Green Hydrogen', l1['hydrogen'])]
    
    for i, (name, val) in enumerate(items):
        with cols[i]:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>{name.upper()}</div>
                <div class='metric-value' style='font-size:1.8rem;'>₩{val/1e9:.0f}B</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='text-align:center;margin:2rem 0;'>
        <span class='level-badge level-1' style='font-size:1.5rem;padding:1rem 3rem;'>
            {'레벨1 합계' if is_ko() else 'Level 1 Total'}: ₩{l1['total']/1e9:.0f}B/{t('year')} (${l1['total']/1250/1e6:.0f}M)
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Level 2 + 3
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown(f"### {'레벨2: 추가경제가치' if is_ko() else 'Level 2: Additional Value'}")
        l2 = POSCO_DATA['credits']['level_2']
        for name, val in [(k, v) for k, v in l2.items() if k != 'total']:
            st.markdown(f"""
            <div class='metric-card' style='border-left-color:#E4002B;'>
                <div class='metric-label'>{name.upper()}</div>
                <div class='metric-value' style='font-size:1.5rem;color:#E4002B;'>₩{val/1e9:.0f}B</div>
            </div>
            """, unsafe_allow_html=True)
    
    with c2:
        st.markdown(f"### {'레벨3: 미래시장' if is_ko() else 'Level 3: Future Markets'}")
        l3 = POSCO_DATA['credits']['level_3']
        for name, val in [(k, v) for k, v in l3.items() if k != 'total']:
            st.markdown(f"""
            <div class='metric-card' style='border-left-color:#00B894;'>
                <div class='metric-label'>{name.replace('_', ' ').upper()}</div>
                <div class='metric-value' style='font-size:1.5rem;color:#00B894;'>₩{val/1e9:.0f}B</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Total
    total = l1['total'] + l2['total'] + l3['total']
    st.markdown(f"""
    <div class='steel-box' style='text-align:center;margin-top:2rem;'>
        <h2 style='color:white;margin:0;'>{t('total_value')}</h2>
        <div style='font-size:5rem;font-weight:800;margin:1rem 0;'>₩{total/1e12:.1f}T</div>
        <p style='color:rgba(255,255,255,0.8);font-size:1.3rem;'>${total/1250/1e9:.1f}B / {t('year')}</p>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# PAGE: BUSINESS CASE
# =============================================================================

elif st.session_state.page == 'business':
    st.markdown(f"""
    <div class='posco-header'>
        <h1>📊 {'비즈니스 케이스' if is_ko() else 'Business Case'}</h1>
        <p class='subtitle'>{'투자수익률 분석' if is_ko() else 'Return on Investment Analysis'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>{'투자액' if is_ko() else 'INVESTMENT'}</div>
            <div class='metric-value'>₩3.75B</div>
            <span class='metric-delta warning'>$3M</span>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>{'투자회수' if is_ko() else 'PAYBACK'}</div>
            <div class='metric-value'>1 {t('days')}</div>
            <span class='metric-delta positive'>~24{'시간' if is_ko() else 'h'}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with c3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>5-{'년' if is_ko() else 'YEAR'} ROI</div>
            <div class='metric-value'>425,000%</div>
            <span class='metric-delta positive'>{'탁월' if is_ko() else 'Exceptional'}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with c4:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>5-{'년 순이익' if is_ko() else 'YEAR PROFIT'}</div>
            <div class='metric-value'>₩38T</div>
            <span class='metric-delta positive'>$30B</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 5-Year Projection
    years = [1, 2, 3, 4, 5]
    l1_rev = [0.61, 0.65, 0.70, 0.75, 0.80]
    l2_rev = [3.2, 3.4, 3.6, 3.8, 4.0]
    l3_rev = [0.5, 1.2, 2.0, 3.0, 3.8]
    total_rev = [a+b+c for a, b, c in zip(l1_rev, l2_rev, l3_rev)]
    cumulative = [sum(total_rev[:i+1]) for i in range(5)]
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Bar(x=years, y=l1_rev, name='Level 1', marker_color='#003DA5'), secondary_y=False)
    fig.add_trace(go.Bar(x=years, y=l2_rev, name='Level 2', marker_color='#E4002B'), secondary_y=False)
    fig.add_trace(go.Bar(x=years, y=l3_rev, name='Level 3', marker_color='#00B894'), secondary_y=False)
    fig.add_trace(go.Scatter(x=years, y=cumulative, name='Cumulative (₩T)',
                             mode='lines+markers', line=dict(color='#001F5B', width=4),
                             marker=dict(size=12)), secondary_y=True)
    
    fig.update_layout(
        title={'text': '5-Year Revenue & Cumulative' if not is_ko() else '5년 매출 및 누적', 'x': 0.5},
        barmode='stack', height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5)
    )
    
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PAGE: SIMULATION
# =============================================================================

elif st.session_state.page == 'simulation':
    st.markdown(f"""
    <div class='posco-header'>
        <h1>🎮 {'인터랙티브 시뮬레이션' if is_ko() else 'Interactive Simulation'}</h1>
        <p class='subtitle'>{'파라미터를 조정하고 실시간 영향 확인' if is_ko() else 'Adjust parameters and see real-time impact'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    
    with c1:
        hyrex = st.slider("HyREX Production (%)" if not is_ko() else "HyREX 생산 (%)", 50, 200, st.session_state.sim['hyrex'])
        eaf = st.slider("EAF Capacity (%)" if not is_ko() else "전기로 용량 (%)", 50, 200, st.session_state.sim['eaf'])
        scrap = st.slider("Scrap Rate (%)" if not is_ko() else "스크랩 비율 (%)", 50, 150, st.session_state.sim['scrap'])
    
    with c2:
        h2 = st.slider("Green H2 (%)" if not is_ko() else "그린수소 (%)", 50, 200, st.session_state.sim['h2'])
        ccus = st.slider("CCUS Capture (%)" if not is_ko() else "CCUS 포집 (%)", 50, 200, st.session_state.sim['ccus'])
    
    st.session_state.sim = {'hyrex': hyrex, 'eaf': eaf, 'scrap': scrap, 'h2': h2, 'ccus': ccus}
    
    # Calculate
    base_l1 = 610  # ₩B
    sim_carbon = 157.5 * (ccus / 100)
    sim_green = 246 * (hyrex / 100) * (eaf / 100)
    sim_scrap = 127.5 * (scrap / 100)
    sim_h2 = 79 * (h2 / 100)
    sim_l1 = sim_carbon + sim_green + sim_scrap + sim_h2
    sim_l2 = sim_l1 + 3200 * ((hyrex + eaf) / 200)
    sim_l3 = sim_l2 + 3800 * ((hyrex + h2) / 200)
    
    st.markdown("---")
    st.markdown(f"### {'시뮬레이션 결과' if is_ko() else 'Simulation Results'}")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Level 1", f"₩{sim_l1:.0f}B", f"{((sim_l1/base_l1)-1)*100:+.1f}%")
    with c2: st.metric("Level 2", f"₩{sim_l2/1000:.2f}T", f"{((sim_l2/3810)-1)*100:+.1f}%")
    with c3: st.metric("Total", f"₩{sim_l3/1000:.2f}T", f"{((sim_l3/7610)-1)*100:+.1f}%")
    with c4:
        intensity = 1857 * (1 - (hyrex - 100) / 200 * 0.5)
        st.metric("CO₂ (kg/t)", f"{intensity:.0f}", f"{((intensity/1857)-1)*100:+.1f}%")
    
    # Charts
    c1, c2 = st.columns(2)
    
    with c1:
        categories = ['HyREX', 'EAF', 'Scrap', 'H2', 'CCUS']
        values = [hyrex/200*100, eaf/200*100, scrap/150*100, h2/200*100, ccus/200*100]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values + [values[0]], theta=categories + [categories[0]],
            fill='toself', fillcolor='rgba(0,61,165,0.2)', line=dict(color='#003DA5', width=3)
        ))
        fig.update_layout(
            title={'text': 'Performance Radar', 'x': 0.5},
            polar=dict(radialaxis=dict(range=[0, 100])), height=400, paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        baseline = [157.5, 246, 127.5, 79, 0]
        simulated = [sim_carbon, sim_green, sim_scrap, sim_h2, 0]
        
        fig = go.Figure(data=[
            go.Bar(name='Baseline', x=categories, y=baseline, marker_color='#001F5B'),
            go.Bar(name='Simulated', x=categories, y=simulated, marker_color='#003DA5')
        ])
        fig.update_layout(title={'text': 'Credits Comparison (₩B)', 'x': 0.5}, barmode='group', height=400, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PAGE: KOREA 2050 CARBON NEUTRAL
# =============================================================================

elif st.session_state.page == 'carbon_neutral':
    st.markdown(f"""
    <div class='posco-header'>
        <h1>🇰🇷 {'2050 탄소중립' if is_ko() else '2050 Carbon Neutral'}</h1>
        <p class='subtitle'>{'한국 탄소중립 기본법 완전 준수' if is_ko() else 'Full alignment with Korea Carbon Neutrality Framework Act'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Overall Score
    st.markdown(f"""
    <div class='korea-box' style='text-align:center;'>
        <h2 style='color:white;margin:0;'>{'전체 준수 점수' if is_ko() else 'Overall Alignment Score'}</h2>
        <div style='font-size:5rem;font-weight:800;color:#FFD700;'>89.5%</div>
        <p style='color:rgba(255,255,255,0.9);'>{'철강업계 선도' if is_ko() else 'Steel Industry Leader'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Korea 2050 Targets Progress
    for key, data in POSCO_DATA['korea_2050'].items():
        progress = (data['current'] / data['target']) * 100
        color = "#00B894" if progress >= 70 else "#F39C12" if progress >= 40 else "#E4002B"
        unit = data.get('unit', '%')
        
        st.markdown(f"""
        <div class='metric-card' style='display:flex;justify-content:space-between;align-items:center;border-left-color:{color};'>
            <div>
                <strong>{key.replace('_', ' ').title()}</strong><br>
                <small>{'현재' if is_ko() else 'Current'}: {data['current']}{unit} | {'목표' if is_ko() else 'Target'}: {data['target']}{unit} ({data['year']})</small>
            </div>
            <div style='font-size:2rem;font-weight:800;color:{color};'>{progress:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# PAGE: COMPLIANCE
# =============================================================================

elif st.session_state.page == 'compliance':
    st.markdown(f"""
    <div class='posco-header'>
        <h1>📋 {'컴플라이언스' if is_ko() else 'Compliance'}</h1>
        <p class='subtitle'>{'8개 국제표준 인증' if is_ko() else 'Certified across 8 international standards'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    comp_data = []
    for key, data in POSCO_DATA['compliance'].items():
        comp_data.append({'Standard': data['name'], 'Score': f"{data['score']}%", 'Status': data['status']})
    
    st.dataframe(pd.DataFrame(comp_data), use_container_width=True, hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown(f"""
        <div class='success-box'>
            <h4 style='margin:0;'>🇰🇷 {'한국 규제' if is_ko() else 'Korean Regulations'}</h4>
            <ul>
                <li><strong>K-ETS:</strong> {'3기 완전 준수' if is_ko() else 'Phase 3 Compliant'}</li>
                <li><strong>{'탄소중립기본법' if is_ko() else 'Carbon Neutral Act'}:</strong> {'준수' if is_ko() else 'Compliant'}</li>
                <li><strong>{'대기환경보전법' if is_ko() else 'Clean Air Act'}:</strong> {'준수' if is_ko() else 'Compliant'}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown(f"""
        <div class='info-box'>
            <h4 style='margin:0;'>🌍 {'국제 표준' if is_ko() else 'International Standards'}</h4>
            <ul>
                <li><strong>ResponsibleSteel:</strong> {'인증' if is_ko() else 'Certified'}</li>
                <li><strong>ISO 14064 + 50001:</strong> {'인증' if is_ko() else 'Certified'}</li>
                <li><strong>TCFD + CDP:</strong> A- {'등급' if is_ko() else 'Rating'}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# PAGE: MRV ARCHITECTURE
# =============================================================================

elif st.session_state.page == 'mrv':
    st.markdown(f"""
    <div class='posco-header'>
        <h1>🔗 {'MRV 아키텍처' if is_ko() else 'MRV Architecture'}</h1>
        <p class='subtitle'>{'7계층: Edge → DT-REC → DT-SEQ → 마켓플레이스' if is_ko() else '7-Layer: Edge → DT-REC → DT-SEQ → Marketplace'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Architecture
    st.markdown("""
    <div style='background:linear-gradient(135deg,#001F5B,#003DA5);padding:2rem;border-radius:20px;color:white;'>
        <h3 style='color:#00B894;text-align:center;'>Rekarbon MRV Platform Architecture</h3>
        <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-top:1.5rem;'>
            <div style='background:rgba(0,61,165,0.3);padding:1.5rem;border-radius:15px;text-align:center;border:2px solid #003DA5;'>
                <div style='font-size:2.5rem;'>📡</div>
                <h4 style='color:#74B9FF;'>EDGE</h4>
                <small>60 IoT Sensors<br>Raspberry Pi 5<br>Ed25519 Signatures</small>
            </div>
            <div style='background:rgba(228,0,43,0.3);padding:1.5rem;border-radius:15px;text-align:center;border:2px solid #E4002B;'>
                <div style='font-size:2.5rem;'>🔐</div>
                <h4 style='color:#FF6B6B;'>DT-REC</h4>
                <small>MRV Validation<br>Steel Intensity Calc<br>K-ETS Reporting</small>
            </div>
            <div style='background:rgba(0,184,148,0.3);padding:1.5rem;border-radius:15px;text-align:center;border:2px solid #00B894;'>
                <div style='font-size:2.5rem;'>🔗</div>
                <h4 style='color:#00B894;'>DT-SEQ</h4>
                <small>ERC-3643 Tokens<br>T-REX Compliant<br>Proof Packs</small>
            </div>
            <div style='background:rgba(255,215,0,0.3);padding:1.5rem;border-radius:15px;text-align:center;border:2px solid #FFD700;'>
                <div style='font-size:2.5rem;'>💰</div>
                <h4 style='color:#FFD700;'>MARKET</h4>
                <small>K-ETS (KRX)<br>ResponsibleSteel<br>Green Premium</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # CERBERE
    st.markdown(f"### 🛡️ {'CERBERE 보안 통합' if is_ko() else 'CERBERE Security Integration'}")
    
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#001F5B,#E4002B);padding:2rem;border-radius:20px;color:white;'>
        <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;'>
            <div style='text-align:center;'>
                <div style='font-size:3rem;'>🔒</div>
                <h4 style='color:white;'>Watchdog</h4>
                <p style='font-size:0.85rem;color:rgba(255,255,255,0.8);'>{'실시간 침입탐지' if is_ko() else 'Real-time intrusion detection'}</p>
            </div>
            <div style='text-align:center;'>
                <div style='font-size:3rem;'>🔐</div>
                <h4 style='color:white;'>Nexus (SIEM)</h4>
                <p style='font-size:0.85rem;color:rgba(255,255,255,0.8);'>{'이벤트 상관분석' if is_ko() else 'Event correlation'}</p>
            </div>
            <div style='text-align:center;'>
                <div style='font-size:3rem;'>👻</div>
                <h4 style='color:white;'>Ghost</h4>
                <p style='font-size:0.85rem;color:rgba(255,255,255,0.8);'>{'허니팟 & 스텔스' if is_ko() else 'Honeypots & Stealth'}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")

total = POSCO_DATA['credits']['level_1']['total'] + POSCO_DATA['credits']['level_2']['total'] + POSCO_DATA['credits']['level_3']['total']

year_text = t('year')
total_value_text = t('total_value')
days_text = t('days')
payback_text = t('payback')
cert_text = '인증' if is_ko() else 'Certifications'
carbon_text = '탄소중립' if is_ko() else 'Carbon Neutral'
align_text = '준수점수' if is_ko() else 'Alignment'
ceo_text = '창립자 & CEO' if is_ko() else 'Founder & CEO'
posco_text = '포스코홀딩스' if is_ko() else 'POSCO Holdings'

st.markdown(f"""
<div style="background:linear-gradient(135deg,#003DA5 0%,#001F5B 50%,#E4002B 100%);padding:3rem;border-radius:20px;color:white;">
    <div style="text-align:center;">
        <h2 style="color:white;margin:0;">{posco_text} × Rekarbon</h2>
        <div style="font-size:3.5rem;font-weight:800;margin:1rem 0;">₩{total/1e12:.1f}T / {year_text}</div>
        <p style="color:rgba(255,255,255,0.8);font-size:1.3rem;">${total/1250/1e9:.1f}B / {year_text} - {total_value_text}</p>
    </div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""
    <div style="background:#001F5B;padding:1.5rem;border-radius:15px;color:white;text-align:center;height:150px;">
        <h4 style="color:white;margin:0 0 0.5rem 0;">{cert_text}</h4>
        <p style="margin:0;font-size:0.9rem;">K-ETS • ResponsibleSteel<br>ISO 14064 • TCFD • CDP A-</p>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div style="background:#001F5B;padding:1.5rem;border-radius:15px;color:white;text-align:center;height:150px;">
        <h4 style="color:white;margin:0 0 0.5rem 0;">🇰🇷 {carbon_text}</h4>
        <p style="margin:0;font-size:0.9rem;">89.5% {align_text}<br>2050 Net-Zero</p>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div style="background:#001F5B;padding:1.5rem;border-radius:15px;color:white;text-align:center;height:150px;">
        <h4 style="color:white;margin:0 0 0.5rem 0;">💰 ROI</h4>
        <p style="margin:0;font-size:0.9rem;">{payback_text}: 1 {days_text}<br>5Y ROI: 425,000%</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div style="background:linear-gradient(135deg,#001F5B 0%,#E4002B 100%);padding:1.5rem;border-radius:15px;color:white;text-align:center;margin-top:1rem;">
    <p style="margin:0;"><strong>Nicolas Bernot</strong> - {ceo_text}</p>
    <p style="margin:0.5rem 0;">📧 support@rekarbon.com | 🌐 www.rekarbon.com</p>
    <p style="font-size:0.85rem;color:rgba(255,255,255,0.6);margin:0;">© 2026 Rekarbon SAS | Paris 🇫🇷 • La Réunion 🇷🇪</p>
</div>
""", unsafe_allow_html=True)
