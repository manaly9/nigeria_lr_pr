import base64

import pandas as pd
import streamlit as st

from nigeria_data import load_data

# --- PAGE CONFIG ---
st.set_page_config(page_title="Nigeria Economic Dashboard", layout="wide")

# --- 🎨 GLASS UI & BACKGROUND SETUP ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f"""
    <style>
    /* ================================================================= */
    /* 1. GLOBAL LAYOUT SETTINGS                                         */
    /* ================================================================= */
    
    /* REMOVES TOP WHITE SPACE: Moves everything higher up the page */
    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
    }}

    /* MAIN BACKGROUND IMAGE: Controls the full page picture */
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* TRANSPARENT HEADER: Hides the default Streamlit top bar background */
    [data-testid="stHeader"] {{
        background-color: rgba(0,0,0,0);
    }}

    /* ================================================================= */
    /* 2. WHITE GLASS CONTAINERS (THE BOXES)                             */
    /* ================================================================= */

    /* MAIN CONTAINER BOXES: Controls the white glass behind Metrics & Table */
    /* If you want to change opacity, change the 0.9 below */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 10px; 
        border: 1px solid rgba(255, 255, 255, 0.5);
    }}

    /* MAIN HEADING BOX: Controls the box around 'Nigeria State Economy' */
    .title-box {{
        background-color: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(5px);
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 15px;
    }}

    /* ================================================================= */
    /* 3. TEXT & NUMBERS STYLING                                         */
    /* ================================================================= */

    /* METRIC NUMBERS: Controls the '36', '77%', etc. */
    [data-testid="stMetric"] {{
        background-color: white !important;
        color: black !important;
        padding: 20px !important;
        opacity: 80%
        border-radius: 15px;
        border-radius: 15px;
    }}
    
    /* METRIC LABELS: Controls 'Avg Literacy', 'States in View' text */
    [data-testid="stMetricLabel"] p {{
        color: green !important;
        font-weight: bold;
        font-size: 0.9rem !important;
    }}
    
    /* METRIC VALUES: Controls the actual number size/color */
    [data-testid="stMetricValue"] div {{
        color: black !important;
        font-size: 1.8rem !important;
    }}

    /* ================================================================= */
    /* 4. SIDEBAR STYLING                                                */
    /* ================================================================= */
    
    /* SIDEBAR TEXT: Ensures sidebar options are readable */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
        background-color: transparent !important;
        color: black !important;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# CALL BACKGROUND
try:
    set_background('background.jpg')
except FileNotFoundError:
    st.warning("⚠️ Image 'background.jpg' not found.")


# --- 1. CENTERED HEADER ---
st.markdown("""
<div class="title-box">
    <h1 style='color: #333; margin:0; text-align:center; font-size: 2.2rem;'>Nigeria State Economy & Demographics</h1>
    <p style='color: #555; margin:0; font-weight: bold; text-align:center;'>Exploratory Data Analysis of all 36 States including Federal Capital(FCT) </p>
</div>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
df = load_data()

# --- SIDEBAR CONTROLS ---
st.sidebar.header("⚙️ Dashboard Controls")

view_mode = st.sidebar.radio(
    "Select Analysis Mode:",
    ["🔀 Regional Filter", "📊 GDP Rankings", "📚 Literacy Rankings", "📉 Poverty Rankings"]
)

filtered_df = df.copy() 
subtitle = "Overview"

# --- LOGIC ENGINE ---
if view_mode == "🔀 Regional Filter":
    st.sidebar.divider()
    selected_regions = st.sidebar.multiselect(
        "Filter by Region:", 
        options=df["Region"].unique(), 
        default=[]
    )
    if not selected_regions:
        filtered_df = df
        subtitle = "National Overview (All Regions)"
    else:
        filtered_df = df[df["Region"].isin(selected_regions)]
        subtitle = f"Region View: {', '.join(selected_regions)}"

elif view_mode == "📊 GDP Rankings":
    st.sidebar.divider()
    sort_option = st.sidebar.radio(
        "Sort GDP By:",
        ["🏆 Top 5 Richest", "🔻 Bottom 5 Lowest", "⬇️ All (High to Low)"]
    )
    if sort_option == "🏆 Top 5 Richest":
        filtered_df = df.sort_values(by="GDP_Billions_Naira", ascending=False).head(5)
        subtitle = "Top 5 Richest States"
    elif sort_option == "🔻 Bottom 5 Lowest":
        filtered_df = df.sort_values(by="GDP_Billions_Naira", ascending=True).head(5)
        subtitle = "Bottom 5 Lowest GDP States"
    else: 
        filtered_df = df.sort_values(by="GDP_Billions_Naira", ascending=False)
        subtitle = "GDP Ranking (Rich to Poor)"

elif view_mode == "📚 Literacy Rankings":
    st.sidebar.divider()
    sort_option = st.sidebar.radio(
        "Sort Literacy By:",
        ["🎓 Top 5 Most Literate", "⚠️ Bottom 5 Least Literate", "⬇️ All (High to Low)"]
    )
    if sort_option == "🎓 Top 5 Most Literate":
        filtered_df = df.sort_values(by="Literacy_Rate", ascending=False).head(5)
        subtitle = "Top 5 Educated States"
    elif sort_option == "⚠️ Bottom 5 Least Literate":
        filtered_df = df.sort_values(by="Literacy_Rate", ascending=True).head(5)
        subtitle = "States with Literacy Challenges"
    else:
        filtered_df = df.sort_values(by="Literacy_Rate", ascending=False)
        subtitle = "National Literacy Ranking"

elif view_mode == "📉 Poverty Rankings":
    st.sidebar.divider()
    sort_option = st.sidebar.radio(
        "Sort Poverty By:",
        ["🛡️ Lowest Poverty (Best)", "🚨 Highest Poverty (Worst)"]
    )
    if sort_option == "🛡️ Lowest Poverty (Best)":
        filtered_df = df.sort_values(by="Poverty_Rate", ascending=True).head(10)
        subtitle = "Top 10 States with Lowest Poverty"
    else:
        filtered_df = df.sort_values(by="Poverty_Rate", ascending=False).head(10)
        subtitle = "Top 10 States with Highest Poverty"

# --- AUTOMATIC INDEX RESTART ---
filtered_df = filtered_df.reset_index(drop=True)
filtered_df.index = filtered_df.index + 1 

# --- METRICS ROW ---
# The glass background for this row is controlled by 'div[data-testid="stVerticalBlockBorderWrapper"]' in CSS
with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    col1.metric("States in View", len(filtered_df))
    col2.metric("Avg Literacy", f"{filtered_df['Literacy_Rate'].mean():.1f}%")
    col3.metric("Avg GDP", f"₦{filtered_df['GDP_Billions_Naira'].mean():,.0f}B")

# --- MAIN DISPLAY ---
# SUBTITLE STYLING: Controls color and underline of 'National Overview'
st.markdown(f"""
    <h3 style="
        color: white; 
        text-align: center;
        font-weight: bold;
        padding-bottom: 5px;
        margin-bottom: 10px;
        margin-top: 10px;
        border-bottom: 2px solid #ddd; 
    ">
        {subtitle}
    </h3>
""", unsafe_allow_html=True)

left_col, right_col = st.columns([2, 1], gap="small")

with left_col:
    # DATA TABLE CONTAINER: Inherits white glass style from 'stVerticalBlockBorderWrapper'
    with st.container(border=True):
        st.dataframe(
            filtered_df.style.background_gradient(cmap="Greens", subset=["GDP_Billions_Naira"])
                             .background_gradient(cmap="Reds", subset=["Poverty_Rate"]),
            use_container_width=True,
            height=500
        )

with right_col:
    # HIERARCHY FLOW CONTAINER: Inherits white glass style
    with st.container(border=True):
        st.markdown("""
        <div style="background-color: rgba(255, 255, 255, 0.9); padding: 8px; border-radius: 10px; margin-bottom: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h4 style="margin: 0; color: #333;">📊 Hierarchy Flow</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not filtered_df.empty:
            if view_mode == "📉 Poverty Rankings" and "Lowest" in str(sort_option):
                top_state = filtered_df.iloc[0]; bottom_state = filtered_df.iloc[-1]
                metric_col = "Poverty_Rate"; unit = "%"; label = "Poverty"
            elif view_mode == "📚 Literacy Rankings":
                top_state = filtered_df.iloc[0]; bottom_state = filtered_df.iloc[-1]
                metric_col = "Literacy_Rate"; unit = "%"; label = "Literacy"
            else:
                top_state = filtered_df.sort_values("GDP_Billions_Naira", ascending=False).iloc[0]
                bottom_state = filtered_df.sort_values("GDP_Billions_Naira", ascending=False).iloc[-1]
                metric_col = "GDP_Billions_Naira"; unit = "B"; label = "GDP"

            gap = top_state[metric_col] - bottom_state[metric_col]

            # 1. THE PEAK CARD (Green)
            st.markdown(f"""
            <div style="background-color: rgba(255, 255, 255, 0.85); padding: 10px; border-radius: 10px; margin-bottom: 5px; text-align:center; border-left: 6px solid #28a745; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <strong style="color: #28a745; font-size: 14px;">🚀 Peak {label}</strong><br>
                <span style="font-size: 1.3em; font-weight: bold; color: #333;">{top_state['State']}</span><br>
                <span style="font-size: 1.0em; color: #555;">{top_state[metric_col]:,.0f}{unit}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # 2. THE GAP CARD (Dashed Red)
            st.markdown(f"""
            <div style="background-color: rgba(255, 255, 255, 0.85); padding: 5px; border-radius: 20px; text-align: center; margin: 5px 0; border: 1px dashed #ff4b4b;">
                <span style="color: #ff4b4b; font-weight:bold; font-size: 1.0em;">⬇️ Gap: {gap:,.0f}{unit} ⬇️</span>
            </div>
            """, unsafe_allow_html=True)
            
            # 3. THE BASE CARD (Red)
            st.markdown(f"""
            <div style="background-color: rgba(255, 255, 255, 0.85); padding: 10px; border-radius: 10px; text-align: center; margin-top: 5px; border-left: 6px solid #dc3545; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <strong style="color: #dc3545; font-size: 14px;">📉 Base {label}</strong><br>
                <span style="font-size: 1.3em; font-weight: bold; color: #333;">{bottom_state['State']}</span><br>
                <span style="font-size: 1.0em; color: #555;">{bottom_state[metric_col]:,.0f}{unit}</span>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.write("No data to compare.")